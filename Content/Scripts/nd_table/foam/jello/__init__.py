"""
foam3_py.jello — integrate codereport/jello via the parse combinators.

Jello (https://github.com/codereport/jello) is a Python wrapper around the
Jelly programming language. It maps human-readable keywords (``abs``,
``head``, ``rev``, ``fold``, …) to Jelly's Unicode atoms (``A``, ``Ḣ``,
``Ṛ``, ``/``, …) and pipes the result through the ``jelly`` executable.

This subpackage sits between ``foam3_py.parse`` and ``foam3_py.json`` because
its tokenizer is built out of the parse combinators — keyword expressions are
parsed by a real PStream-driven grammar rather than a regex split. That
lets the jello grammar compose with any other foam3_py grammar (you can
embed jello chains inside FOAM3 JSON, CSV cells, etc.).

Layered API:

    translate(keyword_expr)         keyword string → Jelly atom string
    keyword_arity(kw)               classify a keyword (0/1/2/quick/sep/array)
    is_jelly_available()            True iff jelly binary is reachable
    set_jelly_path(path)            point at a non-PATH jelly install
    run_jelly(atom_expr, *args)     subprocess invocation
    evaluate(keyword_expr, *args)   translate + run
    JelloFormula                    callable wrapper for nd_table cells
    install_into_table(table)       register JELLY()/jello()/jelly() in cells

Tokenizer grammar (built with foam3_py.parse):

    Token  := ParenOpen | ParenClose | NiladArray | Keyword
    Expr   := Whitespace? (Token Whitespace?)*

    Keyword     := IdentifierChar+
    NiladArray  := [-0-9,\\[\\]]+
    Whitespace  := (\\x20|\\t|\\r|\\n)+

``run_jelly`` honours the ``JELLY_BIN`` environment variable and the
``set_jelly_path`` override, so the user doesn't have to put ``jelly`` on
PATH for the integration to work.
"""

from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Sequence

from ..parse import (
    AbstractLiteral, Alt, Chars, Literal, NotChars, Parser, ParserContext,
    ParserContextImpl, PStream, Repeat, Repeat0, Seq, Seq0, Seq1, StringPStream,
    Substring,
)


# ---------------------------------------------------------------------------
# Lazy import of jello's `tokens` and `utils` modules from the vendored
# clone at ../nd_table/jello/src — without modifying jello's source tree.
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))

_JELLO_CANDIDATES = [
    # foam3_py is at .../Scripts/foam3_py/jello; jello is at .../Scripts/nd_table/jello/src
    os.path.normpath(os.path.join(_HERE, "..", "..", "nd_table", "jello", "src")),
    # Allow override via env var
    os.environ.get("JELLO_SRC", ""),
]

_tokens = None
_utils = None
_import_error: Optional[BaseException] = None
_jello_src_used: Optional[str] = None


def _ensure_jello_loaded() -> None:
    """Lazily import jello.tokens + jello.utils. Caches success and failure
    so we don't retry on every call."""
    global _tokens, _utils, _import_error, _jello_src_used
    if _tokens is not None and _utils is not None:
        return
    if _import_error is not None:
        raise _import_error

    for candidate in _JELLO_CANDIDATES:
        if candidate and os.path.isdir(candidate):
            if candidate not in sys.path:
                sys.path.insert(0, candidate)
            try:
                _tokens = importlib.import_module("tokens")
                _utils = importlib.import_module("utils")
                _jello_src_used = candidate
                return
            except Exception:
                continue

    _import_error = ImportError(
        "jello source not found. Looked in: "
        + ", ".join(repr(c) for c in _JELLO_CANDIDATES if c)
        + ". Set $JELLO_SRC to the directory containing tokens.py."
    )
    raise _import_error


# ---------------------------------------------------------------------------
# Public lookup helpers
# ---------------------------------------------------------------------------

def jello_source_dir() -> Optional[str]:
    """Return the directory we imported jello.tokens / jello.utils from."""
    _ensure_jello_loaded()
    return _jello_src_used


def monadic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded(); return dict(_tokens.monadic)


def dyadic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded(); return dict(_tokens.dyadic)


def niladic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded(); return dict(_tokens.niladic)


def quick_atoms() -> Dict[str, str]:
    _ensure_jello_loaded(); return dict(_tokens.quick)


