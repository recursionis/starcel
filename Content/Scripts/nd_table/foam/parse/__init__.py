"""
foam3_py.parse — port of foam/lib/parse/*.java.

The Java framework is a backtracking parser-combinator library. Each parser
implements ``parse(ps: PStream, x: ParserContext) -> PStream | None``: on
success it returns an advanced ``PStream`` whose ``value()`` carries the
parsed value; on failure it returns ``None``. ``PStream`` is immutable —
``tail()`` returns a new stream, ``setValue(v)`` returns a copy with a new
value, so backtracking is automatic (you keep the old stream).

This module exposes the same class names as the Java package so call-sites
translate directly:

    from foam3_py.parse import (
        # streams
        StringPStream, ParserContextImpl, Reference,
        # atoms
        AnyChar, Literal, LiteralIC, Range, Chars, NotChar, NotChars, EOF, Fail,
        # combinators
        Alt, GreedyAlt, Seq, Seq0, Seq1, Seq2, SeqI,
        Optional, Not, Repeat, Repeat0,
        # composed
        ProxyParser, Substring, Join, Quoted, Until, Until0,
        UntilLiteral, UntilLiteral0,
    )
"""

from __future__ import annotations

from typing import Any, List, Optional as Opt, Sequence


# ---------------------------------------------------------------------------
# Reference (mutable wrapper, matches foam.lib.parse.Reference<T>)
# ---------------------------------------------------------------------------

class Reference:
    """Mutable single-value cell. Shared between StringPStream copies so all
    children of one root stream see the same source string."""

    __slots__ = ("_v",)

    def __init__(self, value: Any = None) -> None:
        self._v = value

    def get(self) -> Any:
        return self._v

    def set(self, value: Any) -> None:
        self._v = value


# ---------------------------------------------------------------------------
# Parser / PStream / ParserContext (the three Java interfaces)
# ---------------------------------------------------------------------------

class Parser:
    """Base parser class. Subclasses override ``parse``."""

    def parse(self, ps: "PStream", x: "ParserContext") -> Opt["PStream"]:
        raise NotImplementedError


class PStream:
    """Immutable token stream. See StringPStream for the concrete impl."""

    def head(self) -> str:                   raise NotImplementedError
    def valid(self) -> bool:                  raise NotImplementedError
    def tail(self) -> "PStream":              raise NotImplementedError
    def value(self) -> Any:                   raise NotImplementedError
    def setValue(self, v: Any) -> "PStream":  raise NotImplementedError
    def pos(self) -> int:                     raise NotImplementedError
    def substring(self, end: "PStream") -> str: raise NotImplementedError

    def apply(self, parser: Parser, x: "ParserContext") -> Opt["PStream"]:
        return parser.parse(self, x)


class ParserContext:
    def get(self, key: str) -> Any:               raise NotImplementedError
    def set(self, key: str, value: Any) -> None:  raise NotImplementedError
    def sub(self) -> "ParserContext":             raise NotImplementedError


class ParserContextImpl(ParserContext):
    """Variable bag with lexical-style parent chaining (port of
    ParserContextImpl.java). ``sub()`` returns a child whose ``get`` falls
    back to its parent's bindings."""

    def __init__(self) -> None:
        self._map: dict = {}
        self._parent: Opt[ParserContext] = None

    def get(self, key: str) -> Any:
        if key in self._map:
            return self._map[key]
        if self._parent is not None:
            return self._parent.get(key)
        return None

    def set(self, key: str, value: Any) -> None:
        self._map[key] = value

    def sub(self) -> "ParserContextImpl":
        child = ParserContextImpl()
        child._parent = self
        return child


# ---------------------------------------------------------------------------
# StringPStream (port of foam/lib/parse/StringPStream.java)
# ---------------------------------------------------------------------------

