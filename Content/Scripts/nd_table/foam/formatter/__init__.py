"""
foam3_py.formatter — port of foam/lib/formatter/.

Two layers:

* ``AbstractFObjectFormatter`` — base class with the StringBuilder-like
  buffer, ``builder()`` / ``append()`` / ``maybe_append_comma()`` / ``reset``
  / ``stringify`` infrastructure shared by all formatters.
* ``JSONFObjectFormatter`` — production JSON emitter. Mirrors the Java class
  attribute-by-attribute: ``quote_keys``, ``output_short_names``,
  ``output_default_values``, ``multi_line_output``, ``output_class_names``,
  ``output_readable_dates``, ``output_default_class_names``.

The class accepts dicts, dataclasses, and ad-hoc Python objects (with
``__dict__``). Java's PropertyPredicate is represented as a callable
``(field_name) -> bool`` set via ``set_property_predicate``.
"""

from __future__ import annotations

import datetime
from typing import Any, Callable, Dict, Iterable, List, Optional as Opt

from ..json import escape


COMMA = ","


class FObjectFormatter:
    """Python equivalent of the Java FObjectFormatter interface. Subclasses
    implement ``output(value)`` and ``stringify(obj)``."""

    def reset(self) -> None: raise NotImplementedError
    def builder(self) -> List[str]: raise NotImplementedError
    def append(self, o: Any) -> List[str]: raise NotImplementedError
    def stringify(self, obj: Any) -> str: raise NotImplementedError
    def output(self, value: Any) -> None: raise NotImplementedError


class AbstractFObjectFormatter(FObjectFormatter):
    """Base for all FObject formatters. Owns the buffer + the property
    predicate + the cached property map."""

    def __init__(self, x: Any = None) -> None:
        self._x = x
        self._b: List[str] = []
        self._property_predicate: Opt[Callable[[str], bool]] = None
        self._property_cache: Dict[type, List[str]] = {}

    # ---- X context --------------------------------------------------------
    def set_x(self, x: Any) -> None:
        self._x = x
        self._property_cache.clear()

    def get_x(self) -> Any:
        return self._x

    # ---- buffer -----------------------------------------------------------
    def builder(self) -> List[str]:
        return self._b

    def append(self, o: Any) -> List[str]:
        self._b.append(str(o))
        return self._b

    def maybe_append_comma(self) -> List[str]:
        i = len(self._b) - 1
        # walk back past whitespace-only chunks
        while i >= 0:
            chunk = self._b[i]
            if chunk and not chunk.isspace():
                break
            i -= 1
        if i < 0:
            return self._b
        last = self._b[i][-1] if self._b[i] else ""
        if last == "{" or last == "[":
            return self._b
        return self.append(COMMA)

    def set_length(self, length: int) -> None:
        cur = sum(len(c) for c in self._b)
        if length >= cur:
            return
        # Truncate to `length` chars total
        kept: List[str] = []
        remaining = length
        for c in self._b:
            if remaining >= len(c):
                kept.append(c)
                remaining -= len(c)
            else:
                kept.append(c[:remaining])
                remaining = 0
                break
        self._b = kept

    def reset(self) -> None:
        self._b = []

    # ---- predicate --------------------------------------------------------
    def set_property_predicate(self, pred: Opt[Callable[[str], bool]]) -> None:
        self._property_predicate = pred
        self._property_cache.clear()

    def get_property_predicate(self) -> Opt[Callable[[str], bool]]:
        return self._property_predicate

    def _filter(self, name: str) -> bool:
        return self._property_predicate is None or self._property_predicate(name)

    # ---- string output ----------------------------------------------------
    def stringify(self, obj: Any) -> str:
        self.reset()
        self.output(obj)
        return "".join(self._b)

    def __str__(self) -> str:
        return "".join(self._b)


# ---------------------------------------------------------------------------
# JSONFObjectFormatter
# ---------------------------------------------------------------------------