def separator_atoms() -> Dict[str, str]:
    _ensure_jello_loaded(); return dict(_tokens.separators)


def all_keywords() -> List[str]:
    _ensure_jello_loaded()
    return sorted(set(_tokens.monadic) | set(_tokens.dyadic)
                  | set(_tokens.niladic) | set(_tokens.quick)
                  | set(_tokens.separators))


# ---------------------------------------------------------------------------
# Combinator grammar
# ---------------------------------------------------------------------------
#
# We build a real foam3_py.parse grammar instead of regex-splitting. The
# tokenizer is:
#
#   whitespace = Repeat0(Chars(" \t\r\n"))
#   paren      = Chars("()")
#   nilad_char = Chars("-0123456789,[]")
#   nilad_arr  = Substring(Repeat(nilad_char, 1))
#   ident_char = NotChars(" \t\r\n()")
#   ident      = Substring(Repeat(ident_char, 1))
#   token      = paren | nilad_arr | ident
#   expr       = whitespace + Repeat(token + whitespace)
#
# nilad_arr is tried before ident so "[1,2,3]" is captured as one token;
# Substring turns the matched span into a string for downstream lookup.

_WS_CHARS = " \t\r\n"
_NILAD_CHARS = "-0123456789,[]"

_whitespace = Repeat0(Chars(_WS_CHARS))
_paren = Substring(Chars("()"))
_nilad_arr = Substring(Repeat(Chars(_NILAD_CHARS), 1))
_ident = Substring(Repeat(NotChars(_WS_CHARS + "()"), 1))
_token = Alt(_paren, _nilad_arr, _ident)
_expr = Seq1(1, _whitespace, Repeat(_token, _whitespace))


def _tokenize(keyword_expr: str) -> List[str]:
    """Run the combinator grammar and return the parsed token list. Raises
    ``ValueError`` if the input doesn't fully tokenize."""
    _ensure_jello_loaded()
    ps = StringPStream(keyword_expr)
    x = ParserContextImpl()
    res = ps.apply(_expr, x)
    if res is None:
        raise ValueError(f"failed to tokenize Jello expression: {keyword_expr!r}")
    # The grammar tolerates trailing whitespace; ensure no non-whitespace remains.
    tail = res.apply(_whitespace, x)
    if tail is None or tail.valid():
        raise ValueError(f"unexpected trailing input in: {keyword_expr!r}")
    return list(res.value())


def is_nilad_array(s: str) -> bool:
    """A literal array like ``[1,2,3]`` — passed through unchanged."""
    return bool(s) and all(c in _NILAD_CHARS for c in s)


def to_jelly_atom(token: str) -> str:
    """Translate a single token to its Jelly atom. Raises ``KeyError`` for
    unknown tokens."""
    _ensure_jello_loaded()
    if token in ("(", ")"):
        return token
    for table in (_tokens.monadic, _tokens.dyadic, _tokens.niladic,
                  _tokens.quick, _tokens.separators):
        if token in table:
            return table[token]
    if is_nilad_array(token):
        return token
    raise KeyError(f"{token!r} is not a Jello keyword")


def translate(keyword_expr: str) -> str:
    """Tokenize via combinators, then concatenate Jelly atoms."""
    return "".join(to_jelly_atom(t) for t in _tokenize(keyword_expr))


def keyword_arity(kw: str) -> int:
    """Arity code for a keyword: 0/1/2 (nilad/monad/dyad), -3 (quick),
    -10 (each), -50 (flip c), -20 (separator .), -21 (separator :).
    Mirrors jello.py's Quick/Separator enum values."""
    _ensure_jello_loaded()
    if kw in _tokens.niladic:   return 0
    if kw in _tokens.monadic:   return 1
    if kw in _tokens.dyadic:    return 2
    if kw == "each":            return -10
    if kw == "c":               return -50
    if kw in _tokens.quick:     return -3
    if kw == ".":               return -20
    if kw == ":":               return -21
    if is_nilad_array(kw):      return 0
    raise KeyError(f"{kw!r} arity unknown")


# ---------------------------------------------------------------------------
# Execution layer
# ---------------------------------------------------------------------------