class StringPStream(PStream):
    """Immutable stream over an in-memory string. ``tail()`` is cached, so
    repeated backtracking from the same position doesn't reallocate."""

    __slots__ = ("str", "_pos", "_value", "_tail")

    def __init__(self, s=None, pos: int = 0, value: Any = None) -> None:
        if isinstance(s, Reference):
            self.str = s
        elif s is None:
            self.str = Reference()
        else:
            self.str = Reference(s)
        self._pos = pos
        self._value = value
        self._tail: Opt[StringPStream] = None

    def setString(self, s: str) -> None:
        self.str.set(s)

    def head(self) -> str:
        return self.str.get()[self._pos]

    def valid(self) -> bool:
        src = self.str.get()
        return src is not None and self._pos < len(src)

    def tail(self) -> "StringPStream":
        if self._tail is None:
            self._tail = StringPStream(self.str, self._pos + 1)
        return self._tail

    def value(self) -> Any:
        return self._value

    def setValue(self, v: Any) -> "StringPStream":
        return StringPStream(self.str, self._pos, v)

    def pos(self) -> int:
        return self._pos

    def substring(self, end: PStream) -> str:
        return self.str.get()[self._pos:end.pos()]

    def __repr__(self) -> str:
        src = self.str.get() or ""
        return f"StringPStream(pos={self._pos}, head={src[self._pos:self._pos+8]!r})"


# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------

class AnyChar(Parser):
    """Matches any single character. Singleton via ``AnyChar.instance()``."""

    _instance: Opt["AnyChar"] = None

    @classmethod
    def instance(cls) -> "AnyChar":
        if cls._instance is None:
            cls._instance = AnyChar()
        return cls._instance

    def parse(self, ps, x):
        if ps.valid():
            return ps.tail().setValue(ps.head())
        return None


class EOF(Parser):
    """Matches end-of-input only. Singleton via ``EOF.instance()``."""

    _instance: Opt["EOF"] = None

    @classmethod
    def instance(cls) -> "EOF":
        if cls._instance is None:
            cls._instance = EOF()
        return cls._instance

    def parse(self, ps, x):
        return None if ps.valid() else ps


class Fail(Parser):
    """Always fails. Used as a sentinel parser."""

    def parse(self, ps, x):
        return None


class AbstractLiteral(Parser):
    """Match an exact string. ``Literal.create(s)`` uses a multiton cache so
    the same string yields the same parser instance (port of
    AbstractLiteral.java)."""

    _cache: dict = {}

    def __init__(self, s: Opt[str]) -> None:
        self.string_ = s

    @classmethod
    def create(cls, s: Opt[str]) -> Parser:
        if s is None:
            # Java returns a parser that always fails by returning value None
            inst = AbstractLiteral(None)
            return inst
        if s in cls._cache:
            return cls._cache[s]
        inst = _LiteralStr(s)
        cls._cache[s] = inst
        return inst

    def getString(self) -> Opt[str]:
        return self.string_

    def parse(self, ps, x):
        if self.string_ is None:
            return None
        s = self.string_
        for i in range(len(s)):
            if not ps.valid() or ps.head() != s[i]:
                return None
            ps = ps.tail()
        return ps.setValue(self.value())

    def value(self) -> Any:
        return None

    def __repr__(self) -> str:
        return f"Literal({self.string_!r})"


class _LiteralStr(AbstractLiteral):
    """AbstractLiteral whose ``value()`` is the matched string itself.
    Returned by ``AbstractLiteral.create``."""

    def value(self) -> Any:
        return self.string_


_UNSET = object()


class Literal(AbstractLiteral):
    """Match exact string ``s`` and set the parser value to ``v``. When ``v``
    is omitted the value defaults to ``s`` itself; pass ``v=None`` explicitly
    to make the parser produce ``None`` (used by NullParser)."""

    def __init__(self, s: str, v: Any = _UNSET) -> None:
        super().__init__(s)
        self._value = s if v is _UNSET else v

    def value(self) -> Any:
        return self._value


class LiteralIC(Literal):
    """Case-insensitive Literal. Stores the uppercased pattern and compares
    against ``head().upper()`` (matches Java Character.toUpperCase)."""

    def __init__(self, s: str, v: Any = _UNSET) -> None:
        super().__init__(s.upper(), s if v is _UNSET else v)

    def parse(self, ps, x):
        s = self.string_
        for i in range(len(s)):
            if not ps.valid() or ps.head().upper() != s[i]:
                return None
            ps = ps.tail()
        return ps.setValue(self._value)

    def __repr__(self) -> str:
        return f"LiteralIC({self.string_!r}, {self._value!r})"


class Range(Parser):
    """Match any char ``c`` with ``from_ <= c <= to_``. Multiton via
    ``Range.create(from_, to_)``."""

    _cache: dict = {}

    def __init__(self, from_: str, to_: str) -> None:
        self.from_ = from_
        self.to_ = to_

    @classmethod
    def create(cls, from_: str, to_: str) -> "Range":
        key = (from_, to_)
        if key in cls._cache:
            return cls._cache[key]
        inst = Range(from_, to_)
        cls._cache[key] = inst
        return inst

    def parse(self, ps, x):
        if ps.valid():
            c = ps.head()
            if self.from_ <= c <= self.to_:
                return ps.tail().setValue(c)
        return None

    def __repr__(self) -> str:
        return f"Range({self.from_}-{self.to_})"


