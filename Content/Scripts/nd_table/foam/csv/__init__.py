"""
foam3_py.csv — port of foam/lib/csv/.

Parsers (from the .java files in that directory):
    CSVNewlineParser        ``\\r\\n / \\r / \\n`` → ``\\n``
    CSVNormalStringParser   bare field (no ``"``, no ``\\``)
    CSVEscapeStringParser   ``"...""..."`` quoted field with ``""`` escapes
    CSVStringParser         Alt(normal, escaped)
    YYMMDDParser            ``YYYY-MM-DD`` or epoch millis → ``date``

Helpers:
    CSVSupport              header + row reader. Yields ``dict`` per row.
    CSVOutputter            row writer mirroring foam.lib.csv.CSVOutputterImpl
    read_rows               one-shot wrapper around CSVSupport
    write_rows              one-shot wrapper around CSVOutputter

Parsers take the delimiter via ``ParserContext`` key ``"csvDelimiter"`` (a
single-character string) — same convention as the Java code. Defaults to
``,``.
"""

from __future__ import annotations

import datetime
import io
from typing import Any, Dict, Iterable, Iterator, List, Optional as Opt

from ..parse import (
    AbstractLiteral, Alt, Parser, ParserContext, ParserContextImpl,
    PStream, ProxyParser, Seq, Seq1, StringPStream,
)
from ..json import IntParser, LongParser, NullParser


# ---------------------------------------------------------------------------
# Newline parser
# ---------------------------------------------------------------------------

class CSVNewlineParser(Parser):
    """Match any CRLF / CR / LF and normalise to ``\\n``."""

    _delegate = Alt(AbstractLiteral.create("\r\n"),
                    AbstractLiteral.create("\r"),
                    AbstractLiteral.create("\n"))

    def parse(self, ps, x):
        if ps is None:
            return None
        ps = ps.apply(self._delegate, x)
        if ps is None:
            return None
        return ps.setValue("\n")


# ---------------------------------------------------------------------------
# Field parsers (port of CSVNormalStringParser and CSVEscapeStringParser)
# ---------------------------------------------------------------------------

class CSVNormalStringParser(Parser):
    """Bare CSV field. Rejects ``"`` and bare backslashes (per Java code).
    Stops at the active delimiter; empty fields are valid."""

    _newline_parser = CSVNewlineParser()

    def __init__(self, delimiter: str = ",") -> None:
        self.delimiter_ = delimiter

    def parse(self, ps, x):
        if ps is None:
            return None
        active = self.delimiter_
        if x is not None:
            d = x.get("csvDelimiter")
            if d is not None:
                active = d
        buf: List[str] = []
        while ps.valid():
            head = ps.head()
            if head == '"':
                return None
            if head == "\\":
                if ps.apply(self._newline_parser, x) is None:
                    buf.append("\\\\")
                    ps = ps.tail()
                    continue
                else:
                    return None
            if head == active:
                break
            buf.append(head)
            ps = ps.tail()
        return ps.setValue("".join(buf))


class CSVEscapeStringParser(Parser):
    """Quoted CSV field. ``""`` inside the quoted body becomes a literal
    ``"``. Other special characters (``,``, ``\\n``, ``\\r``) are allowed
    unescaped."""

    ESCAPE = '"'
    _newline_parser = CSVNewlineParser()

    def __init__(self, delimiter: str = ",") -> None:
        self.delimiter_ = delimiter

    def parse(self, ps, x):
        if ps is None or not ps.valid():
            return None
        if ps.head() != self.ESCAPE:
            return None
        active = self.delimiter_
        if x is not None:
            d = x.get("csvDelimiter")
            if d is not None:
                active = d
        delim_count = 0
        buf: List[str] = []
        ps = ps.tail()
        while ps.valid():
            head = ps.head()
            if head == self.ESCAPE:
                if delim_count == 1:
                    buf.append(self.ESCAPE)
                    delim_count = 0
                else:
                    delim_count = 1
            elif head == active:
                if delim_count == 1:
                    break
                else:
                    delim_count = 0
                    buf.append(head)
            else:
                if delim_count == 1:
                    return None
                if head == "\\":
                    ps1 = ps.apply(self._newline_parser, x)
                    if ps1 is not None:
                        buf.append(ps1.value())
                        ps = ps1
                        delim_count = 0
                        continue
                    delim_count = 0
                    buf.append("\\\\")
                else:
                    delim_count = 0
                    buf.append(head)
            ps = ps.tail()
        if not ps.valid() and delim_count != 1:
            return None
        return ps.setValue("".join(buf))