_JELLY_BIN: Optional[str] = None    # cached
_JELLY_OVERRIDE: Optional[str] = None  # set via set_jelly_path


def set_jelly_path(path: Optional[str]) -> None:
    """Override jelly discovery. Pass ``None`` to clear and re-probe PATH."""
    global _JELLY_BIN, _JELLY_OVERRIDE
    _JELLY_OVERRIDE = path
    _JELLY_BIN = None  # force re-probe on next call


def _probe_jelly() -> Optional[str]:
    if _JELLY_OVERRIDE:
        return _JELLY_OVERRIDE if os.path.isfile(_JELLY_OVERRIDE) else None
    env = os.environ.get("JELLY_BIN", "")
    if env and os.path.isfile(env):
        return env
    hit = shutil.which("jelly")
    if hit:
        return hit
    # Common Windows install locations to try as a fallback. Each is
    # checked verbatim; missing paths are silently skipped.
    candidates = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     "Programs", "Python", "Python39", "Scripts", "jelly.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""),
                     "Programs", "Python", "Python39", "Scripts", "jelly.bat"),
        os.path.join(os.environ.get("APPDATA", ""),
                     "Python", "Python39", "Scripts", "jelly.exe"),
        os.path.join(os.environ.get("USERPROFILE", ""),
                     "scoop", "shims", "jelly.exe"),
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    return None


def jelly_path() -> Optional[str]:
    """Return the path to the ``jelly`` executable, or None."""
    global _JELLY_BIN
    if _JELLY_BIN is None:
        _JELLY_BIN = _probe_jelly() or ""
    return _JELLY_BIN or None


def is_jelly_available() -> bool:
    return jelly_path() is not None


def run_jelly(atom_expr: str, *args: Any, timeout: float = 30.0) -> str:
    """Pipe ``atom_expr`` (Jelly atoms) through ``jelly eun``. Raises
    ``RuntimeError`` if the binary isn't found, ``CalledProcessError`` on
    non-zero exit."""
    binary = jelly_path()
    if binary is None:
        raise RuntimeError(
            "jelly executable not found. Set $JELLY_BIN or call "
            "set_jelly_path(...) with the full path to your jelly install."
        )
    cmd = [binary, "eun", atom_expr, *[str(a) for a in args]]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          check=True, timeout=timeout)
    return proc.stdout.strip()


def evaluate(keyword_expr: str, *args: Any, timeout: float = 30.0) -> str:
    return run_jelly(translate(keyword_expr), *args, timeout=timeout)


# ---------------------------------------------------------------------------
# JelloFormula + nd_table wiring
# ---------------------------------------------------------------------------

class JelloFormula:
    """Callable for embedding in any formula evaluator. Returns the jelly
    stdout when the binary is available; otherwise returns a dict describing
    the translation (useful for tests and translation-only environments)."""

    def __init__(self, *, translation_only: bool = False,
                 timeout: float = 30.0) -> None:
        self.translation_only = translation_only
        self.timeout = timeout

    def __call__(self, expr: str, *args: Any) -> Any:
        atoms = translate(expr)
        if self.translation_only or not is_jelly_available():
            return {"atoms": atoms, "args": list(args),
                    "executed": False,
                    "reason": "translation_only=True" if self.translation_only
                              else "jelly not available"}
        return run_jelly(atoms, *args, timeout=self.timeout)


_SIDE_NS: Dict[int, Dict[str, Any]] = {}


def formula_namespace_for(table: Any) -> Dict[str, Any]:
    """Get-or-create the per-table extra-context dict."""
    ns = getattr(table, "_formula_namespace", None)
    if ns is None:
        ns = _SIDE_NS.get(id(table))
    if ns is None:
        ns = {}
        try:
            setattr(table, "_formula_namespace", ns)
        except AttributeError:
            _SIDE_NS[id(table)] = ns
    return ns