class Chars(Parser):
    """Match any char in the given alphabet string."""

    def __init__(self, s: str) -> None:
        self.chars_ = s

    def parse(self, ps, x):
        if ps.valid() and ps.head() in self.chars_:
            return ps.tail().setValue(ps.head())
        return None


class NotChar(Parser):
    """Match any char that is NOT the given one."""

    def __init__(self, c: str) -> None:
        self.c_ = c

    def parse(self, ps, x):
        if ps.valid() and ps.head() != self.c_:
            return ps.tail().setValue(ps.head())
        return None


class NotChars(Parser):
    """Match any char not in the given alphabet string."""

    def __init__(self, s: str) -> None:
        self.chars_ = s

    def parse(self, ps, x):
        if ps.valid() and ps.head() not in self.chars_:
            return ps.tail().setValue(ps.head())
        return None


# ---------------------------------------------------------------------------
# Combinators
# ---------------------------------------------------------------------------

class Alt(Parser):
    """First-match alternative. Tries each parser in order; returns the first
    success, ``None`` if all fail."""

    def __init__(self, *parsers: Parser) -> None:
        if len(parsers) == 1 and isinstance(parsers[0], (list, tuple)):
            parsers = tuple(parsers[0])
        self.parsers_: tuple = parsers

    def parse(self, ps, x):
        for p in self.parsers_:
            ret = ps.apply(p, x)
            if ret is not None:
                return ret
        return None


class GreedyAlt(Parser):
    """Greedy alternative — tries every branch, returns the one that consumed
    the most characters (port of GreedyAlt.java)."""

    def __init__(self, *parsers: Parser) -> None:
        if len(parsers) == 1 and isinstance(parsers[0], (list, tuple)):
            parsers = tuple(parsers[0])
        self.parsers_: tuple = parsers

    def parse(self, ps, x):
        best_pos = 0
        best: Opt[PStream] = None
        for p in self.parsers_:
            ret = ps.apply(p, x)
            if ret is not None and ret.pos() > best_pos:
                best_pos = ret.pos()
                best = ret
        return best


class Seq(Parser):
    """Sequence. Returns ``[v0, v1, ..., vN]`` of all sub-parser values; fails
    if any sub-parser fails."""

    def __init__(self, *parsers: Parser) -> None:
        if len(parsers) == 1 and isinstance(parsers[0], (list, tuple)):
            parsers = tuple(parsers[0])
        self.parsers_: tuple = parsers

    def parse(self, ps, x):
        values: List[Any] = [None] * len(self.parsers_)
        for i, p in enumerate(self.parsers_):
            ps = ps.apply(p, x)
            if ps is None:
                return None
            values[i] = ps.value()
        return ps.setValue(values)


class Seq0(Parser):
    """Sequence that discards values; preserves the final ``PStream`` only."""

    def __init__(self, *parsers: Parser) -> None:
        self.parsers_: tuple = parsers

    def parse(self, ps, x):
        for p in self.parsers_:
            ps = ps.apply(p, x)
            if ps is None:
                return None
        return ps


class Seq1(Parser):
    """Sequence returning only the value at position ``index``."""

    def __init__(self, index: int, *parsers: Parser) -> None:
        self.index = index
        self.parsers: tuple = parsers

    def parse(self, ps, x):
        value: Any = None
        for i, p in enumerate(self.parsers):
            ps = ps.apply(p, x)
            if ps is None:
                return None
            if i == self.index:
                value = ps.value()
        return ps.setValue(value)


class Seq2(Parser):
    """Sequence returning ``[values[i], values[j]]``."""

    def __init__(self, i: int, j: int, *parsers: Parser) -> None:
        self.index1 = i
        self.index2 = j
        self.parsers: tuple = parsers

    def parse(self, ps, x):
        value = [None, None]
        for i, p in enumerate(self.parsers):
            ps = ps.apply(p, x)
            if ps is None:
                return None
            if i == self.index1:
                value[0] = ps.value()
            if i == self.index2:
                value[1] = ps.value()
        return ps.setValue(value)


