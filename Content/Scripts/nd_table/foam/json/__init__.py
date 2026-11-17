"""
foam3_py.json — port of foam/lib/json/*.java.

Parsers cover JSON's six structural characters, all primitive types, arrays,
maps, and FObject-style objects. The class names match the Java package
one-to-one (Whitespace, NullParser, BooleanParser, IntParser, LongParser,
FloatParser, DoubleParser, StringParser, UnicodeParser, ASCIIEscapeParser,
HexCharParser, ArrayParser, MapParser, AnyParser, KeyParser, AnyKeyParser,
KeyValueParser, IdentifierStartParser, ObjectNullParser).

The output side ports Util.escape and exposes a Python-friendly
JSONOutputter that mirrors JSONFObjectFormatter's flags
(outputShortNames, outputDefaultValues, multiLineOutput, outputClassNames,
quoteKeys). Top-level helpers ``loads`` / ``dumps`` make the round-trip
ergonomic from Python.
"""

from __future__ import annotations

import datetime
import io
from typing import Any, Iterable, List, Optional as Opt

from ..parse import (
    AbstractLiteral, Alt, AnyChar, Chars, Literal, LiteralIC, NotChars, Not,
    Optional, Parser, ParserContext, ParserContextImpl, ProxyParser, PStream,
    Range, Repeat, Repeat0, Seq, Seq0, Seq1, Seq2, StringPStream, Substring,
)


# ---------------------------------------------------------------------------
# Whitespace
# ---------------------------------------------------------------------------

class Whitespace(Parser):
    """RFC 4627 insignificant whitespace: ``\\x20 / \\t / \\r / \\n``."""

    _instance: Opt["Whitespace"] = None

    @classmethod
    def instance(cls) -> "Whitespace":
        if cls._instance is None:
            cls._instance = Whitespace()
        return cls._instance

    @staticmethod
    def wrap(p: Parser) -> Parser:
        return Seq1(1, Whitespace.instance(), p, Whitespace.instance())

    def parse(self, ps, x):
        while ps.valid():
            c = ps.head()
            if c == " " or c == "\t" or c == "\r" or c == "\n":
                ps = ps.tail()
            else:
                return ps
        return ps

    def __repr__(self) -> str:
        return "Whitespace"


# ---------------------------------------------------------------------------
# Hex/Unicode/ASCII escapes
# ---------------------------------------------------------------------------

class HexCharParser(ProxyParser):
    def __init__(self) -> None:
        super().__init__(Alt(Range.create("0", "9"),
                             Range.create("A", "F"),
                             Range.create("a", "f")))


class UnicodeParser(ProxyParser):
    """Parses ``\\uXXXX`` into a single char."""

    def __init__(self) -> None:
        super().__init__(Seq(Whitespace.instance(),
                             AbstractLiteral.create("\\"),
                             AbstractLiteral.create("u"),
                             Repeat(HexCharParser(), None, 4, 4)))

    def parse(self, ps, x):
        ps = super().parse(ps, x)
        if ps is None:
            return None
        values = ps.value()
        hex_seq = values[3]
        n = 0
        for h in hex_seq:
            c = h.upper() if "a" <= h <= "z" else h
            n = n * 16 + (ord(c) - ord("0") if c <= "9" else 10 + ord(c) - ord("A"))
        return ps.setValue(chr(n))


class ASCIIEscapeParser(ProxyParser):
    """Parses ``\\n \\t \\r \\f \\b \\\\`` into the corresponding char."""

    _MAP = {"\\": "\\", "n": "\n", "t": "\t", "r": "\r", "f": "\f", "b": "\b"}

    def __init__(self) -> None:
        super().__init__(Seq(
            Whitespace.instance(),
            AbstractLiteral.create("\\"),
            Alt(AbstractLiteral.create("\\"),
                AbstractLiteral.create("n"),
                AbstractLiteral.create("t"),
                AbstractLiteral.create("r"),
                AbstractLiteral.create("f"),
                AbstractLiteral.create("b"))))

    def parse(self, ps, x):
        ps = super().parse(ps, x)
        if ps is None:
            return None
        c = ps.value()[2]
        return ps.setValue(self._MAP.get(c, c))


# ---------------------------------------------------------------------------
# Primitive value parsers
# ---------------------------------------------------------------------------