class JSONFObjectFormatter(AbstractFObjectFormatter):
    """Port of foam/lib/formatter/JSONFObjectFormatter.java.

    Attribute names match the Java source one-for-one. All accept Boolean
    setters of the form ``set_<flag>(value)`` for Java-style fluent use, or
    you can construct with keyword args."""

    def __init__(self, x: Any = None, *,
                 quote_keys: bool = False,
                 output_short_names: bool = False,
                 output_default_values: bool = False,
                 multi_line_output: bool = False,
                 output_class_names: bool = True,
                 output_readable_dates: bool = False,
                 output_default_class_names: bool = True) -> None:
        super().__init__(x)
        self.quote_keys_ = quote_keys
        self.output_short_names_ = output_short_names
        self.output_default_values_ = output_default_values
        self.multi_line_output_ = multi_line_output
        self.output_class_names_ = output_class_names
        self.output_readable_dates_ = output_readable_dates
        self.output_default_class_names_ = output_default_class_names

    # ---- setters (mirror Java fluent API) ---------------------------------
    def set_quote_keys(self, v: bool) -> "JSONFObjectFormatter":
        self.quote_keys_ = v; return self
    def set_output_short_names(self, v: bool) -> "JSONFObjectFormatter":
        self.output_short_names_ = v; return self
    def set_output_default_values(self, v: bool) -> "JSONFObjectFormatter":
        self.output_default_values_ = v; return self
    def set_multi_line_output(self, v: bool) -> "JSONFObjectFormatter":
        self.multi_line_output_ = v; return self
    def set_output_class_names(self, v: bool) -> "JSONFObjectFormatter":
        self.output_class_names_ = v; return self
    def set_output_readable_dates(self, v: bool) -> "JSONFObjectFormatter":
        self.output_readable_dates_ = v; return self
    def set_output_default_class_names(self, v: bool) -> "JSONFObjectFormatter":
        self.output_default_class_names_ = v; return self

    # ---- primitives -------------------------------------------------------
    def output_string(self, s: str) -> None:
        if self.multi_line_output_ and "\n" in s:
            self.append("\n\"\"\"")
            self.escape_append(s)
            self.append("\"\"\"")
        else:
            self.append('"')
            self.escape_append(s)
            self.append('"')

    def escape_append(self, s: Opt[str]) -> None:
        if s is None:
            return
        self.append(escape(s))

    # ---- value dispatcher -------------------------------------------------
    def output(self, value: Any, default_class: Opt[type] = None) -> None:
        if value is None:
            self.append("null")
            return
        if isinstance(value, str):
            self.output_string(value)
            return
        if isinstance(value, bool):
            self.append("true" if value else "false")
            return
        if isinstance(value, int):
            self.append(value)
            return
        if isinstance(value, float):
            self.append(repr(value))
            return
        if isinstance(value, datetime.datetime):
            self.output_date(value)
            return
        if isinstance(value, datetime.date):
            self.output_date(datetime.datetime(value.year, value.month, value.day))
            return
        if isinstance(value, (list, tuple)):
            self.output_array(value)
            return
        if isinstance(value, dict):
            self.output_map(value)
            return
        # Otherwise: an FObject-shaped Python object
        self.output_fobject(value, default_class)

    # ---- collections ------------------------------------------------------
    def output_array(self, array: Iterable) -> None:
        self.append("[")
        first = True
        for item in array:
            if not first:
                self.append(COMMA)
            first = False
            self.output(item)
        self.append("]")

    def output_map(self, m: Dict) -> None:
        self.append("{")
        first = True
        for k, v in m.items():
            if not first:
                self.append(COMMA)
            first = False
            self.output_string("" if k is None else str(k))
            self.append(":")
            self.output(v)
        self.append("}")

    def output_date(self, value: datetime.datetime) -> None:
        if self.output_readable_dates_:
            ms = value.microsecond // 1000
            iso = value.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z"
            self.append('"'); self.append(iso); self.append('"')
        else:
            # milliseconds since epoch (matches Java FastTimestamper default)
            ts = int(value.timestamp() * 1000)
            self.append(ts)

    # ---- FObject ----------------------------------------------------------
    def output_fobject(self, obj: Any, default_class: Opt[type] = None) -> None:
        self.append("{")
        first = True

        if self.output_class_names_:
            same_as_default = default_class is type(obj)
            if (not same_as_default) or self.output_default_class_names_:
                self._output_key("class")
                self.append(":")
                self.output_string(type(obj).__name__)
                first = False

        for name in self._properties(obj):
            value = self._get_property(obj, name)
            if not self.output_default_values_ and _is_default(obj, name, value):
                continue
            if not first:
                self.append(COMMA)
            if self.multi_line_output_:
                self.append("\n")
            first = False
            self._output_key(self._property_name(obj, name))
            self.append(":")
            self.output(value)
        self.append("}")

    def _output_key(self, name: str) -> None:
        if self.quote_keys_:
            self.append('"'); self.append(escape(name)); self.append('"')
        else:
            self.append(name)

    # ---- introspection ----------------------------------------------------
    def _properties(self, obj: Any) -> List[str]:
        cls = type(obj)
        cached = self._property_cache.get(cls)
        if cached is not None:
            return cached
        if hasattr(obj, "__dataclass_fields__"):
            names = list(obj.__dataclass_fields__.keys())
        else:
            names = [k for k in vars(obj).keys() if not k.startswith("_")]
        names = [n for n in names if self._filter(n)]
        self._property_cache[cls] = names
        return names

    def _get_property(self, obj: Any, name: str) -> Any:
        return getattr(obj, name)

    def _property_name(self, obj: Any, name: str) -> str:
        if self.output_short_names_:
            short_map = getattr(obj, "json_short_names", None)
            if isinstance(short_map, dict) and name in short_map:
                return short_map[name]
        return name


def _is_default(obj: Any, name: str, value: Any) -> bool:
    if hasattr(obj, "__dataclass_fields__"):
        f = obj.__dataclass_fields__.get(name)
        if f is None:
            return False
        try:
            return value == f.default
        except Exception:
            return False
    return False


__all__ = [
    "FObjectFormatter",
    "AbstractFObjectFormatter",
    "JSONFObjectFormatter",
    "COMMA",
]
