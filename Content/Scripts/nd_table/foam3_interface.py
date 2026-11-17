"""
Python interface to FOAM3 (https://github.com/kgrgreer/foam3).

FOAM3 declares models in JavaScript with ``foam.CLASS({...})`` and
``foam.LIB({...})`` blocks. This module parses those declarations directly
from the source tree and exposes them as Python objects, so Python code can
inspect, traverse, and instantiate FOAM3 models without booting a JS runtime.
If Node.js *is* available, ``run_node_script`` runs arbitrary FOAM3 JS via
subprocess for cases the static parser can't cover.

The parser is a balanced-bracket tokenizer (strings, /*...*/, //... aware), not
a full JS parser — it extracts enough structure for class metadata, property
names/classes/values, method names, and require/import/export lists.

Quick start:

    from foam3_interface import FOAM3Registry
    reg = FOAM3Registry()
    reg.parse_directory("foam3/src")
    cls = reg.find("foam.dao.AbstractDAO")
    print(cls.properties, cls.methods)

    # Instantiate as a plain Python object:
    PyDAO = cls.to_python_class()
    inst = PyDAO(some_property="x")
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FOAMProperty:
    name: str
    cls: Optional[str] = None        # class: 'String' / 'Int' / 'StringArray' / ...
    value: Any = None                # literal default (best-effort decoded)
    factory_src: Optional[str] = None
    expression_src: Optional[str] = None
    raw: str = ""                    # original JS source of this property

    def python_default(self) -> Any:
        if self.value is not None:
            return self.value
        if self.cls in {"StringArray", "FObjectArray", "Array"}:
            return []
        if self.cls in {"Map", "FObjectProperty"}:
            return None
        if self.cls == "String":
            return ""
        if self.cls in {"Int", "Long", "Float", "Double"}:
            return 0
        if self.cls == "Boolean":
            return False
        return None


@dataclass
class FOAMMethod:
    name: str
    args: List[str] = field(default_factory=list)
    body_src: str = ""
    raw: str = ""


@dataclass
class FOAMClass:
    package: Optional[str]
    name: str
    kind: str = "CLASS"              # CLASS | LIB | INTERFACE | ENUM | RELATIONSHIP
    extends: Optional[str] = None
    implements: List[str] = field(default_factory=list)
    requires: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)
    properties: List[FOAMProperty] = field(default_factory=list)
    methods: List[FOAMMethod] = field(default_factory=list)
    constants: Dict[str, Any] = field(default_factory=dict)
    source_file: Optional[str] = None

    @property
    def id(self) -> str:
        return f"{self.package}.{self.name}" if self.package else self.name

    def property(self, name: str) -> Optional[FOAMProperty]:
        return next((p for p in self.properties if p.name == name), None)

    def method(self, name: str) -> Optional[FOAMMethod]:
        return next((m for m in self.methods if m.name == name), None)

    def to_python_class(self) -> type:
        """Build a thin Python class with each property as an attribute."""
        defaults = {p.name: p.python_default() for p in self.properties}

        def __init__(self, **kwargs):
            for k, v in defaults.items():
                setattr(self, k, v() if callable(v) else v)
            for k, v in kwargs.items():
                if k not in defaults:
                    raise AttributeError(f"{self.__class__.__name__}: unknown property '{k}'")
                setattr(self, k, v)

        def __repr__(self):
            kv = ", ".join(f"{p.name}={getattr(self, p.name)!r}" for p in self_outer.properties)
            return f"{self.__class__.__name__}({kv})"

        self_outer = self
        return type(self.name, (object,), {
            "__init__": __init__,
            "__repr__": __repr__,
            "_foam_id": self.id,
            "_foam_class": self,
        })


# ---------------------------------------------------------------------------
# Tokenizer / bracket scanner
# ---------------------------------------------------------------------------

_BLOCK_RE = re.compile(r"\bfoam\.(CLASS|LIB|INTERFACE|ENUM|RELATIONSHIP)\s*\(\s*\{")


def _scan_balanced(src: str, start: int) -> int:
    """Return the index in `src` of the matching closing brace for the
    opening `{` at `start - 1`. Handles strings, regex-ish content, and
    /* */ // comments. Returns -1 if unbalanced."""
    depth = 1
    i = start
    n = len(src)
    while i < n:
        c = src[i]
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            i = n if j == -1 else j + 1
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c in ("'", '"', "`"):
            quote = c
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _strip_comments(src: str) -> str:
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            i = n if j == -1 else j
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c in ("'", '"', "`"):
            quote = c
            start = i
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == quote:
                    i += 1
                    break
                i += 1
            out.append(src[start:i])
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _split_top_level_commas(body: str) -> List[str]:
    """Split a JS array body by top-level commas (depth 0). Strings/brackets
    aware. The input is expected to be the body between [ and ]."""
    parts = []
    depth_curly = depth_sq = depth_paren = 0
    buf: List[str] = []
    i = 0
    n = len(body)
    while i < n:
        c = body[i]
        if c in ("'", '"', "`"):
            quote = c
            buf.append(c)
            i += 1
            while i < n:
                buf.append(body[i])
                if body[i] == "\\":
                    if i + 1 < n:
                        buf.append(body[i + 1])
                    i += 2
                    continue
                if body[i] == quote:
                    i += 1
                    break
                i += 1
            continue
        if c == "{": depth_curly += 1
        elif c == "}": depth_curly -= 1
        elif c == "[": depth_sq += 1
        elif c == "]": depth_sq -= 1
        elif c == "(": depth_paren += 1
        elif c == ")": depth_paren -= 1
        if c == "," and depth_curly == depth_sq == depth_paren == 0:
            parts.append("".join(buf).strip())
            buf = []
        else:
            buf.append(c)
        i += 1
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)
    return parts