class SeqI(Parser):
    """Sequence returning values at the specified indices."""

    def __init__(self, indices: Sequence[int], *parsers: Parser) -> None:
        self.indices = list(indices)
        self.parsers: tuple = parsers

    def parse(self, ps, x):
        value: List[Any] = [None] * len(self.indices)
        for i, p in enumerate(self.parsers):
            ps = ps.apply(p, x)
            if ps is None:
                return None
            for j, idx in enumerate(self.indices):
                if i == idx:
                    value[j] = ps.value()
        return ps.setValue(value)


class Optional(Parser):
    """Match ``p`` if possible; on failure return the original stream with
    value=None (never fails)."""

    def __init__(self, p: Parser) -> None:
        self.p_ = p

    def parse(self, ps, x):
        ret = ps.apply(self.p_, x)
        if ret is not None:
            return ret
        return ps.setValue(None)


class Not(Parser):
    """Negative lookahead: succeed (without consuming) iff ``p`` fails. If
    ``else_p`` is set, apply it on success."""

    def __init__(self, p: Parser, else_p: Opt[Parser] = None) -> None:
        self.p_ = p
        self.elseP_ = else_p

    def parse(self, ps, x):
        if ps.apply(self.p_, x) is not None:
            return None
        if self.elseP_ is None:
            return ps
        return ps.apply(self.elseP_, x)


class Repeat(Parser):
    """Greedy 1+ (or ``[min, max]``) repetition with optional delimiter.
    Returns a Python ``list`` of values (Java returns ``Object[]``)."""

    def __init__(self, parser: Parser, delim_or_min=None, minimum: int = -1,
                 maximum: int = -1) -> None:
        if isinstance(delim_or_min, str):
            delim_or_min = AbstractLiteral.create(delim_or_min)
        if isinstance(delim_or_min, int):
            minimum = delim_or_min
            delim_or_min = None
        self.p = parser
        self.delim = delim_or_min
        self.min = minimum
        self.max = maximum

    def parse(self, ps, x):
        values: List[Any] = []
        i = 0
        while self.max == -1 or i < self.max:
            if self.delim is not None and values:
                result = ps.apply(self.delim, x)
                if result is None:
                    break
            else:
                result = ps
            result = result.apply(self.p, x)
            if result is None:
                break
            values.append(result.value())
            ps = result
            i += 1
        if self.min != -1 and len(values) < self.min:
            return None
        return ps.setValue(values)


class Repeat0(Parser):
    """Like Repeat but discards values. Returns the advanced ``PStream`` with
    its previous value untouched."""

    def __init__(self, parser: Parser, delim_or_min=None, minimum: int = -1,
                 maximum: int = -1) -> None:
        if isinstance(delim_or_min, str):
            delim_or_min = AbstractLiteral.create(delim_or_min)
        if isinstance(delim_or_min, int):
            minimum = delim_or_min
            delim_or_min = None
        self.p = parser
        self.delim = delim_or_min
        self.min = minimum
        self.max = maximum

    def parse(self, ps, x):
        first = True
        i = 0
        while self.max == -1 or i < self.max:
            if self.delim is not None and not first:
                result = ps.apply(self.delim, x)
                if result is None:
                    break
                ps = result
            result = ps.apply(self.p, x)
            if result is None:
                break
            ps = result
            first = False
            i += 1
        if self.min != -1 and i < self.min:
            return None
        return ps


# ---------------------------------------------------------------------------
# Composed: ProxyParser, Substring, Join, Quoted, Until, Until0
# ---------------------------------------------------------------------------

class ProxyParser(Parser):
    """Wraps a delegate parser. Subclasses override ``parse`` to add behaviour
    around the delegate."""

    def __init__(self, delegate: Parser) -> None:
        self.delegate_ = delegate

    def parse(self, ps, x):
        return self.delegate_.parse(ps, x)


class Substring(ProxyParser):
    """Run delegate, then replace its value with the source substring it
    consumed (Java: ``Substring.java``)."""

    def parse(self, ps, x):
        start = ps
        ps = super().parse(ps, x)
        if ps is not None:
            return ps.setValue(start.substring(ps))
        return ps


class Join(Parser):
    """Run delegate, then flatten its (possibly nested) ``Object[]`` result
    into a single string (recursively concatenating non-null leaves)."""

    def __init__(self, d: Parser) -> None:
        self.d_ = d

    def parse(self, ps, x):
        ps = ps.apply(self.d_, x)
        if ps is None:
            return None
        parts: List[str] = []
        self._append(parts, ps.value())
        return ps.setValue("".join(parts))

    def _append(self, parts: List[str], o: Any) -> None:
        if o is None:
            return
        if isinstance(o, (list, tuple)):
            for item in o:
                self._append(parts, item)
        else:
            parts.append(str(o))