class CSVStringParser(ProxyParser):
    """``Alt(CSVNormalStringParser, CSVEscapeStringParser)``."""

    _instance: Opt["CSVStringParser"] = None

    @classmethod
    def instance(cls) -> "CSVStringParser":
        if cls._instance is None:
            cls._instance = CSVStringParser()
        return cls._instance

    def __init__(self) -> None:
        super().__init__(Alt(CSVNormalStringParser(), CSVEscapeStringParser()))


class YYMMDDParser(ProxyParser):
    """Parse ``YYYY-MM-DD`` (3 ints separated by ``-``) or epoch milliseconds
    (a single long) into a ``datetime.date`` / ``datetime.datetime``. ``null``
    yields ``None``."""

    _instance: Opt["YYMMDDParser"] = None

    @classmethod
    def instance(cls) -> "YYMMDDParser":
        if cls._instance is None:
            cls._instance = YYMMDDParser()
        return cls._instance

    def __init__(self) -> None:
        super().__init__(Alt(
            NullParser.instance(),
            Seq(IntParser.instance(),
                AbstractLiteral.create("-"),
                IntParser.instance(),
                AbstractLiteral.create("-"),
                IntParser.instance()),
            LongParser.instance(),
        ))

    def parse(self, ps, x):
        ps = super().parse(ps, x)
        if ps is None:
            return None
        v = ps.value()
        if v is None:
            return ps.setValue(None)
        if isinstance(v, int):
            # Treat as epoch milliseconds (matches Java Date(long))
            return ps.setValue(
                datetime.datetime.fromtimestamp(v / 1000.0, tz=datetime.timezone.utc)
            )
        if isinstance(v, list):
            year, _, month, _, day = v
            return ps.setValue(datetime.date(year, month, day))
        return ps


# ---------------------------------------------------------------------------
# Row reader (port of CSVSupport.inputCSV)
# ---------------------------------------------------------------------------

