"""
foam3_py.html — port of foam/lib/html/Outputter.java.

Render Python objects into HTML table rows. Mirrors the Java semantics:

* ``output_start_table()`` / ``output_end_table()`` wrap a ``<table border="1">``.
* ``output_head(obj)`` writes the ``<thead><tr><th>...`` header row.
* ``output_fobject(obj)`` writes a ``<tr><td col=N>value</td>...</tr>`` body row.
* Empty cells emit ``&nbps;`` *(yes, with the same typo the Java code has —
  set ``preserve_java_typo=False`` to switch to the correct ``&nbsp;``)*.
* Strings inside cells are escaped with the Java rule
  ``s.replace("\\n","\\\\n").replace("\\"", "\\\\\\"")`` plus HTML entity escaping
  for ``< > &``.

The ``mode`` flag matches XML's OutputterMode (FULL / NETWORK / STORAGE).
"""

from __future__ import annotations

import datetime
import enum
import io
from typing import Any, Iterable, List, Optional as Opt, Sequence

from ..xml import OutputterMode, _all_property_names, _get_field, _transient_for_mode


class Outputter:
    """HTML table outputter (port of foam/lib/html/Outputter.java)."""

    def __init__(self, *, mode: OutputterMode = OutputterMode.FULL,
                 output_headers: bool = True,
                 nbsp_enabled: bool = True,
                 preserve_java_typo: bool = True) -> None:
        self.mode_ = mode
        self.output_headers_ = output_headers
        self.is_headers_output_ = False
        self.nbsp_enabled_ = nbsp_enabled
        self._nbsp = "&nbps;" if preserve_java_typo else "&nbsp;"
        self._sb = io.StringIO()

    # ---- shell ------------------------------------------------------------
    def output_start_html(self) -> None:
        self._sb.write("<html><head></head><body>")

    def output_end_html(self) -> None:
        self._sb.write("</body></html>")

    def output_start_table(self) -> None:
        self._sb.write('<table border="1">')

    def output_end_table(self) -> None:
        self._sb.write("</table>")

    def output_nbsp(self) -> None:
        if self.nbsp_enabled_:
            self._sb.write(self._nbsp)

    # ---- header ------------------------------------------------------------
    def output_head(self, obj: Any) -> None:
        self._sb.write("<thead><tr>")
        for name in self._property_names(obj):
            self._sb.write("<th>")
            self._sb.write(_html_escape(name))
            self._sb.write("</th>")
        self._sb.write("</tr></thead>")
        self.is_headers_output_ = True

    # ---- body row ---------------------------------------------------------
    def output_fobject(self, obj: Any) -> None:
        self._sb.write("<tr>")
        for j, name in enumerate(self._property_names(obj), start=1):
            self._sb.write(f'<td col={j}>')
            try:
                self.output(_get_field(obj, name))
            except Exception:
                self.output_nbsp()
                self._sb.write("<!-- error -->")
            self._sb.write("</td>")
        self._sb.write("</tr>")

    # ---- value dispatch ---------------------------------------------------
    def output(self, value: Any) -> None:
        if value is None:
            self.output_nbsp()
            return
        if isinstance(value, str):
            if not value:
                self.output_nbsp()
                return
            self._sb.write(_html_escape(_java_escape(value)))
            return
        if isinstance(value, bool):
            self._sb.write("true" if value else "false")
            return
        if isinstance(value, (int, float)):
            self._sb.write(str(value))
            return
        if isinstance(value, datetime.datetime):
            ms = value.microsecond // 1000
            self._sb.write(value.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z")
            return
        if isinstance(value, datetime.date):
            self._sb.write(value.isoformat())
            return
        if isinstance(value, enum.Enum):
            self._sb.write(value.name)
            return
        # Fallback: stringify
        self._sb.write(_html_escape(str(value)))

    # ---- helpers ----------------------------------------------------------
    def _property_names(self, obj: Any) -> List[str]:
        skip = set(_transient_for_mode(obj, self.mode_))
        return [n for n in _all_property_names(obj) if n not in skip]

    def stringify(self, obj: Any) -> str:
        self._sb = io.StringIO()
        if self.output_headers_ and not self.is_headers_output_:
            self.output_start_table()
            self.output_head(obj)
            self.output_fobject(obj)
            self.output_end_table()
        else:
            self.output_fobject(obj)
        return self._sb.getvalue()

    def stringify_rows(self, rows: Iterable[Any]) -> str:
        self._sb = io.StringIO()
        self.output_start_table()
        rows = list(rows)
        if rows and self.output_headers_:
            self.output_head(rows[0])
        for r in rows:
            self.output_fobject(r)
        self.output_end_table()
        return self._sb.getvalue()

    def __str__(self) -> str:
        return self._sb.getvalue()


_HTML_ESCAPES = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}


def _html_escape(s: str) -> str:
    return "".join(_HTML_ESCAPES.get(c, c) for c in s)


def _java_escape(s: str) -> str:
    """Java code's escape(): replace ``\\n`` -> ``\\\\n`` and ``"`` -> ``\\"``."""
    return s.replace("\n", "\\n").replace('"', '\\"')


def stringify(obj: Any, **kwargs) -> str:
    """One-shot ``Outputter(**kwargs).stringify(obj)``."""
    return Outputter(**kwargs).stringify(obj)


def stringify_rows(rows: Iterable[Any], **kwargs) -> str:
    return Outputter(**kwargs).stringify_rows(rows)


__all__ = ["Outputter", "stringify", "stringify_rows"]