def _wrap_formula_context(table: Any) -> None:
    """Idempotently patch ``table._get_formula_context`` so the returned
    namespace is merged with ``formula_namespace_for(table)`` before the
    cell formula is eval'd."""
    if getattr(table, "_jello_patched", False):
        return
    if not hasattr(table, "_get_formula_context"):
        setattr(table, "_jello_patched", True)
        return

    original = table._get_formula_context

    def patched(*args, **kwargs):
        ctx = original(*args, **kwargs)
        extra = formula_namespace_for(table)
        if extra:
            ctx.update(extra)
        return ctx

    try:
        table._get_formula_context = patched  # type: ignore[assignment]
    except AttributeError:
        cls = type(table)
        if not getattr(cls, "_jello_class_patched", False):
            cls_original = cls._get_formula_context
            def cls_patched(self_, *a, **kw):
                ctx = cls_original(self_, *a, **kw)
                extra = formula_namespace_for(self_)
                if extra:
                    ctx.update(extra)
                return ctx
            cls._get_formula_context = cls_patched  # type: ignore[assignment]
            cls._jello_class_patched = True  # type: ignore[attr-defined]
    setattr(table, "_jello_patched", True)


def install_into_table(table: Any, *, name: str = "JELLY",
                       translation_only: bool = False,
                       timeout: float = 30.0,
                       also: Sequence[str] = ("jello", "jelly")) -> "JelloFormula":
    """Register ``JELLY(expr, *args)`` (and the aliases ``jello`` / ``jelly``)
    as callables visible to cell formula ``eval``. The hook is idempotent,
    instance-scoped, and works with any Table whose formula engine exposes
    ``_get_formula_context``."""
    formula = JelloFormula(translation_only=translation_only, timeout=timeout)
    ns = formula_namespace_for(table)
    for n in (name, *also):
        ns[n] = formula
    _wrap_formula_context(table)
    return formula


# ---------------------------------------------------------------------------
# JelloExpr — value type that travels through foam3_py.json / formatter /
# csv / xml / html and ndtable_zarr without losing identity.
# ---------------------------------------------------------------------------

import dataclasses as _dc


@_dc.dataclass
class JelloExpr:
    """A serializable Jello expression.

    Fields:
        keyword_expr  the source keyword string, e.g. "abs neg"
        atoms         the translated Jelly atoms (cached for round-trips)
        args          optional positional args bound at construction
        last_result   optional last execution result (informational)

    Why a dataclass: foam3_py.json.JSONOutputter and
    foam3_py.formatter.JSONFObjectFormatter already serialize dataclasses by
    walking ``__dataclass_fields__``, so this class round-trips through both
    layers with no codec registration. ``from_dict`` reverses
    ``foam3_py.json.loads``.
    """

    keyword_expr: str = ""
    atoms: str = ""
    args: Optional[List[Any]] = None
    last_result: Optional[str] = None

    # Tag used by ``from_dict`` to distinguish a serialized JelloExpr from a
    # bare dict that happens to have the same field names.
    _CLASS_TAG = "JelloExpr"

    def __post_init__(self) -> None:
        if not self.atoms and self.keyword_expr:
            # Translate on construction so serialized form is self-contained.
            try:
                self.atoms = translate(self.keyword_expr)
            except (KeyError, ValueError):
                # Defer validation — invalid keywords are caught at eval()
                self.atoms = ""

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "JelloExpr":
        """Inverse of ``foam3_py.json.loads(dumps(jello_expr))``. Accepts
        either the bare-keys form or the tagged form (with ``"class"`` key).
        """
        if d.get("class") and d["class"] != cls._CLASS_TAG:
            raise ValueError(f"expected {cls._CLASS_TAG}, got {d['class']!r}")
        return cls(
            keyword_expr=d.get("keyword_expr", ""),
            atoms=d.get("atoms", ""),
            args=list(d["args"]) if d.get("args") is not None else None,
            last_result=d.get("last_result"),
        )

    def eval(self, *override_args: Any, timeout: float = 30.0) -> Any:
        """Run this expression. ``override_args`` replace ``self.args``
        when provided; otherwise the stored args are used. The result is
        cached on ``last_result`` for the next serialization."""
        args = list(override_args) if override_args else (self.args or [])
        atoms = self.atoms or translate(self.keyword_expr)
        if not is_jelly_available():
            self.last_result = None
            return {"atoms": atoms, "args": list(args),
                    "executed": False, "reason": "jelly not available"}
        out = run_jelly(atoms, *args, timeout=timeout)
        self.last_result = out
        return out

    def __repr__(self) -> str:
        return (f"JelloExpr(keyword_expr={self.keyword_expr!r}, "
                f"atoms={self.atoms!r}, args={self.args!r})")