class IntParser(Parser):
    """Optional minus + digits, bounded to Python int (Java caps at INT_MAX —
    we accept full Python int range since Python has no overflow)."""

    _instance: Opt["IntParser"] = None

    @classmethod
    def instance(cls) -> "IntParser":
        if cls._instance is None:
            cls._instance = IntParser()
        return cls._instance

    def parse(self, ps, x):
        if not ps.valid():
            return None
        negate = False
        c = ps.head()
        if c == "-":
            negate = True
            ps = ps.tail()
            if not ps.valid():
                return None
            c = ps.head()
        if not c.isdigit():
            return None
        n = int(c)
        ps = ps.tail()
        while ps.valid():
            c = ps.head()
            if c.isdigit():
                n = n * 10 + int(c)
                ps = ps.tail()
            else:
                break
        if negate:
            n = -n
        return ps.setValue(n)


class LongParser(IntParser):
    """In Java a distinct 64-bit parser; in Python Long == int."""

    _instance: Opt["LongParser"] = None

    @classmethod
    def instance(cls) -> "LongParser":
        if cls._instance is None:
            cls._instance = LongParser()
        return cls._instance


class DoubleParser(Parser):
    """JSON number with optional sign, fraction, and exponent. Returns
    Python float."""

    _instance: Opt["DoubleParser"] = None

    @classmethod
    def instance(cls) -> "DoubleParser":
        if cls._instance is None:
            cls._instance = DoubleParser()
        return cls._instance

    def parse(self, ps, x):
        buf: List[str] = []
        decimal_found = False
        exponent_found = False
        negative_exp = False

        if not ps.valid():
            return None
        c = ps.head()
        if c == "-":
            buf.append(c)
            ps = ps.tail()
            if not ps.valid():
                return None
            c = ps.head()
        if c.isdigit():
            buf.append(c)
        else:
            return None
        ps = ps.tail()
        prev = c
        while ps.valid():
            c = ps.head()
            if c.isdigit():
                buf.append(c)
            elif c == ".":
                if decimal_found or exponent_found:
                    return None
                decimal_found = True
                buf.append(c)
            elif c in ("E", "e"):
                if exponent_found:
                    return None
                exponent_found = True
                buf.append(c)
            elif c == "-":
                if negative_exp:
                    return None
                if prev in ("E", "e"):
                    negative_exp = True
                    buf.append(c)
                else:
                    break
            else:
                break
            prev = c
            ps = ps.tail()
        return ps.setValue(float("".join(buf)) if buf else None)


class FloatParser(DoubleParser):
    """Java has separate Float — Python only has one float type."""

    _instance: Opt["FloatParser"] = None

    @classmethod
    def instance(cls) -> "FloatParser":
        if cls._instance is None:
            cls._instance = FloatParser()
        return cls._instance


class BooleanParser(ProxyParser):
    """Match literal ``true`` or ``false``, returning Python bool."""

    _instance: Opt["BooleanParser"] = None

    @classmethod
    def instance(cls) -> "BooleanParser":
        if cls._instance is None:
            cls._instance = BooleanParser()
        return cls._instance

    def __init__(self) -> None:
        super().__init__(Alt(Literal("true", True), Literal("false", False)))


class NullParser:
    """Matches literal ``null``, value=None."""

    _instance: Opt[Parser] = None

    @classmethod
    def instance(cls) -> Parser:
        if cls._instance is None:
            cls._instance = Literal("null", None)
        return cls._instance


class StringParser(Parser):
    """Quoted string with ``"``, ``'``, ``\\``` or ``\"\"\"`` delimiters.
    Recognises ``\\uXXXX``, ``\\n`` etc. escape sequences."""

    _instance: Opt["StringParser"] = None
    ESCAPE = "\\"

    _delimiter_parser = Alt(
        Literal('"""', AbstractLiteral.create('"""')),
        Literal('"',   AbstractLiteral.create('"')),
        Literal("'",   AbstractLiteral.create("'")),
        Literal("`",   AbstractLiteral.create("`")),
    )

    @classmethod
    def instance(cls) -> "StringParser":
        if cls._instance is None:
            cls._instance = StringParser()
        return cls._instance

    def __init__(self) -> None:
        self._escape_parser = Alt(
            UnicodeParser(),
            ASCIIEscapeParser(),
            Seq1(1, AbstractLiteral.create(self.ESCAPE), AnyChar.instance()),
        )

    def parse(self, ps, x):
        ps = ps.apply(self._delimiter_parser, x)
        if ps is None:
            return None
        delimiter = ps.value()
        buf: List[str] = []
        escaping = False
        while ps.valid():
            if escaping:
                ps = ps.apply(self._escape_parser, x)
                if ps is None:
                    return None
                buf.append(ps.value())
                escaping = False
                continue
            result = ps.apply(delimiter, x)
            if result is not None:
                ps = result
                break
            c = ps.head()
            if c == self.ESCAPE:
                escaping = True
                continue
            buf.append(c)
            ps = ps.tail()
        return ps.setValue("".join(buf))