def _extract_field(body: str, field_name: str) -> Optional[Tuple[int, int, str]]:
    """Find `field_name:` at top level of an object literal body and return
    (value_start, value_end, value_src)."""
    n = len(body)
    pat = re.compile(rf"(^|[\s,{{]){re.escape(field_name)}\s*:", re.M)
    depth_curly = depth_sq = depth_paren = 0
    i = 0
    while i < n:
        c = body[i]
        if c in ("'", '"', "`"):
            quote = c; i += 1
            while i < n:
                if body[i] == "\\": i += 2; continue
                if body[i] == quote: i += 1; break
                i += 1
            continue
        if c == "{": depth_curly += 1
        elif c == "}": depth_curly -= 1
        elif c == "[": depth_sq += 1
        elif c == "]": depth_sq -= 1
        elif c == "(": depth_paren += 1
        elif c == ")": depth_paren -= 1
        if depth_curly == depth_sq == depth_paren == 0:
            m = pat.match(body, i)
            if m:
                val_start = m.end()
                while val_start < n and body[val_start] in " \t\r\n":
                    val_start += 1
                val_end = _find_value_end(body, val_start)
                return val_start, val_end, body[val_start:val_end].strip()
        i += 1
    return None


def _find_value_end(body: str, start: int) -> int:
    n = len(body)
    i = start
    depth_curly = depth_sq = depth_paren = 0
    while i < n:
        c = body[i]
        if c in ("'", '"', "`"):
            quote = c; i += 1
            while i < n:
                if body[i] == "\\": i += 2; continue
                if body[i] == quote: i += 1; break
                i += 1
            continue
        if c == "{": depth_curly += 1
        elif c == "}":
            if depth_curly == 0: return i
            depth_curly -= 1
        elif c == "[": depth_sq += 1
        elif c == "]":
            if depth_sq == 0: return i
            depth_sq -= 1
        elif c == "(": depth_paren += 1
        elif c == ")":
            if depth_paren == 0: return i
            depth_paren -= 1
        if c == "," and depth_curly == depth_sq == depth_paren == 0:
            return i
        i += 1
    return n


_JS_ESCAPES = {
    "\\n": "\n", "\\r": "\r", "\\t": "\t", "\\b": "\b", "\\f": "\f",
    "\\\\": "\\", "\\'": "'", "\\\"": "\"", "\\`": "`", "\\/": "/",
}


def _unescape_js(s: str) -> str:
    out: List[str] = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] == "\\" and i + 1 < n:
            pair = s[i:i + 2]
            if pair in _JS_ESCAPES:
                out.append(_JS_ESCAPES[pair])
                i += 2
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def _string_literal(s: str) -> Optional[str]:
    s = s.strip().rstrip(",").strip()
    if len(s) >= 2 and s[0] in ("'", '"', "`") and s[-1] == s[0]:
        return _unescape_js(s[1:-1])
    return None


def _string_array(s: str) -> List[str]:
    s = s.strip()
    if not (s.startswith("[") and s.endswith("]")):
        return []
    return [
        _string_literal(part) or part.strip()
        for part in _split_top_level_commas(s[1:-1])
        if part.strip()
    ]