class Quoted(Parser):
    """Wraps inner so it accepts both bare and double-quoted forms (Java's
    Quoted.java). Used for JSON dates whose underlying grammar is delimiter
    free but wire form is quoted."""

    def __init__(self, inner: Parser) -> None:
        self.inner_ = inner

    def parse(self, ps, x):
        open_ = ps.apply(AbstractLiteral.create("\""), x)
        if open_ is not None:
            val = open_.apply(self.inner_, x)
            if val is None:
                return None
            close_ = val.apply(AbstractLiteral.create("\""), x)
            if close_ is None:
                return None
            return close_.setValue(val.value())
        return ps.apply(self.inner_, x)


class UntilLiteral(Parser):
    """Optimized: ``Until(Literal(s))`` — scans via ``str.find`` when the
    stream is a StringPStream. Returns ``list[str]`` of chars before the
    terminator and consumes the terminator."""

    def __init__(self, literal: str) -> None:
        self.literal_ = literal

    def parse(self, ps, x):
        if isinstance(ps, StringPStream):
            return self._parse_fast(ps)
        return self._parse_generic(ps, x)

    def _parse_fast(self, ps: StringPStream) -> Opt[PStream]:
        src = ps.str.get()
        idx = src.find(self.literal_, ps.pos())
        if idx < 0:
            return None
        chars = list(src[ps.pos():idx])
        return StringPStream(ps.str, idx + len(self.literal_), chars)

    def _parse_generic(self, ps, x):
        lit = AbstractLiteral.create(self.literal_)
        delegate = Seq1(0, Repeat(Not(lit, AnyChar.instance())), lit)
        return delegate.parse(ps, x)


class UntilLiteral0(Parser):
    """Discarding variant of UntilLiteral — fast indexOf, value=None."""

    def __init__(self, literal: str) -> None:
        self.literal_ = literal

    def parse(self, ps, x):
        if isinstance(ps, StringPStream):
            src = ps.str.get()
            idx = src.find(self.literal_, ps.pos())
            if idx < 0:
                return None
            return StringPStream(ps.str, idx + len(self.literal_), None)
        # generic
        lit = AbstractLiteral.create(self.literal_)
        while True:
            res = ps.apply(lit, x)
            if res is not None:
                return res.setValue(None)
            if not ps.valid():
                return None
            ps = ps.tail()


class Until(Parser):
    """Match anything up to ``until`` (exclusive), consume ``until``. Returns
    ``list[str]`` of chars before the terminator. When ``until`` is an
    AbstractLiteral, delegates to UntilLiteral for O(n) scan."""

    def __init__(self, until: Parser) -> None:
        if isinstance(until, AbstractLiteral) and until.getString() is not None:
            self.delegate_ = UntilLiteral(until.getString())
        else:
            self.delegate_ = Seq1(0,
                                  Repeat(Not(until, AnyChar.instance())),
                                  until)

    def parse(self, ps, x):
        return self.delegate_.parse(ps, x)


class Until0(Parser):
    """Discarding Until — consumes through the terminator, value=None."""

    def __init__(self, until: Parser) -> None:
        self.until_ = until
        if isinstance(until, AbstractLiteral) and until.getString() is not None:
            self.optimized_: Opt[Parser] = UntilLiteral0(until.getString())
        else:
            self.optimized_ = None

    def parse(self, ps, x):
        if self.optimized_ is not None:
            return self.optimized_.parse(ps, x)
        while True:
            res = ps.apply(self.until_, x)
            if res is not None:
                return res.setValue(None)
            if not ps.valid():
                return None
            ps = ps.tail()


__all__ = [
    "Reference", "Parser", "PStream", "ParserContext", "ParserContextImpl",
    "StringPStream",
    "AnyChar", "EOF", "Fail",
    "AbstractLiteral", "Literal", "LiteralIC",
    "Range", "Chars", "NotChar", "NotChars",
    "Alt", "GreedyAlt", "Seq", "Seq0", "Seq1", "Seq2", "SeqI",
    "Optional", "Not", "Repeat", "Repeat0",
    "ProxyParser", "Substring", "Join", "Quoted",
    "Until", "Until0", "UntilLiteral", "UntilLiteral0",
]