# ---------------------------------------------------------------------------
# Identifier + key parsers
# ---------------------------------------------------------------------------

class IdentifierStartParser(ProxyParser):
    def __init__(self) -> None:
        super().__init__(Alt(Range.create("A", "Z"), Range.create("a", "z"),
                             AbstractLiteral.create("_"),
                             AbstractLiteral.create("$")))


class KeyParser(Parser):
    """Matches either ``"key"`` or bare ``key``."""

    def __init__(self, key: str) -> None:
        self.delegate = Alt(AbstractLiteral.create(f'"{key}"'),
                            AbstractLiteral.create(key))

    def parse(self, ps, x):
        return ps.apply(self.delegate, x)


class AnyKeyParser(ProxyParser):
    """String literal or bare JS identifier."""

    def __init__(self) -> None:
        super().__init__(Alt(
            StringParser.instance(),
            Substring(Seq0(
                IdentifierStartParser(),
                Repeat0(Alt(Range.create("0", "9"),
                            IdentifierStartParser())),
            )),
        ))


class KeyValueParser(ProxyParser):
    """Parses ``key: value`` returning ``[key, value]`` (or just ``value`` if
    the key is fixed)."""

    def __init__(self, opt_key: Opt[str] = None,
                 opt_value_parser: Opt[Parser] = None) -> None:
        value_parser = opt_value_parser or AnyParser.instance()
        if opt_key is not None:
            super().__init__(Seq1(5,
                                  Whitespace.instance(),
                                  KeyParser(opt_key),
                                  Whitespace.instance(),
                                  AbstractLiteral.create(":"),
                                  Whitespace.instance(),
                                  value_parser))
        else:
            super().__init__(Seq2(1, 5,
                                  Whitespace.instance(),
                                  AnyKeyParser(),
                                  Whitespace.instance(),
                                  AbstractLiteral.create(":"),
                                  Whitespace.instance(),
                                  value_parser))


# ---------------------------------------------------------------------------
# Compound: ObjectNullParser / ArrayParser / MapParser / AnyParser
# ---------------------------------------------------------------------------

class ObjectNullParser(ProxyParser):
    """Tries NullParser, then the given object parser."""

    def __init__(self, object_parser: Parser) -> None:
        super().__init__(Alt(NullParser.instance(), object_parser))


class _LazyParser(Parser):
    """Defers resolution of a Parser singleton until parse-time. Mirrors the
    Java ``return instance__ == null ? new ProxyParser { getDelegate() {
    return instance__; } } : instance__;`` pattern that breaks circular
    references between AnyParser <-> ArrayParser <-> MapParser."""

    def __init__(self, resolver) -> None:
        self._resolver = resolver

    def parse(self, ps, x):
        return self._resolver().parse(ps, x)


class ArrayParser(ProxyParser):
    """``[ v, v, v ]``. Defaults to AnyParser for values."""

    _instance: Opt["ArrayParser"] = None
    _building = False

    @classmethod
    def instance(cls) -> Parser:
        if cls._instance is None:
            if cls._building:
                return _LazyParser(lambda: cls._instance)
            cls._building = True
            cls._instance = ArrayParser()
            cls._building = False
        return cls._instance

    def __init__(self, value_parser: Opt[Parser] = None) -> None:
        if value_parser is None:
            value_parser = AnyParser.instance()
        super().__init__(Seq1(3,
            Whitespace.instance(),
            AbstractLiteral.create("["),
            Whitespace.instance(),
            Repeat(value_parser,
                   Seq0(Whitespace.instance(),
                        AbstractLiteral.create(","),
                        Whitespace.instance())),
            Whitespace.instance(),
            AbstractLiteral.create("]"),
        ))

    def parse(self, ps, x):
        ps = super().parse(ps, x)
        if ps is None:
            return None
        # value is List from Repeat — already a Python list, so we're done
        return ps


