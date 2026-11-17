"""
foam3_py.xml — port of foam/lib/xml/Outputter.java.

Walk a Python value tree and emit XML in the FOAM convention:

* Each object becomes ``<ClassName ...attrs>...children...</ClassName>``.
* Properties marked as XML attributes (see ``xml_attribute_names`` below) are
  emitted as ``name="value"`` inside the opening tag.
* Other properties become nested ``<name>value</name>`` elements.
* Plain values (str/int/float/bool/date) are emitted directly inside the
  element they belong to.

The Java code calls ``PropertyInfo.getXMLAttribute()`` to decide attribute vs
element. Python has no equivalent introspection, so:

* For a ``dict`` value, the optional key ``"_xml_attrs"`` lists attribute
  field names; everything else becomes a child element.
* For an object, set the class attribute ``xml_attribute_names = (...)``.

There are also ``OutputterMode``-style ``mode`` filters for excluding
properties whose names appear in ``transient_for_mode``.
"""

from __future__ import annotations

import datetime
import enum
import io
from typing import Any, Iterable, List, Optional as Opt, Sequence


class OutputterMode(enum.Enum):
    FULL = "FULL"
    NETWORK = "NETWORK"
    STORAGE = "STORAGE"
    EXTERNAL = "EXTERNAL"