def _decode_literal(s: str) -> Any:
    s = s.strip().rstrip(",").strip()
    if not s:
        return None
    lit = _string_literal(s)
    if lit is not None:
        return lit
    if s == "true": return True
    if s == "false": return False
    if s == "null" or s == "undefined": return None
    try: return int(s)
    except ValueError: pass
    try: return float(s)
    except ValueError: pass
    if s.startswith("[") and s.endswith("]"):
        return [_decode_literal(p) for p in _split_top_level_commas(s[1:-1])]
    return s


# ---------------------------------------------------------------------------
# Block parser
# ---------------------------------------------------------------------------

def _parse_properties(body: str) -> List[FOAMProperty]:
    out: List[FOAMProperty] = []
    if not (body.startswith("[") and body.endswith("]")):
        return out
    for part in _split_top_level_commas(body[1:-1]):
        part = part.strip()
        if not part:
            continue
        lit = _string_literal(part)
        if lit is not None:
            out.append(FOAMProperty(name=lit, raw=part))
            continue
        if part.startswith("{") and part.endswith("}"):
            inner = part[1:-1]
            name_f = _extract_field(inner, "name")
            class_f = _extract_field(inner, "class")
            value_f = _extract_field(inner, "value")
            factory_f = _extract_field(inner, "factory")
            expr_f = _extract_field(inner, "expression")
            if not name_f:
                continue
            prop = FOAMProperty(
                name=_string_literal(name_f[2]) or name_f[2].strip().rstrip(","),
                cls=_string_literal(class_f[2]) if class_f else None,
                value=_decode_literal(value_f[2]) if value_f else None,
                factory_src=factory_f[2] if factory_f else None,
                expression_src=expr_f[2] if expr_f else None,
                raw=part,
            )
            out.append(prop)
    return out


_FUNC_HEADER_RE = re.compile(r"function\s+([A-Za-z_$][\w$]*)?\s*\(([^)]*)\)")


def _parse_methods(body: str) -> List[FOAMMethod]:
    out: List[FOAMMethod] = []
    if not (body.startswith("[") and body.endswith("]")):
        return out
    for part in _split_top_level_commas(body[1:-1]):
        part = part.strip()
        if not part:
            continue
        m = _FUNC_HEADER_RE.match(part)
        if m and m.group(1):
            args = [a.strip() for a in m.group(2).split(",") if a.strip()]
            out.append(FOAMMethod(name=m.group(1), args=args, body_src=part, raw=part))
            continue
        if part.startswith("{") and part.endswith("}"):
            inner = part[1:-1]
            name_f = _extract_field(inner, "name")
            code_f = _extract_field(inner, "code")
            if not name_f:
                continue
            name = _string_literal(name_f[2]) or name_f[2].strip().rstrip(",")
            args: List[str] = []
            if code_f:
                fm = _FUNC_HEADER_RE.search(code_f[2])
                if fm:
                    args = [a.strip() for a in fm.group(2).split(",") if a.strip()]
            out.append(FOAMMethod(name=name, args=args, body_src=code_f[2] if code_f else "", raw=part))
    return out


def _parse_block(kind: str, body: str, source_file: Optional[str]) -> Optional[FOAMClass]:
    pkg = _extract_field(body, "package")
    name = _extract_field(body, "name")
    if not name:
        return None
    extends = _extract_field(body, "extends")
    implements = _extract_field(body, "implements")
    requires = _extract_field(body, "requires")
    imports = _extract_field(body, "imports")
    exports = _extract_field(body, "exports")
    flags = _extract_field(body, "flags")
    properties = _extract_field(body, "properties")
    methods = _extract_field(body, "methods")
    constants = _extract_field(body, "constants")

    cls = FOAMClass(
        package=(_string_literal(pkg[2]) if pkg else None),
        name=(_string_literal(name[2]) or name[2].strip().rstrip(",")),
        kind=kind,
        extends=(_string_literal(extends[2]) if extends else None),
        implements=_string_array(implements[2]) if implements else [],
        requires=_string_array(requires[2]) if requires else [],
        imports=_string_array(imports[2]) if imports else [],
        exports=_string_array(exports[2]) if exports else [],
        flags=_string_array(flags[2]) if flags else [],
        properties=_parse_properties(properties[2]) if properties else [],
        methods=_parse_methods(methods[2]) if methods else [],
        source_file=source_file,
    )

    if constants and constants[2].startswith("{") and constants[2].endswith("}"):
        inner = constants[2][1:-1]
        for part in _split_top_level_commas(inner):
            if ":" not in part:
                continue
            k, _, v = part.partition(":")
            cls.constants[k.strip()] = _decode_literal(v)

    return cls