class MapParser(ObjectNullParser):
    """``{ "k": v, ... }`` -> Python dict. Allows null sentinel."""

    _instance: Opt["MapParser"] = None
    _building = False

    @classmethod
    def instance(cls) -> Parser:
        if cls._instance is None:
            if cls._building:
                return _LazyParser(lambda: cls._instance)
            cls._building = True
            cls._instance = MapParser()
            cls._building = False
        return cls._instance

    def __init__(self) -> None:
        super().__init__(Seq1(3,
            Whitespace.instance(),
            AbstractLiteral.create("{"),
            Whitespace.instance(),
            Repeat(Seq2(1, 5,
                        Whitespace.instance(),
                        AnyKeyParser(),
                        Whitespace.instance(),
                        AbstractLiteral.create(":"),
                        Whitespace.instance(),
                        AnyParser.instance()),
                   Seq0(Whitespace.instance(),
                        AbstractLiteral.create(","))),
            Whitespace.instance(),
            AbstractLiteral.create("}"),
        ))

    def parse(self, ps, x):
        ps = super().parse(ps, x)
        if ps is None:
            return None
        v = ps.value()
        if v is None:
            return ps
        d = {}
        for item in v:
            d[item[0]] = item[1]
        return ps.setValue(d)


class AnyParser(ProxyParser):
    """Tries every primitive/compound parser in priority order. Singleton."""

    _instance: Opt["AnyParser"] = None
    _building = False

    @classmethod
    def instance(cls) -> Parser:
        if cls._instance is None:
            if cls._building:
                return _LazyParser(lambda: cls._instance)
            cls._building = True
            cls._instance = AnyParser()
            cls._building = False
        return cls._instance

    def __init__(self) -> None:
        # Build lazily because of circular reference w/ Array / Map.
        # ArrayParser.instance() returns the singleton; if we're in the
        # middle of constructing AnyParser, that singleton's instance is
        # still the one we're building. We assemble the Alt here directly.
        delegate = Alt(
            NullParser.instance(),
            StringParser.instance(),
            BooleanParser.instance(),
            # Long but only if no decimal / exponent
            Seq1(0, LongParser.instance(), Not(Chars("eE."))),
            DoubleParser.instance(),
            ArrayParser.instance(),
            MapParser.instance(),
        )
        super().__init__(delegate)


# ---------------------------------------------------------------------------
# Util.escape — JSON string escape function (Java port)
# ---------------------------------------------------------------------------

def escape(src: str) -> str:
    """Append-escape ``src`` for embedding in a JSON string. Matches
    ``foam.lib.json.Util.escape``: control chars become ``\\uXXXX``, the six
    special chars become ``\\t \\r \\n \\\\ \\"`` and printable ASCII passes
    through unchanged."""
    if not src:
        return ""
    out: List[str] = []
    start = 0
    for i, c in enumerate(src):
        if c == "\t":
            out.append(src[start:i]); out.append("\\t"); start = i + 1
        elif c == "\r":
            out.append(src[start:i]); out.append("\\r"); start = i + 1
        elif c == "\n":
            out.append(src[start:i]); out.append("\\n"); start = i + 1
        elif c == "\\":
            out.append(src[start:i]); out.append("\\\\"); start = i + 1
        elif c == '"':
            out.append(src[start:i]); out.append('\\"'); start = i + 1
        else:
            if c < " " or c > "~":
                out.append(src[start:i])
                out.append("\\u{:04x}".format(ord(c)))
                start = i + 1
    out.append(src[start:])
    return "".join(out)


# ---------------------------------------------------------------------------
# JSON outputter / loader  (Python-friendly facade)
# ---------------------------------------------------------------------------