class Outputter:
    """XML outputter. Constructor flags mirror the Java class — call
    ``stringify(obj)`` for a one-shot string, or ``output(...)`` repeatedly
    against a streaming buffer."""

    _ISO_FMT = "%Y-%m-%dT%H:%M:%S.{ms:03d}Z"

    def __init__(self, *, mode: OutputterMode = OutputterMode.FULL,
                 output_short_names: bool = False,
                 output_default_values: bool = False) -> None:
        self.mode_ = mode
        self.output_short_names_ = output_short_names
        self.output_default_values_ = output_default_values
        self._sb = io.StringIO()

    # --------------------------------------------------------------- dispatch
    def output(self, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, str):
            self._output_string(value)
        elif isinstance(value, bool):
            self._output_boolean(value)
        elif isinstance(value, (int, float)):
            self._output_number(value)
        elif isinstance(value, (datetime.datetime, datetime.date)):
            self._output_date(value)
        elif isinstance(value, enum.Enum):
            self._output_enum(value)
        elif isinstance(value, (list, tuple)):
            self._output_array(value)
        elif isinstance(value, bytes):
            self._sb.write(value.decode("utf-8", errors="replace"))
        else:
            self._output_fobject(value)

    def stringify(self, obj: Any) -> str:
        self._sb = io.StringIO()
        self.output(obj)
        return self._sb.getvalue()

    def __str__(self) -> str:
        return self._sb.getvalue()

    # ----------------------------------------------------------- primitives
    def _output_string(self, s: str) -> None:
        # XML content escaping (the Java code does NOT escape, but we do —
        # raw appends produce invalid XML for content containing < > & ).
        self._sb.write(_xml_escape_text(s))

    def _output_number(self, value) -> None:
        self._sb.write(str(value))

    def _output_boolean(self, value: bool) -> None:
        self._sb.write("true" if value else "false")

    def _output_date(self, value) -> None:
        if isinstance(value, datetime.datetime):
            ms = value.microsecond // 1000
            self._sb.write(value.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z")
        else:
            self._sb.write(value.isoformat())

    def _output_enum(self, value: enum.Enum) -> None:
        self._sb.write(value.name)

    def _output_array(self, values: Iterable) -> None:
        for v in values:
            self.output(v)

    # ----------------------------------------------------------- FObject
    def _output_fobject(self, obj: Any) -> None:
        name = type(obj).__name__
        if isinstance(obj, dict):
            name = obj.get("_class", name)
        self._sb.write("<")
        self._sb.write(name)
        self._output_attributes(obj)
        self._sb.write(">")
        self._output_properties(obj)
        self._sb.write("</")
        self._sb.write(name)
        self._sb.write(">")

    def _output_attributes(self, obj: Any) -> None:
        for attr_name in _xml_attribute_names(obj):
            value = _get_field(obj, attr_name)
            if value is None:
                continue
            self._sb.write(" ")
            self._sb.write(self._property_name(obj, attr_name))
            self._sb.write('="')
            self._sb.write(_xml_escape_attr(self._stringify_attr(value)))
            self._sb.write('"')

    def _stringify_attr(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, enum.Enum):
            return value.name
        if isinstance(value, datetime.datetime):
            ms = value.microsecond // 1000
            return value.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z"
        if isinstance(value, datetime.date):
            return value.isoformat()
        return str(value)

    def _output_properties(self, obj: Any) -> None:
        elem_names = [n for n in _all_property_names(obj)
                      if n not in _xml_attribute_names(obj) and not n.startswith("_")]
        skip = _transient_for_mode(obj, self.mode_)
        for name in elem_names:
            if name in skip:
                continue
            value = _get_field(obj, name)
            if value is None or (isinstance(value, (list, tuple)) and not value):
                continue
            if not self.output_default_values_ and _is_default(obj, name, value):
                continue
            self._output_property(name, value, obj)

    def _output_property(self, name: str, value: Any, obj: Any) -> None:
        tag = self._property_name(obj, name)
        if isinstance(value, (list, tuple)):
            for item in value:
                self._output_property(name, item, obj)
            return
        if isinstance(value, dict) or (hasattr(value, "__dict__")
                                       and not isinstance(value, (str, bytes))):
            # Nested object — recurse into a wrapping element
            self._sb.write("<"); self._sb.write(tag); self._sb.write(">")
            self._output_properties(value)
            self._sb.write("</"); self._sb.write(tag); self._sb.write(">")
            return
        self._sb.write("<"); self._sb.write(tag); self._sb.write(">")
        self.output(value)
        self._sb.write("</"); self._sb.write(tag); self._sb.write(">")

    def _property_name(self, obj: Any, name: str) -> str:
        if self.output_short_names_:
            short_map = getattr(obj, "xml_short_names", None)
            if isinstance(short_map, dict) and name in short_map:
                return short_map[name]
        return name


# ---------------------------------------------------------------------------
# Introspection helpers (Python equivalent of PropertyInfo.getXMLAttribute)
# ---------------------------------------------------------------------------

def _xml_attribute_names(obj: Any) -> List[str]:
    if isinstance(obj, dict):
        v = obj.get("_xml_attrs")
        return list(v) if v else []
    return list(getattr(obj, "xml_attribute_names", ()))


def _transient_for_mode(obj: Any, mode: OutputterMode) -> List[str]:
    if mode == OutputterMode.FULL:
        return []
    key = {
        OutputterMode.NETWORK: "network_transient",
        OutputterMode.STORAGE: "storage_transient",
        OutputterMode.EXTERNAL: "external_transient",
    }[mode]
    if isinstance(obj, dict):
        return list(obj.get(key) or [])
    return list(getattr(obj, key, ()))


def _all_property_names(obj: Any) -> List[str]:
    if isinstance(obj, dict):
        return [k for k in obj.keys() if not str(k).startswith("_")]
    if hasattr(obj, "__dataclass_fields__"):
        return list(obj.__dataclass_fields__.keys())
    return [k for k in vars(obj).keys() if not k.startswith("_")]


def _get_field(obj: Any, name: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(name)
    return getattr(obj, name, None)


def _is_default(obj: Any, name: str, value: Any) -> bool:
    if hasattr(obj, "__dataclass_fields__"):
        f = obj.__dataclass_fields__.get(name)
        if f is not None:
            try:
                if value == f.default:
                    return True
            except Exception:
                pass
    return False


_XML_TEXT_ESCAPES = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
_XML_ATTR_ESCAPES = {"&": "&amp;", "<": "&lt;", '"': "&quot;"}


def _xml_escape_text(s: str) -> str:
    return "".join(_XML_TEXT_ESCAPES.get(c, c) for c in s)


def _xml_escape_attr(s: str) -> str:
    return "".join(_XML_ATTR_ESCAPES.get(c, c) for c in s)


def stringify(obj: Any, **kwargs) -> str:
    """Top-level convenience: ``Outputter(**kwargs).stringify(obj)``."""
    return Outputter(**kwargs).stringify(obj)


__all__ = ["OutputterMode", "Outputter", "stringify"]