def parse_foam_file(path: str) -> List[FOAMClass]:
    """Parse every foam.CLASS / foam.LIB / etc. block in a single JS file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    classes: List[FOAMClass] = []
    for m in _BLOCK_RE.finditer(src):
        body_start = m.end()
        body_end = _scan_balanced(src, body_start)
        if body_end < 0:
            continue
        body = src[body_start:body_end]
        cls = _parse_block(m.group(1), body, source_file=path)
        if cls is not None:
            classes.append(cls)
    return classes


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

class FOAM3Registry:
    """Indexed collection of parsed FOAM3 classes."""

    def __init__(self) -> None:
        self.classes: Dict[str, FOAMClass] = {}
        self.by_package: Dict[str, List[FOAMClass]] = {}
        self.errors: List[Tuple[str, Exception]] = []

    def add(self, cls: FOAMClass) -> None:
        self.classes[cls.id] = cls
        self.by_package.setdefault(cls.package or "", []).append(cls)

    def find(self, class_id: str) -> Optional[FOAMClass]:
        if class_id in self.classes:
            return self.classes[class_id]
        matches = [c for c in self.classes.values() if c.name == class_id]
        return matches[0] if len(matches) == 1 else None

    def subclasses_of(self, parent_id: str) -> List[FOAMClass]:
        return [c for c in self.classes.values() if c.extends == parent_id]

    def parse_file(self, path: str) -> int:
        try:
            classes = parse_foam_file(path)
        except Exception as e:
            self.errors.append((path, e))
            return 0
        for c in classes:
            self.add(c)
        return len(classes)

    def parse_directory(self, root: str, *, exclude: Iterable[str] = ()) -> int:
        excl = tuple(exclude)
        total = 0
        for dirpath, dirnames, filenames in os.walk(root):
            if any(part in dirpath.replace("\\", "/").split("/") for part in excl):
                continue
            for fn in filenames:
                if fn.endswith(".js"):
                    total += self.parse_file(os.path.join(dirpath, fn))
        return total

    def stats(self) -> Dict[str, int]:
        return {
            "classes": len(self.classes),
            "packages": len(self.by_package),
            "errors": len(self.errors),
        }


# ---------------------------------------------------------------------------
# Optional: invoke FOAM3 via Node.js
# ---------------------------------------------------------------------------

def node_available() -> bool:
    try:
        subprocess.run(["node", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def run_node_script(js_source: str, *, cwd: Optional[str] = None,
                    timeout: float = 30.0) -> str:
    """Run arbitrary JS through Node.js. The caller is responsible for any
    FOAM3 bootstrap (`require('./foam3/src/foam.js')` or equivalent)."""
    if not node_available():
        raise RuntimeError("node executable not found on PATH")
    proc = subprocess.run(
        ["node", "-e", js_source],
        capture_output=True, text=True, cwd=cwd, timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"node failed (exit {proc.returncode}): {proc.stderr}")
    return proc.stdout


# ---------------------------------------------------------------------------
# CLI / smoke test
# ---------------------------------------------------------------------------

def _demo() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    foam_src = os.path.join(here, "foam3", "src")
    if not os.path.isdir(foam_src):
        print(f"[skip] FOAM3 source not at {foam_src}")
        return

    reg = FOAM3Registry()
    sample = os.path.join(foam_src, "foam", "android", "tools", "GenResources.js")
    if os.path.isfile(sample):
        n = reg.parse_file(sample)
        print(f"parsed {n} block(s) from GenResources.js")
        for cls in reg.classes.values():
            print(f"  {cls.kind} {cls.id} extends={cls.extends!r}")
            for p in cls.properties:
                print(f"    prop  {p.name}  class={p.cls!r}  default={p.python_default()!r}")
            for mth in cls.methods:
                print(f"    meth  {mth.name}({', '.join(mth.args)})")

        for cls in list(reg.classes.values())[:1]:
            PyCls = cls.to_python_class()
            inst = PyCls()
            print(f"  python instance: {inst}")

    print("\n[scanning full src tree — this may take a moment]")
    reg2 = FOAM3Registry()
    reg2.parse_directory(foam_src)
    print("stats:", reg2.stats())
    examples = ["foam.dao.AbstractDAO", "foam.core.Property", "foam.u2.Element"]
    for cid in examples:
        c = reg2.find(cid)
        if c:
            print(f"  found {cid}: {len(c.properties)} props, "
                  f"{len(c.methods)} methods, source={os.path.basename(c.source_file or '')}")


if __name__ == "__main__":
    _demo()