class JSONOutputter:
    """Walks a Python value tree and emits FOAM-style JSON. The flags mirror
    JSONFObjectFormatter (multi-line mode, key-quoting, default-value
    filtering, class-name emission for tagged objects)."""

    def __init__(self, *, multi_line_output: bool = False,
                 quote_keys: bool = True,
                 output_short_names: bool = False,
                 output_default_values: bool = True,
                 output_class_names: bool = False,
                 indent: str = "  ") -> None:
        self.multi_line_output = multi_line_output
        self.quote_keys = quote_keys
        self.output_short_names = output_short_names
        self.output_default_values = output_default_values
        self.output_class_names = output_class_names
        self.indent = indent
        self._buf: List[str] = []
        self._depth = 0

    # core
    def output(self, value: Any) -> None:
        if value is None:
            self._buf.append("null")
        elif value is True:
            self._buf.append("true")
        elif value is False:
            self._buf.append("false")
        elif isinstance(value, str):
            self._buf.append('"'); self._buf.append(escape(value)); self._buf.append('"')
        elif isinstance(value, bool):  # never reached after True/False, kept for safety
            self._buf.append("true" if value else "false")
        elif isinstance(value, (int, float)):
            self._buf.append(repr(value) if isinstance(value, float)
                             else str(value))
        elif isinstance(value, (list, tuple)):
            self._output_array(value)
        elif isinstance(value, dict):
            self._output_map(value)
        elif isinstance(value, (datetime.datetime, datetime.date)):
            self._output_date(value)
        elif hasattr(value, "__dict__") or hasattr(value, "__dataclass_fields__"):
            self._output_fobject(value)
        else:
            # last-resort: stringify
            self._buf.append('"'); self._buf.append(escape(str(value))); self._buf.append('"')

    def _output_array(self, value: Iterable) -> None:
        self._buf.append("[")
        first = True
        for item in value:
            if not first:
                self._buf.append(",")
                self._nl()
            first = False
            self.output(item)
        self._buf.append("]")

    def _output_map(self, value: dict) -> None:
        self._buf.append("{")
        self._depth += 1
        first = True
        for k, v in value.items():
            if not first:
                self._buf.append(",")
            self._nl()
            self._output_key(str(k))
            self._buf.append(":")
            self.output(v)
            first = False
        self._depth -= 1
        if not first:
            self._nl()
        self._buf.append("}")

    def _output_fobject(self, value: Any) -> None:
        props = _fobject_properties(value, include_defaults=self.output_default_values)
        self._buf.append("{")
        self._depth += 1
        first = True
        if self.output_class_names:
            self._nl()
            self._output_key("class")
            self._buf.append(":")
            self._buf.append('"'); self._buf.append(escape(type(value).__name__))
            self._buf.append('"')
            first = False
        for name, val in props:
            if not first:
                self._buf.append(",")
            self._nl()
            self._output_key(name)
            self._buf.append(":")
            self.output(val)
            first = False
        self._depth -= 1
        if not first:
            self._nl()
        self._buf.append("}")

    def _output_key(self, k: str) -> None:
        if self.quote_keys:
            self._buf.append('"'); self._buf.append(escape(k)); self._buf.append('"')
        else:
            self._buf.append(k)

    def _output_date(self, value) -> None:
        if isinstance(value, datetime.datetime):
            v = value
        else:
            v = datetime.datetime(value.year, value.month, value.day)
        # ISO 8601 with milliseconds: yyyy-MM-ddTHH:mm:ss.SSSZ
        ms = v.microsecond // 1000
        s = v.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z"
        self._buf.append('"'); self._buf.append(s); self._buf.append('"')

    def _nl(self) -> None:
        if self.multi_line_output:
            self._buf.append("\n")
            self._buf.append(self.indent * self._depth)

    def reset(self) -> None:
        self._buf.clear()
        self._depth = 0

    def stringify(self, obj: Any) -> str:
        self.reset()
        self.output(obj)
        return "".join(self._buf)


def _fobject_properties(obj: Any, *, include_defaults: bool) -> List:
    """Yield (name, value) pairs for an FObject-ish Python object.
    Dataclasses use their declared fields; everything else falls back to
    ``vars(obj)`` filtered for non-underscore names."""
    if hasattr(obj, "__dataclass_fields__"):
        result = []
        for fname, f in obj.__dataclass_fields__.items():
            v = getattr(obj, fname)
            if not include_defaults:
                default = f.default
                if default is v or default == v:
                    continue
            result.append((fname, v))
        return result
    pairs: List = []
    for k, v in vars(obj).items():
        if k.startswith("_"):
            continue
        pairs.append((k, v))
    return pairs


def dumps(obj: Any, **kwargs) -> str:
    """Serialize ``obj`` to a JSON string with FOAM defaults."""
    return JSONOutputter(**kwargs).stringify(obj)


def dump(obj: Any, fp, **kwargs) -> None:
    fp.write(dumps(obj, **kwargs))


def loads(s: str) -> Any:
    """Parse ``s`` as JSON. Returns Python dict / list / str / int / float /
    bool / None."""
    ps = StringPStream(s)
    x = ParserContextImpl()
    parser = Seq1(1, Whitespace.instance(), AnyParser.instance(),
                  Whitespace.instance())
    result = ps.apply(parser, x)
    if result is None:
        raise ValueError("JSON parse failed")
    return result.value()


def load(fp) -> Any:
    return loads(fp.read())


__all__ = [
    "Whitespace", "HexCharParser", "UnicodeParser", "ASCIIEscapeParser",
    "IntParser", "LongParser", "FloatParser", "DoubleParser",
    "BooleanParser", "NullParser", "StringParser",
    "IdentifierStartParser", "KeyParser", "AnyKeyParser", "KeyValueParser",
    "ObjectNullParser", "ArrayParser", "MapParser", "AnyParser",
    "escape", "JSONOutputter", "dumps", "dump", "loads", "load",
]