def is_jello_expr_dict(d: Any) -> bool:
    """True iff ``d`` looks like a serialized ``JelloExpr`` (has the class
    tag, or has the keyword_expr+atoms shape)."""
    if not isinstance(d, dict):
        return False
    if d.get("class") == JelloExpr._CLASS_TAG:
        return True
    return "keyword_expr" in d and "atoms" in d


def revive(value: Any) -> Any:
    """Walk a Python value tree and revive any embedded JelloExpr dicts to
    actual JelloExpr instances. Useful right after ``foam3_py.json.loads``."""
    if isinstance(value, list):
        return [revive(v) for v in value]
    if isinstance(value, dict):
        if is_jello_expr_dict(value):
            return JelloExpr.from_dict(value)
        return {k: revive(v) for k, v in value.items()}
    return value


# ---------------------------------------------------------------------------
# Register a JelloExpr codec with ndtable_zarr so that a Table cell whose
# raw_value is a JelloExpr survives the Zarr round-trip as a JelloExpr (not
# as a repr() string). The registration is best-effort: if ndtable_zarr
# isn't importable (e.g. running foam3_py on its own), we silently skip.
# ---------------------------------------------------------------------------

def _register_zarr_codec_for_jello_expr() -> bool:
    """Idempotent. Returns True if registration succeeded.

    Two import strategies, in order:

    1. Add ``nd_table/`` to ``sys.path`` and import ``ndtable_zarr`` directly
       — bypasses ``nd_table/__init__.py`` (which can fail on machines
       without the UnrealEnginePython runtime).
    2. Whatever ``import_module("ndtable_zarr")`` finds via the current
       ``sys.path`` — covers the case where the user has arranged their
       own path layout.

    We catch ``BaseException`` here because a broken ``nd_table/__init__.py``
    can raise ``SyntaxError`` (not just ``ImportError``) and we never want a
    failed auto-registration to break ``import foam3_py.jello``.
    """
    mod = None

    # Strategy 1: direct path import from foam3_py/jello → Content/Scripts/nd_table/.
    try:
        scripts_dir = os.path.normpath(os.path.join(_HERE, "..", ".."))
        nd_table_dir = os.path.join(scripts_dir, "nd_table")
        if os.path.isdir(nd_table_dir) and nd_table_dir not in sys.path:
            sys.path.insert(0, nd_table_dir)
        mod = importlib.import_module("ndtable_zarr")
    except BaseException:
        mod = None

    # Strategy 2: package-style fallback if Strategy 1 left mod=None.
    if mod is None:
        try:
            mod = importlib.import_module("nd_table.ndtable_zarr")
        except BaseException:
            mod = None

    if mod is None or not hasattr(mod, "register_codec"):
        return False
    try:
        mod.register_codec(
            tag=JelloExpr._CLASS_TAG,
            predicate=lambda v: isinstance(v, JelloExpr),
            encode=lambda v: _dc.asdict(v),
            decode=lambda payload: JelloExpr.from_dict(payload or {}),
        )
        return True
    except BaseException:
        return False


# Auto-register on import. The result is exposed for tests / diagnostics.
_zarr_codec_registered: bool = _register_zarr_codec_for_jello_expr()


def ensure_zarr_codec_registered() -> bool:
    """Public retry hook — call this if ``foam3_py.jello`` was imported
    before ``ndtable_zarr`` was reachable, then ``ndtable_zarr`` became
    importable later (e.g. you added ``nd_table/`` to ``sys.path``)."""
    global _zarr_codec_registered
    if not _zarr_codec_registered:
        _zarr_codec_registered = _register_zarr_codec_for_jello_expr()
    return _zarr_codec_registered


__all__ = [
    "monadic_atoms", "dyadic_atoms", "niladic_atoms",
    "quick_atoms", "separator_atoms", "all_keywords",
    "is_nilad_array", "to_jelly_atom", "translate",
    "keyword_arity", "jello_source_dir",
    "set_jelly_path", "jelly_path", "is_jelly_available",
    "run_jelly", "evaluate",
    "JelloFormula", "install_into_table", "formula_namespace_for",
    "JelloExpr", "is_jello_expr_dict", "revive",
    "ensure_zarr_codec_registered",
]