class CSVSupport:
    """Stream CSV rows out of a file-like or string source.

    Unlike the Java port the Python version is generator-based and doesn't
    require an FObject class — it yields ``dict`` rows keyed by header name.
    Pass ``cls`` to instantiate a Python class instead.
    """

    def __init__(self, *, delimiter: str = ",") -> None:
        self.delimiter = delimiter

    def _parse_row(self, line: str) -> Opt[List[str]]:
        x = ParserContextImpl()
        x.set("csvDelimiter", self.delimiter)
        # Build a row parser that handles N comma-separated fields
        ps = StringPStream(line)
        cells: List[str] = []
        first = True
        delim_parser = AbstractLiteral.create(self.delimiter)
        field = CSVStringParser.instance()
        while True:
            if not first:
                ps2 = ps.apply(delim_parser, x)
                if ps2 is None:
                    break
                ps = ps2
            ps3 = ps.apply(field, x)
            if ps3 is None:
                break
            cells.append(ps3.value())
            ps = ps3
            first = False
        return cells

    def read_rows(self, source, *, cls=None) -> Iterator[Any]:
        """Yield ``dict`` (or ``cls`` instances) from a CSV source. ``source``
        may be a path, a file-like object, or a raw CSV string."""
        for header, row in self._iter_lines(source):
            data = dict(zip(header, row))
            if cls is None:
                yield data
            else:
                yield cls(**data)

    def _iter_lines(self, source):
        if hasattr(source, "read"):
            text = source.read()
        elif isinstance(source, str) and ("\n" in source or "," in source):
            text = source
        else:
            with open(source, "r", encoding="utf-8") as f:
                text = f.read()
        # Split on newlines but keep the parser tolerant of mixed CRLF
        lines = [ln for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n") if ln]
        if not lines:
            return
        header = self._parse_row(lines[0])
        if header is None:
            raise ValueError("CSV header parse failed")
        for ln in lines[1:]:
            row = self._parse_row(ln)
            if row is None:
                raise ValueError(f"CSV row parse failed: {ln!r}")
            # pad shorter rows with empty
            if len(row) < len(header):
                row += [""] * (len(header) - len(row))
            yield header, row


# ---------------------------------------------------------------------------
# Row writer (port of CSVOutputterImpl)
# ---------------------------------------------------------------------------

class CSVOutputter:
    """Build CSV text one row at a time. Mirrors ``CSVOutputterImpl`` —
    fields containing ``,`` ``"`` or newlines are double-quoted with embedded
    quotes doubled."""

    def __init__(self, *, delimiter: str = ",", line_terminator: str = "\n",
                 sheets_compatible: bool = False) -> None:
        self.delimiter = delimiter
        self.line_terminator = line_terminator
        self.sheets_compatible = sheets_compatible
        self.is_first_column = True
        self.is_first_row = True
        self._sb = io.StringIO()
        self._fields: Opt[List[str]] = None

    def output_value(self, value: Any) -> None:
        if not self.is_first_column:
            self._sb.write(self.delimiter)
        self.is_first_column = False
        self._output_value_raw(value)

    def _output_value_raw(self, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, datetime.datetime):
            if self.sheets_compatible:
                self._sb.write(value.strftime("%m/%d/%Y %I:%M:%S %p"))
            else:
                self._sb.write(value.isoformat())
            return
        if isinstance(value, datetime.date):
            self._sb.write(value.isoformat())
            return
        if isinstance(value, (list, tuple)):
            self._output_value_raw("|".join(str(v) for v in value))
            return
        if isinstance(value, bool):
            self._sb.write("true" if value else "false")
            return
        if isinstance(value, (int, float)):
            self._sb.write(str(value))
            return
        s = str(value)
        needs_quote = (self.delimiter in s) or ('"' in s) or ("\n" in s) or ("\r" in s)
        if needs_quote:
            self._sb.write('"')
            self._sb.write(s.replace('"', '""'))
            self._sb.write('"')
        else:
            self._sb.write(s)

    def newline(self) -> None:
        self._sb.write(self.line_terminator)
        self.is_first_column = True

    def output_header(self, fields: Iterable[str]) -> None:
        self._fields = list(fields)
        for name in self._fields:
            self.output_value(name)
        self.newline()
        self.is_first_row = False

    def output_row(self, row: Dict[str, Any]) -> None:
        if self.is_first_row:
            self.output_header(row.keys())
        assert self._fields is not None
        for name in self._fields:
            self.output_value(row.get(name))
        self.newline()

    def __str__(self) -> str:
        return self._sb.getvalue()

    def flush(self) -> str:
        return str(self)


# ---------------------------------------------------------------------------
# One-shot helpers
# ---------------------------------------------------------------------------

def read_rows(source, *, delimiter: str = ",", cls=None) -> List[Any]:
    """Parse a full CSV (path, string, or file-like) into a list of dicts (or
    ``cls`` instances)."""
    return list(CSVSupport(delimiter=delimiter).read_rows(source, cls=cls))


def write_rows(rows: Iterable[Dict[str, Any]], *, delimiter: str = ",",
               line_terminator: str = "\n") -> str:
    """Render a sequence of dict rows as a CSV string. Headers come from the
    first row's keys."""
    out = CSVOutputter(delimiter=delimiter, line_terminator=line_terminator)
    for row in rows:
        out.output_row(row)
    return str(out)


__all__ = [
    "CSVNewlineParser", "CSVNormalStringParser", "CSVEscapeStringParser",
    "CSVStringParser", "YYMMDDParser",
    "CSVSupport", "CSVOutputter", "read_rows", "write_rows",
]
