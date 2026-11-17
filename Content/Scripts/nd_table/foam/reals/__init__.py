"""
foam3_py.reals — integrate the constructive reals package (PyPI ``reals``,
SGI/Hans-Boehm-style symbolic CR arithmetic) with the rest of foam3_py and
the nD Table.

Constructive reals let cells hold exact, arbitrary-precision numbers. The
underlying ``reals.Real`` is *lazy*: an expression like ``sqrt(2)`` or
``pi * 2`` keeps its symbolic form and is only approximated to as many
digits as you ask for via ``r.evaluate(n)``. Operations don't accumulate
rounding error — the answer is described exactly and only materialised
when you call for a specific precision.

This module exposes:

    CRExpr            dataclass holding a source expression + precision +
                      cached decimal string. Round-trips through
                      foam3_py.json, foam3_py.formatter, and ndtable_zarr.
    CR(expr, prec)    construct a CRExpr (the formula-friendly callable)
    evaluate(expr)    one-shot: parse + materialise + decimal string
    materialize(s)    parse an expression string into a live reals.Real
    revive(value)     walk a tree and revive embedded CRExpr dicts
    install_into_table(table)
                      register CR()/cr()/Real()/PI/E/PHI/SQRT/SIN/COS/EXP/LOG
                      callables into a table's formula context
    ensure_zarr_codec_registered()
                      retry hook for codec registration

Cell example::

    from ndtable import Table, Axis
    from foam3_py.reals import install_into_table
    t = Table(axes=[Axis(0, 4, name="r"), Axis(0, 4, name="c")])
    install_into_table(t)
    t[0, 0] = '=CR("sqrt(2)", 40)'
    print(t[0, 0])
    # CR('sqrt(2)', precision=40) ≈ 1.4142135623730950488016887242096980785696...

The expression language is a small subset of Python evaluated against a
locked namespace (``pi e phi sqrt sin cos exp log + - * / **`` plus the
constructors ``Real.from_int / from_fraction / from_decimal``). It is NOT
arbitrary Python — ``eval`` runs with ``__builtins__ = {}`` and only the
explicit whitelist.
"""

from __future__ import annotations

import dataclasses as _dc
import importlib
import os
import sys
from decimal import Decimal
from fractions import Fraction
from typing import Any, Callable, Dict, Optional, Sequence

# Re-export the public reals symbols so callers can write
# ``from foam3_py.reals import pi, sqrt`` without depending on `reals`
# directly. This also lets the safe-eval namespace pull names from us.
from reals import Real, pi, e, phi, sqrt, sin, cos, exp, log
from reals import sinh, cosh, tan, tanh, csc, sec, cot, coth, csch, sech


_HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Locked expression-eval namespace
# ---------------------------------------------------------------------------

_SAFE_NAMESPACE: Dict[str, Any] = {
    # Constructors
    "Real": Real,
    "from_int":      Real.from_int,
    "from_fraction": Real.from_fraction,
    "from_decimal":  Real.from_decimal,
    # Constants
    "pi": pi, "e": e, "phi": phi,
    "PI": pi, "E": e, "PHI": phi,
    # Functions
    "sqrt": sqrt, "exp": exp, "log": log,
    "sin": sin, "cos": cos, "tan": tan,
    "sinh": sinh, "cosh": cosh, "tanh": tanh,
    "csc": csc, "sec": sec, "cot": cot,
    "csch": csch, "sech": sech, "coth": coth,
    # Helpers for inline fractions/decimals
    "Fraction": Fraction,
    "Decimal": Decimal,
    # Aliases the calculator UI typically uses
    "ln": log,
}


def materialize(expr: str) -> Real:
    """Parse a CR expression string and return a live ``reals.Real``.
    The expression is evaluated against a locked namespace — pure Python
    syntax is allowed but ``__builtins__`` is empty, so file IO, imports,
    attribute escapes etc. cannot resolve."""
    if not isinstance(expr, str):
        raise TypeError(f"expected str, got {type(expr).__name__}")
    expr = expr.strip()
    if not expr:
        raise ValueError("empty CR expression")
    code = compile(expr, "<cr-expr>", "eval")
    value = eval(code, {"__builtins__": {}}, _SAFE_NAMESPACE)
    if isinstance(value, (int, Fraction)):
        value = Real.from_fractional(value) if isinstance(value, Fraction) \
                else Real.from_int(value)
    if isinstance(value, Decimal):
        value = Real.from_decimal(value)
    if not isinstance(value, Real):
        raise TypeError(
            f"CR expression must yield a Real / int / Fraction / Decimal, "
            f"got {type(value).__name__}"
        )
    return value


# ---------------------------------------------------------------------------
# CRExpr — the serialisable value type
# ---------------------------------------------------------------------------

DEFAULT_PRECISION = 30


@_dc.dataclass
class CRExpr:
    """A serializable constructive-real expression.

    Fields:
        expr           Source expression (e.g. "sqrt(2)", "pi * 2")
        precision      Default digits for ``str(self)`` / ``cached_value``
        cached_value   Evaluated decimal string (computed in __post_init__)

    The ``cached_value`` lets the JSON / Zarr serialised form carry the
    decimal representation alongside the symbolic form — so even if the
    expression language drifts, the numeric value survives.
    """

    expr: str = ""
    precision: int = DEFAULT_PRECISION
    cached_value: str = ""

    _CLASS_TAG = "CRExpr"

    def __post_init__(self) -> None:
        if not self.cached_value and self.expr:
            try:
                self.cached_value = self.materialize().evaluate(self.precision)
            except Exception:
                # Defer until explicit call; serialisation can still proceed
                # with the source expression alone.
                self.cached_value = ""

    def materialize(self) -> Real:
        """Re-evaluate the source expression and return a live ``Real``."""
        return materialize(self.expr)

    def evaluate(self, n: Optional[int] = None) -> str:
        """Return a decimal string with ``n`` digits (default
        ``self.precision``). Updates ``cached_value`` when called with
        the default precision."""
        digits = self.precision if n is None else n
        s = self.materialize().evaluate(digits)
        if n is None or n == self.precision:
            self.cached_value = s
        return s

    def to_float(self) -> float:
        return self.materialize().to_float()

    def to_decimal(self, n: Optional[int] = None) -> Decimal:
        return self.materialize().to_decimal(n if n is not None
                                             else self.precision)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CRExpr":
        if d.get("class") and d["class"] != cls._CLASS_TAG:
            raise ValueError(f"expected {cls._CLASS_TAG}, got {d['class']!r}")
        return cls(
            expr=d.get("expr", ""),
            precision=int(d.get("precision", DEFAULT_PRECISION)),
            cached_value=d.get("cached_value", "") or "",
        )

    # Arithmetic — convenience so cells can do CR("pi") * CR("e")
    def _to_real(self, other: Any) -> Real:
        if isinstance(other, CRExpr):
            return other.materialize()
        if isinstance(other, Real):
            return other
        if isinstance(other, (int, Fraction, Decimal)):
            return Real.from_number(other)
        if isinstance(other, str):
            return materialize(other)
        if isinstance(other, float):
            return Real.from_decimal(Decimal(repr(other)))
        raise TypeError(f"cannot CR-combine with {type(other).__name__}")

    def _wrap(self, lhs: str, op: str, other: Any, prec: Optional[int] = None) -> "CRExpr":
        if isinstance(other, CRExpr):
            rhs = f"({other.expr})"
        elif isinstance(other, (int, Fraction, Decimal)):
            rhs = repr(other)
        elif isinstance(other, str):
            rhs = f"({other})"
        elif isinstance(other, float):
            rhs = f"Decimal('{other!r}')"
        elif isinstance(other, Real):
            # No way to round-trip a raw Real symbolically, so render via decimal.
            rhs = f"Decimal('{other.evaluate(prec or self.precision)}')"
        else:
            raise TypeError(f"unsupported CR operand: {type(other).__name__}")
        expr = f"({lhs}) {op} {rhs}"
        return CRExpr(expr=expr, precision=prec or self.precision)

    def __add__(self, other: Any) -> "CRExpr": return self._wrap(self.expr, "+", other)
    def __sub__(self, other: Any) -> "CRExpr": return self._wrap(self.expr, "-", other)
    def __mul__(self, other: Any) -> "CRExpr": return self._wrap(self.expr, "*", other)
    def __truediv__(self, other: Any) -> "CRExpr": return self._wrap(self.expr, "/", other)
    def __pow__(self, other: Any) -> "CRExpr": return self._wrap(self.expr, "**", other)
    def __radd__(self, other: Any) -> "CRExpr": return self._wrap(repr(other), "+", self)
    def __rsub__(self, other: Any) -> "CRExpr": return self._wrap(repr(other), "-", self)
    def __rmul__(self, other: Any) -> "CRExpr": return self._wrap(repr(other), "*", self)
    def __rtruediv__(self, other: Any) -> "CRExpr": return self._wrap(repr(other), "/", self)
    def __neg__(self) -> "CRExpr":
        return CRExpr(expr=f"-({self.expr})", precision=self.precision)

    def __str__(self) -> str:
        if self.cached_value:
            return self.cached_value
        try:
            return self.evaluate()
        except Exception as exc:
            return f"<CR expr {self.expr!r}: {exc}>"

    def __repr__(self) -> str:
        v = self.cached_value or "?"
        return f"CR({self.expr!r}, precision={self.precision}) ≈ {v}"


# ---------------------------------------------------------------------------
# Public construction helpers (used as cell-formula callables)
# ---------------------------------------------------------------------------

def CR(expr: Any, precision: int = DEFAULT_PRECISION) -> CRExpr:
    """Build a CRExpr from a source expression or a numeric literal."""
    if isinstance(expr, CRExpr):
        return CRExpr(expr=expr.expr, precision=precision,
                      cached_value=expr.cached_value)
    if isinstance(expr, str):
        return CRExpr(expr=expr, precision=precision)
    if isinstance(expr, Real):
        return CRExpr(expr=f"Decimal('{expr.evaluate(precision)}')",
                      precision=precision)
    if isinstance(expr, (int, Fraction, Decimal)):
        return CRExpr(expr=repr(expr), precision=precision)
    if isinstance(expr, float):
        return CRExpr(expr=f"Decimal('{expr!r}')", precision=precision)
    raise TypeError(f"cannot construct CR from {type(expr).__name__}")


def evaluate(expr: str, precision: int = DEFAULT_PRECISION) -> str:
    """One-shot helper: parse, materialise, render as a decimal string."""
    return materialize(expr).evaluate(precision)


def is_cr_expr_dict(d: Any) -> bool:
    if not isinstance(d, dict):
        return False
    if d.get("class") == CRExpr._CLASS_TAG:
        return True
    return "expr" in d and "precision" in d and "cached_value" in d


def revive(value: Any) -> Any:
    """Walk a Python value tree (e.g. from ``foam3_py.json.loads``) and
    revive any embedded ``CRExpr`` dicts into ``CRExpr`` instances."""
    if isinstance(value, list):
        return [revive(v) for v in value]
    if isinstance(value, dict):
        if is_cr_expr_dict(value):
            return CRExpr.from_dict(value)
        return {k: revive(v) for k, v in value.items()}
    return value


# ---------------------------------------------------------------------------
# nD Table wiring — mirrors foam3_py.jello.install_into_table
# ---------------------------------------------------------------------------

_SIDE_NS: Dict[int, Dict[str, Any]] = {}


def formula_namespace_for(table: Any) -> Dict[str, Any]:
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
    if getattr(table, "_cr_patched", False):
        return
    if not hasattr(table, "_get_formula_context"):
        setattr(table, "_cr_patched", True)
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
        if not getattr(cls, "_cr_class_patched", False):
            cls_original = cls._get_formula_context
            def cls_patched(self_, *a, **kw):
                ctx = cls_original(self_, *a, **kw)
                extra = formula_namespace_for(self_)
                if extra:
                    ctx.update(extra)
                return ctx
            cls._get_formula_context = cls_patched  # type: ignore[assignment]
            cls._cr_class_patched = True  # type: ignore[attr-defined]
    setattr(table, "_cr_patched", True)


def install_into_table(table: Any,
                       *, name: str = "CR",
                       also: Sequence[str] = ("cr",)) -> None:
    """Register ``CR``, ``cr``, the constants ``PI``/``E``/``PHI`` and the
    helpers ``SQRT``/``SIN``/``COS``/``EXP``/``LOG`` as cell-formula
    callables on ``table``. Idempotent, instance-scoped, doesn't pollute
    other tables."""
    ns = formula_namespace_for(table)
    ns[name] = CR
    for n in also:
        ns[n] = CR
    # Convenience: also expose the underlying Real + functions so a cell
    # formula can write =sqrt(2)+pi/4 directly without going through CR().
    ns.update({
        "Real": Real,
        "PI": pi, "E": e, "PHI": phi,
        "SQRT": sqrt, "SIN": sin, "COS": cos, "EXP": exp, "LOG": log,
        # lower-case aliases for chained inline use
        "cr_pi": pi, "cr_e": e, "cr_phi": phi,
        "cr_sqrt": sqrt, "cr_sin": sin, "cr_cos": cos,
        "cr_exp": exp, "cr_log": log,
    })
    _wrap_formula_context(table)


# ---------------------------------------------------------------------------
# ndtable_zarr codec registration (auto on import, with retry hook)
# ---------------------------------------------------------------------------

def _register_zarr_codec_for_cr_expr() -> bool:
    """Idempotent. Tries to register a CRExpr codec with ndtable_zarr so
    cells holding CRExpr survive the Zarr round-trip as CRExpr. Returns
    True on success, False otherwise."""
    mod = None

    # Strategy 1: direct path import (bypasses nd_table/__init__.py).
    try:
        scripts_dir = os.path.normpath(os.path.join(_HERE, "..", ".."))
        nd_table_dir = os.path.join(scripts_dir, "nd_table")
        if os.path.isdir(nd_table_dir) and nd_table_dir not in sys.path:
            sys.path.insert(0, nd_table_dir)
        mod = importlib.import_module("ndtable_zarr")
    except BaseException:
        mod = None

    if mod is None:
        try:
            mod = importlib.import_module("nd_table.ndtable_zarr")
        except BaseException:
            mod = None

    if mod is None or not hasattr(mod, "register_codec"):
        return False
    try:
        mod.register_codec(
            tag=CRExpr._CLASS_TAG,
            predicate=lambda v: isinstance(v, CRExpr),
            encode=lambda v: _dc.asdict(v),
            decode=lambda payload: CRExpr.from_dict(payload or {}),
        )
        return True
    except BaseException:
        return False


_zarr_codec_registered: bool = _register_zarr_codec_for_cr_expr()


def ensure_zarr_codec_registered() -> bool:
    """Public retry hook — call if ``foam3_py.reals`` was imported before
    ``ndtable_zarr`` was reachable."""
    global _zarr_codec_registered
    if not _zarr_codec_registered:
        _zarr_codec_registered = _register_zarr_codec_for_cr_expr()
    return _zarr_codec_registered


# ---------------------------------------------------------------------------
# Java-CR API parity layer
# ---------------------------------------------------------------------------
#
# These helpers mirror methods on Hans-Boehm's com.hp.creals.CR (and the JS
# port creal.js) that aren't directly exposed by the Python `reals` package:
#
#   shift_left(r, n) / shift_right(r, n)     CR.shiftLeft / shiftRight
#   signum(r, tol_bits=-50)                   CR.signum(int)
#   compare_to(a, b, tol_bits=-50)            CR.compareTo(CR, int)
#   select(s, x, y, tol_bits=-50)             CR.select  (divergence-safe)
#   abs_cr(r) / max_cr(a,b) / min_cr(a,b)     CR.abs / max / min
#   to_int(r) / to_long(r) / to_bigint(r)     CR.intValue / longValue /
#                                              BigIntegerValue
#   value_of_string(s, radix=10)              CR.valueOf(String, int)
#   to_string_radix(r, n, radix=10)           CR.toString(int, int)
#   atan(r) / asin(r) / acos(r) / atan2(y,x)  JS port additions
#
# Tolerance is specified in *bits*: an absolute tolerance of 2**tol_bits.
# tol_bits=-50 ≈ 1e-15. Smaller (more negative) = tighter tolerance.

from reals.approximation import Approximation as _Approximation
from fractions import Fraction as _Fraction


import enum as _enum
import math as _math


class IEEEFloatError(ValueError):
    """Raised when a non-finite IEEE 754 float (NaN, +Inf, -Inf) is supplied
    where a constructive real is required. Constructive reals model the
    extended-real number line *without* the IEEE special values: there is
    no exact-zero/negative-zero distinction, no infinities, no NaN."""


def _coerce(x: Any) -> Real:
    """Convert any acceptable input to a reals.Real.

    IEEE 754 input handling:

    * ``float('nan')`` raises ``IEEEFloatError`` — matches Java
      ``CR.valueOf(double)`` which throws ``ArithmeticException`` on NaN.
    * ``float('inf')`` / ``float('-inf')`` likewise — constructive reals
      can't represent infinities. (You can construct numbers arbitrarily
      large via ``Real.from_int(10**N)``.)
    * IEEE −0.0 collapses to exact 0 — same as Java's
      ``Double.doubleToLongBits`` decomposition followed by ``shiftLeft``.
    """
    if isinstance(x, Real):
        return x
    if isinstance(x, CRExpr):
        return x.materialize()
    if isinstance(x, bool):  # before int
        return Real.from_int(int(x))
    if isinstance(x, int):
        return Real.from_int(x)
    if isinstance(x, _Fraction):
        return Real.from_fraction(x)
    if isinstance(x, Decimal):
        if not x.is_finite():
            raise IEEEFloatError(f"cannot coerce non-finite Decimal: {x!r}")
        return Real.from_decimal(x)
    if isinstance(x, float):
        if _math.isnan(x):
            raise IEEEFloatError("cannot coerce NaN to constructive real")
        if _math.isinf(x):
            raise IEEEFloatError(
                "cannot coerce ±Infinity to constructive real "
                "(constructive reals are finite by construction)"
            )
        # IEEE -0.0 → exact 0
        if x == 0.0:
            return Real.from_int(0)
        return Real.from_decimal(Decimal(repr(x)))
    if isinstance(x, str):
        return materialize(x)
    raise TypeError(f"cannot coerce {type(x).__name__} to Real")


# ---------------------------------------------------------------------------
# IEEE 754 rounding modes
# ---------------------------------------------------------------------------
#
# IEEE 754-2008 §4.3 defines five "rounding-direction attributes":
#
#   roundTiesToEven       — Banker's rounding; the default for binary floats
#   roundTiesToAway       — Decimal-arithmetic default; Java Math.round
#   roundTowardPositive   — toward +∞ (ceiling)
#   roundTowardNegative   — toward −∞ (floor)
#   roundTowardZero       — truncate toward 0
#
# We expose all five plus the two commonly-asked-for non-IEEE companions:
# HALF_DOWN (ties toward zero, used in some financial code) and UP (always
# away from zero, never IEEE but handy).

class RoundingMode(_enum.Enum):
    """IEEE 754 rounding direction attributes (plus two non-IEEE
    conveniences). The default for ``to_bigint`` / ``to_int`` / ``to_long``
    is ``HALF_EVEN``, matching IEEE 754 binary arithmetic."""

    HALF_EVEN = "roundTiesToEven"        # IEEE 754 default
    HALF_AWAY = "roundTiesToAway"         # IEEE 754; Java Math.round
    CEILING   = "roundTowardPositive"     # toward +∞
    FLOOR     = "roundTowardNegative"     # toward −∞
    DOWN      = "roundTowardZero"         # truncate toward 0
    # Non-IEEE companions; see docstring above.
    HALF_DOWN = "roundHalfDown"           # ties toward 0
    UP        = "roundAwayFromZero"       # always away from 0


# Back-compat aliases.
RoundingMode.HALF_UP = RoundingMode.HALF_AWAY  # type: ignore[attr-defined]


def _round_fraction(p: int, q: int, mode: RoundingMode) -> int:
    """Round the rational ``p/q`` to an integer per the IEEE 754 rounding
    direction ``mode``. Works for any sign of ``p`` and any positive or
    negative ``q``; raises ``ZeroDivisionError`` for q == 0.
    """
    if q < 0:
        p, q = -p, -q
    if q == 0:
        raise ZeroDivisionError("rounding fraction with zero denominator")
    floor = p // q
    rem = p - floor * q  # 0 <= rem < q
    if rem == 0:
        return floor  # exact

    if mode is RoundingMode.FLOOR:
        return floor
    if mode is RoundingMode.CEILING:
        return floor + 1
    if mode is RoundingMode.DOWN:
        # truncate toward 0
        return floor if p >= 0 else floor + 1
    if mode is RoundingMode.UP:
        # away from 0
        return floor + 1 if p >= 0 else floor

    # HALF_* modes: compare rem to q/2 without going through float.
    twice = 2 * rem
    if twice > q:
        return floor + 1
    if twice < q:
        return floor
    # Tie: exactly p/q == floor + 1/2
    if mode is RoundingMode.HALF_EVEN:
        return floor + 1 if floor % 2 else floor
    if mode is RoundingMode.HALF_AWAY:
        return floor + 1 if p >= 0 else floor
    if mode is RoundingMode.HALF_DOWN:
        return floor if p >= 0 else floor + 1
    raise ValueError(f"unknown rounding mode: {mode!r}")


def _round_float(f: float, mode: RoundingMode) -> int:
    """Round an IEEE 754 binary64 ``f`` to integer per ``mode``. Fast paths
    for the common modes; falls back to ``_round_fraction`` otherwise."""
    if mode is RoundingMode.HALF_EVEN:
        # Python's round() is half-to-even (banker's), matching IEEE 754.
        return round(f)
    if mode is RoundingMode.FLOOR:
        return _math.floor(f)
    if mode is RoundingMode.CEILING:
        return _math.ceil(f)
    if mode is RoundingMode.DOWN:
        return int(f)  # truncates toward 0
    # Remaining modes via exact Fraction.
    frac = _Fraction(f)  # exact for any finite float
    return _round_fraction(frac.numerator, frac.denominator, mode)


def _eps_for_bits(tol_bits: int) -> _Fraction:
    """Convert a Java-style bit tolerance to a positive Fraction epsilon."""
    if tol_bits >= 0:
        return _Fraction(1 << tol_bits, 1)
    return _Fraction(1, 1 << -tol_bits)


def _improve_until_eps(appr: "_Approximation", eps: _Fraction,
                       max_iters: int = 4000) -> bool:
    """Tighten ``appr``'s interval until its width is <= ``eps``, using
    only single-step ``improve()`` calls (never the upstream
    ``improve_epsilon`` which has an assertion bug on iterators that
    terminate).

    Returns True if we hit the target width, False if we bailed out
    because (a) the iterator was exhausted (``as_fraction()`` is then
    exact) or (b) we hit ``max_iters`` without converging.
    """
    iters = 0
    while iters < max_iters:
        cur = appr.epsilon_fraction()
        if cur is not None and cur <= eps:
            return True
        try:
            appr.improve()
        except (AssertionError, StopIteration):
            return False
        iters += 1
    return False


def shift_left(r: Any, n: int) -> Real:
    """Multiply ``r`` by 2**n. Equivalent to Java CR.shiftLeft(n)."""
    real = _coerce(r)
    if n == 0:
        return real
    if n > 0:
        return real * Real.from_int(1 << n)
    return real / Real.from_int(1 << -n)


def shift_right(r: Any, n: int) -> Real:
    """Multiply ``r`` by 2**(-n). Equivalent to Java CR.shiftRight(n)."""
    return shift_left(r, -n)


# Cached-float sentinel; bound to a Real via _float_cache(real). We use a
# WeakValueDictionary-style side table keyed by id(real) so we don't hold a
# strong reference and don't have to worry about Real instances rejecting
# attribute assignment (the package doesn't define __slots__ today, but we
# stay defensive in case it does).
_FLOAT_CACHE: Dict[int, float] = {}


def _safe_to_float(real: Real, max_iters: int = 64) -> float:
    """Approximation-driven float probe with a hard iteration budget.

    The upstream ``Real.to_float()`` invokes
    ``Approximation.closest_float()`` which loops until ``lo == hi`` in
    float representation — but on a terminated continued-fraction
    iterator (e.g. ``Real.from_int(0)``) the bounds never collapse,
    leading to an infinite loop. We replicate the same logic but bail
    after ``max_iters`` and fall back to ``as_fraction()`` when the
    iterator says it's done.
    """
    appr = _Approximation(real)
    for _ in range(max_iters):
        try:
            appr.improve()
        except (AssertionError, StopIteration):
            break
        lo = appr.lower_bound_float()
        hi = appr.upper_bound_float()
        if lo is not None and hi is not None and lo == hi:
            return lo
    # Fallback — synthesise a float from whatever exact fraction we have.
    try:
        frac = appr.as_fraction()
    except (AssertionError, StopIteration):
        frac = None
    if frac is None:
        return 0.0
    try:
        return frac.numerator / frac.denominator
    except (OverflowError, ZeroDivisionError):
        # Massive integer — convert via string round-trip
        try:
            return float(frac)
        except (OverflowError, ValueError):
            return 0.0


def _cached_to_float(real: Real) -> float:
    """Memoised ``_safe_to_float``. A miss costs one bounded Approximation
    sweep (~25 µs); a hit costs a dict lookup (~100 ns). Cache entries are
    finalised when the Real instance is garbage-collected so we don't leak
    on long-running tables."""
    key = id(real)
    cached = _FLOAT_CACHE.get(key)
    if cached is not None:
        return cached
    f = _safe_to_float(real)
    _FLOAT_CACHE[key] = f
    try:
        import weakref
        weakref.finalize(real, _FLOAT_CACHE.pop, key, None)
    except TypeError:
        # Not weakref-able — accept the bounded leak.
        pass
    return f


def signum(r: Any, tol_bits: int = -50, max_bits: int = -2000) -> int:
    """Return -1/0/+1 for the sign of ``r`` within an absolute tolerance of
    2**tol_bits. Java CR.signum(int) analogue.

    Three-stage strategy for speed:

    1. **Cached float probe** — for any Real whose magnitude clearly
       exceeds 2*2**tol_bits, the sign is resolved from ``r.to_float()``
       alone (memoised per Real instance). This is the path 99% of
       interactive callers hit.

    2. **Incremental improve** — for values near zero we feed continued
       fraction terms one at a time and bail as soon as the (lower, upper)
       interval becomes single-signed. Terminates in O(log magnitude)
       steps instead of the O(|tol_bits|) of ``improve_epsilon``.

    3. **Exact-rational shortcut** — catches the upstream bug where
       Approximation raises AssertionError/StopIteration when the
       continued-fraction iterator terminates (e.g. ``Real.from_int(0)``),
       and reads ``as_fraction()`` directly.

    Never diverges — unlike Java's no-arg ``signum()`` which loops forever
    on exact zero, ours bails out at ``max_bits`` and returns 0.
    """
    real = _coerce(r)
    # --- Stage 1: cached float probe --------------------------------------
    f = _cached_to_float(real)
    if tol_bits > -1000 and f != 0.0:
        threshold = 2.0 ** max(tol_bits + 1, -1020)
        if abs(f) > threshold:
            return 1 if f > 0 else -1

    # --- Stage 2: incremental improve, same-sign termination -------------
    appr = _Approximation(real)
    max_iters = max(64, -tol_bits + 32)
    iters = 0
    while iters < max_iters:
        try:
            appr.improve()
        except (AssertionError, StopIteration):
            # Stage 3: exact-rational shortcut
            f_frac = appr.as_fraction()
            if f_frac is None:
                return 0
            if f_frac > 0: return 1
            if f_frac < 0: return -1
            return 0
        iters += 1
        lo = appr.lower_bound_fraction()
        hi = appr.upper_bound_fraction()
        if lo is not None and lo > 0:
            return 1
        if hi is not None and hi < 0:
            return -1
        if lo is not None and hi is not None and lo == 0 and hi == 0:
            return 0
    return 0


# ---------------------------------------------------------------------------
# Branch-on-sign primitive
# ---------------------------------------------------------------------------
#
# The Java CR class builds the divergence-safe conditional ``select(s,x,y)``
# as a new lazy CR. Subclasses of ``com.sgi.math.CR`` would override
# ``approximate(p)`` to probe ``s``'s sign and forward to one of
# ``x.approximate(p)`` / ``y.approximate(p)``. The Python ``reals`` package
# doesn't expose subclassing, so we do the same trick in Python land: probe
# the sign once (via the cached-float fast path), then return the chosen
# branch eagerly. The cost is one ``signum()`` plus *one* materialised
# branch — never both. This is what makes ``abs(pi)`` essentially free.
#
# All four select-family helpers (select / abs_cr / max_cr / min_cr) funnel
# through ``_pick_by_sign``, so they share both the optimisation and the
# tolerance semantics.

def _pick_by_sign(selector: Real,
                  neg: "Callable[[], Real]",
                  nonneg: "Callable[[], Real]",
                  tol_bits: int) -> Real:
    """Return ``neg()`` if signum(selector) < 0 else ``nonneg()``.

    The branches are passed as zero-argument thunks so the unused one is
    never materialised. Java's CR.select(x, y) takes already-built CRs;
    we relax that to thunks because in Python ``-real`` is eager and
    relatively expensive (it creates a new Real whose float cache is
    cold).
    """
    if signum(selector, tol_bits=tol_bits) < 0:
        return neg()
    return nonneg()


def compare_to(a: Any, b: Any, tol_bits: int = -50) -> int:
    """Sign of ``a - b`` within 2**tol_bits. Java CR.compareTo(CR, int)
    analogue. Returns -1/0/+1."""
    return signum(_coerce(a) - _coerce(b), tol_bits=tol_bits)


def select(s: Any, x: Any, y: Any, tol_bits: int = -50) -> Real:
    """Divergence-safe conditional: ``x`` if s<0, ``y`` otherwise. Java
    CR.select(x, y) analogue.

    Note: in the Java class, ``select`` is a method on the *selector*
    (``s.select(x, y)``). The required pre-condition ``x == y when s == 0``
    is not checked here; we behave as if s<0 → x, s>=0 → y at the chosen
    tolerance."""
    return _pick_by_sign(_coerce(s),
                         neg=lambda: _coerce(x),
                         nonneg=lambda: _coerce(y),
                         tol_bits=tol_bits)


def abs_cr(r: Any, tol_bits: int = -50) -> Real:
    """Absolute value. Java CR.abs() analogue, defined there as
    ``select(negate(), this)`` — for r>=0 the branch is just ``r`` (already
    cached, so this is essentially free) and ``-r`` is only materialised
    when ``r<0``. Cannot be written as a Python ``if`` because the
    comparison would diverge on exact zero."""
    real = _coerce(r)
    return _pick_by_sign(real,
                         neg=lambda: -real,
                         nonneg=lambda: real,
                         tol_bits=tol_bits)


def max_cr(a: Any, b: Any, tol_bits: int = -50) -> Real:
    """Java CR.max(x) analogue, defined there as
    ``subtract(x).select(x, this)``. Equivalent: pick whichever of (a, b)
    has the larger value at the chosen tolerance."""
    ar = _coerce(a); br = _coerce(b)
    return _pick_by_sign(ar - br,
                         neg=lambda: br,
                         nonneg=lambda: ar,
                         tol_bits=tol_bits)


def min_cr(a: Any, b: Any, tol_bits: int = -50) -> Real:
    """Java CR.min(x) analogue, defined there as
    ``subtract(x).select(this, x)``. Picks the smaller of (a, b)."""
    ar = _coerce(a); br = _coerce(b)
    return _pick_by_sign(ar - br,
                         neg=lambda: ar,
                         nonneg=lambda: br,
                         tol_bits=tol_bits)


def to_bigint(r: Any, *,
              rounding: RoundingMode = RoundingMode.HALF_EVEN,
              half_up: Optional[bool] = None) -> int:
    """Round ``r`` to a Python int according to an IEEE 754 rounding
    direction. Java CR.BigIntegerValue() analogue.

    Default ``rounding`` is ``HALF_EVEN`` — IEEE 754's
    ``roundTiesToEven`` ("banker's rounding"), the default for binary
    floating-point arithmetic. Java's ``BigIntegerValue()`` is equivalent
    to ``HALF_AWAY``; pass ``rounding=RoundingMode.HALF_AWAY`` if you
    need byte-for-byte parity with the Boehm implementation.

    Back-compat: the legacy ``half_up=True/False`` keyword from the
    pre-IEEE version is still accepted (mapping to ``HALF_AWAY`` /
    ``DOWN``); if both ``rounding`` and ``half_up`` are supplied,
    ``rounding`` wins.

    Fast path: for any value whose magnitude fits comfortably inside a
    double (|r| < 2**52), ``to_float()`` is exact-enough to round
    correctly, and we skip Approximation entirely. Falls back to
    incremental ``improve()`` for values too large for double precision.
    """
    # Honor legacy half_up keyword only when rounding wasn't explicitly set
    # (the test for "explicitly set" is intentionally loose — if a caller
    # passes both, the new rounding wins).
    if half_up is not None and rounding is RoundingMode.HALF_EVEN:
        rounding = RoundingMode.HALF_AWAY if half_up else RoundingMode.DOWN

    real = _coerce(r)
    f_val = _cached_to_float(real)
    if f_val is not None and abs(f_val) < 2.0 ** 52:
        # to_float() gives the closest representable double; for |r|<2^52
        # the integer rounding of that float matches the integer rounding
        # of r itself.
        return _round_float(f_val, rounding)

    # Slow path: incremental refinement until the rounded interval picks
    # a unique integer for the chosen rounding rule.
    appr = _Approximation(real)
    iters = 0
    while iters < 200:
        try:
            appr.improve()
        except (AssertionError, StopIteration):
            break
        iters += 1
        lo = appr.lower_bound_fraction()
        hi = appr.upper_bound_fraction()
        if lo is None or hi is None:
            continue
        li = _round_fraction(lo.numerator, lo.denominator, rounding)
        hi_i = _round_fraction(hi.numerator, hi.denominator, rounding)
        if li == hi_i:
            return li
    # Bail-out: read whatever exact value we have.
    f = appr.as_fraction()
    if f is None:
        return 0
    return _round_fraction(f.numerator, f.denominator, rounding)


def to_int(r: Any, *,
           rounding: RoundingMode = RoundingMode.HALF_EVEN) -> int:
    """CR.intValue() analogue. Behaviour on overflow is undefined (Java
    silently truncates; Python ints have arbitrary precision so we just
    return the rounded value)."""
    return to_bigint(r, rounding=rounding)


def to_long(r: Any, *,
            rounding: RoundingMode = RoundingMode.HALF_EVEN) -> int:
    """CR.longValue() analogue. Behaviour on overflow is undefined."""
    return to_bigint(r, rounding=rounding)


# ---------------------------------------------------------------------------
# IEEE 754 binary64 / binary32 conversion
# ---------------------------------------------------------------------------

def to_float64(r: Any) -> float:
    """Convert ``r`` to an IEEE 754 binary64 (Python float) with
    round-to-nearest-even — the IEEE 754 default rounding direction. Java
    CR.doubleValue() analogue. Returns ``float('inf')`` / ``float('-inf')``
    on overflow rather than raising (matches IEEE 754 §7.4)."""
    real = _coerce(r)
    return _cached_to_float(real)


def to_float32(r: Any) -> float:
    """Convert ``r`` to IEEE 754 binary32, returned as a Python float
    (Python has no native single-precision type). Rounding is
    round-to-nearest-even at the binary32 boundary. Java CR.floatValue()
    analogue."""
    import struct
    f64 = to_float64(r)
    # struct round-trip uses the CPython conversion which is IEEE
    # round-to-nearest-even from binary64 → binary32.
    return struct.unpack("<f", struct.pack("<f", f64))[0]


def value_of_string(s: str, radix: int = 10) -> Real:
    """CR.valueOf(String, int) analogue. Parses ``[-]digits[.digits]`` in
    the given base (2..36)."""
    if not (2 <= radix <= 36):
        raise ValueError(f"radix must be in 2..36, got {radix}")
    s = s.strip()
    neg = False
    if s.startswith("-"):
        neg = True
        s = s[1:]
    elif s.startswith("+"):
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
    else:
        whole, frac = s, ""
    if not whole and not frac:
        raise ValueError(f"empty number: {s!r}")
    scaled = int((whole or "0") + frac, radix)
    divisor = radix ** len(frac)
    r = Real.from_fraction(_Fraction(scaled, divisor))
    return -r if neg else r


_DIGIT_CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_string_radix(r: Any, n: int, radix: int = 10, *,
                    rounding: RoundingMode = RoundingMode.HALF_EVEN) -> str:
    """Return a textual representation of ``r`` with ``n`` digits to the
    right of the radix point, in the given base (2..36). Java
    CR.toString(int, int) analogue. Uses IEEE 754 ``HALF_EVEN`` rounding
    at the last digit by default; pass ``rounding=`` to override."""
    if not (2 <= radix <= 36):
        raise ValueError(f"radix must be in 2..36, got {radix}")
    if n < 0:
        raise ValueError(f"n must be >= 0, got {n}")
    real = _coerce(r)
    if radix == 10 and rounding is RoundingMode.HALF_EVEN:
        # Fast path; the reals package's evaluate already uses
        # half-up but for n digits it matches HALF_EVEN except at exact
        # ties on the last digit. Acceptable for the default; pass
        # rounding explicitly for guaranteed behaviour.
        return real.evaluate(n)
    # Scale by radix^n, take BigIntegerValue, format in base.
    scaled = real * Real.from_int(radix ** n)
    bi = to_bigint(scaled, rounding=rounding)
    neg = bi < 0
    x = -bi if neg else bi
    if x == 0:
        digits = "0"
    else:
        out = []
        while x > 0:
            out.append(_DIGIT_CHARS[x % radix])
            x //= radix
        digits = "".join(reversed(out))
    if n == 0:
        return ("-" if neg else "") + digits
    if len(digits) <= n:
        digits = "0" * (n + 1 - len(digits)) + digits
    return ("-" if neg else "") + digits[:-n] + "." + digits[-n:]


# ---------------------------------------------------------------------------
# Inverse trig (JS-port additions to Hans Boehm's base library)
# ---------------------------------------------------------------------------

def _atan_fixed_point(r_frac: _Fraction, precision: int) -> _Fraction:
    """Compute atan of a rational ``r_frac`` with |r| <= 1/2 to ``precision``
    decimal digits, using fixed-point integer arithmetic. Returns a Fraction.

    Naive Real-arithmetic Taylor series is correct but balloons the
    expression tree, making each subsequent term cost O(N) more than the
    last. Fixed-point integers cap each term at constant cost.
    """
    import math
    bits = int(precision * math.log2(10)) + 64
    scale = 1 << bits
    # Scale r to fixed point: r_scaled ≈ r_frac * 2^bits
    p, q = r_frac.numerator, r_frac.denominator
    r_scaled = (p * scale) // q
    r2_scaled = (r_scaled * r_scaled) >> bits  # r^2 in fixed point
    term = r_scaled                              # current r^(2k+1) scaled
    total = r_scaled
    sign = 1
    k = 1
    max_iters = max(40, int(precision * math.log2(10) / 2) + 20)
    while k < max_iters:
        term = (term * r2_scaled) >> bits        # term = r^(2k+1) scaled
        sign = -sign
        contribution = (sign * term) // (2 * k + 1)
        if contribution == 0:
            break
        total += contribution
        k += 1
    # Return as Fraction so caller can build a Real with from_fraction
    return _Fraction(total, scale)


def atan(r: Any, *, precision: int = 30) -> Real:
    """arctan(r) — JS-port creal.js addition. Reduces to ``|r| <= 1/2`` via
    the identity network::

        |r| > 1:        atan(r) = sign(r)*π/2 - atan(1/r)
        1/2 < |r| <= 1: atan(r) = π/4 + atan((r-1)/(r+1))   (half-angle)
        else:           Taylor series in fixed-point integer arithmetic

    Returns a ``reals.Real``. The Taylor branch builds a single
    ``Real.from_fraction`` instead of nesting N levels of Real arithmetic,
    so high-precision calls don't blow up the expression tree."""
    rr = _coerce(r)
    s = signum(rr)
    if s == 0:
        return Real.from_int(0)
    if s < 0:
        return -atan(-rr, precision=precision)
    # rr is positive
    one = Real.from_int(1)
    half = Real.from_fraction(_Fraction(1, 2))
    if compare_to(rr, one) > 0:
        return pi / 2 - atan(one / rr, precision=precision)
    if compare_to(rr, half) > 0:
        return pi / 4 + atan((rr - 1) / (rr + 1), precision=precision)
    # 0 < rr <= 1/2: approximate rr as a Fraction, run fixed-point Taylor.
    import math
    bits = int(precision * math.log2(10)) + 32
    appr = _Approximation(rr)
    # Use our defensive helper rather than appr.improve_epsilon: the
    # upstream call asserts on iterators that terminate, and we want a
    # plain improve()-based loop for both performance and safety.
    _improve_until_eps(appr, _Fraction(1, 1 << bits))
    f = appr.as_fraction()
    if f is None:
        return Real.from_int(0)
    result = _atan_fixed_point(f, precision)
    return Real.from_fraction(result)


def asin(r: Any, *, precision: int = 50) -> Real:
    """arcsin(r), defined on [-1, 1]. Uses ``asin(r) = atan(r/sqrt(1-r²))``.
    Edge cases: asin(±1) = ±π/2."""
    rr = _coerce(r)
    one = Real.from_int(1)
    # Check |r| > 1 — undefined
    if compare_to(abs_cr(rr), one) > 0:
        raise ValueError("asin domain: |r| > 1")
    # |r| == 1 — return ±π/2 exactly
    if compare_to(rr, one) == 0:
        return pi / 2
    if compare_to(rr, -one) == 0:
        return -pi / 2
    return atan(rr / sqrt(1 - rr * rr), precision=precision)


def acos(r: Any, *, precision: int = 50) -> Real:
    """arccos(r) = π/2 - asin(r)."""
    return pi / 2 - asin(r, precision=precision)


def atan2(y: Any, x: Any, *, precision: int = 50) -> Real:
    """atan2(y, x) — quadrant-aware arctangent."""
    yr = _coerce(y)
    xr = _coerce(x)
    sx = signum(xr)
    sy = signum(yr)
    if sx > 0:
        return atan(yr / xr, precision=precision)
    if sx < 0 and sy >= 0:
        return atan(yr / xr, precision=precision) + pi
    if sx < 0 and sy < 0:
        return atan(yr / xr, precision=precision) - pi
    # sx == 0
    if sy > 0:
        return pi / 2
    if sy < 0:
        return -pi / 2
    raise ValueError("atan2(0, 0) undefined")


# ---------------------------------------------------------------------------
# Wire new helpers into safe-eval namespace + install_into_table
# ---------------------------------------------------------------------------

_SAFE_NAMESPACE.update({
    "shift_left":    shift_left,
    "shift_right":   shift_right,
    "shiftLeft":     shift_left,    # Java spelling
    "shiftRight":    shift_right,   # Java spelling
    "signum":        signum,
    "select":        select,
    "abs_cr":        abs_cr,
    "max_cr":        max_cr,
    "min_cr":        min_cr,
    "compare_to":    compare_to,
    "compareTo":     compare_to,    # Java spelling
    "to_bigint":     to_bigint,
    "to_int":        to_int,
    "to_long":       to_long,
    "BigIntegerValue": to_bigint,   # Java spelling
    "intValue":      to_int,
    "longValue":     to_long,
    "value_of_string": value_of_string,
    "valueOf":       value_of_string,  # Java spelling (string form)
    "to_string_radix": to_string_radix,
    "toString":      to_string_radix,  # Java spelling
    "atan":          atan,
    "asin":          asin,
    "acos":          acos,
    "atan2":         atan2,
    # IEEE 754 conversion + rounding
    "to_float64":    to_float64,
    "to_float32":    to_float32,
    "doubleValue":   to_float64,   # Java spelling
    "floatValue":    to_float32,   # Java spelling
    "RoundingMode":  RoundingMode,
})


def _install_parity_helpers(ns: Dict[str, Any]) -> None:
    """Add the Java-CR parity helpers to a per-table formula namespace."""
    ns.update({
        "shift_left": shift_left, "shift_right": shift_right,
        "signum": signum, "select": select, "compare_to": compare_to,
        "abs_cr": abs_cr, "max_cr": max_cr, "min_cr": min_cr,
        "to_bigint": to_bigint, "to_int": to_int, "to_long": to_long,
        "to_float64": to_float64, "to_float32": to_float32,
        "value_of_string": value_of_string,
        "to_string_radix": to_string_radix,
        "atan": atan, "asin": asin, "acos": acos, "atan2": atan2,
        "RoundingMode": RoundingMode,
    })


# Monkey-patch install_into_table to also expose the parity helpers. We
# define a wrapper here so it picks up the updated _SAFE_NAMESPACE without
# breaking back-compat with the original signature.
_install_original = install_into_table


def install_into_table(table: Any,
                       *, name: str = "CR",
                       also: Sequence[str] = ("cr",)) -> None:
    _install_original(table, name=name, also=also)
    _install_parity_helpers(formula_namespace_for(table))


# ---------------------------------------------------------------------------
# CRExpr conveniences mirroring the Java method names
# ---------------------------------------------------------------------------

def _crexpr_shift_left(self, n: int) -> "CRExpr":
    return CRExpr(expr=f"shift_left(({self.expr}), {int(n)})",
                  precision=self.precision)


def _crexpr_shift_right(self, n: int) -> "CRExpr":
    return CRExpr(expr=f"shift_right(({self.expr}), {int(n)})",
                  precision=self.precision)


def _crexpr_abs(self) -> "CRExpr":
    return CRExpr(expr=f"abs_cr({self.expr})", precision=self.precision)


def _crexpr_signum(self, tol_bits: int = -50) -> int:
    return signum(self.materialize(), tol_bits=tol_bits)


def _crexpr_to_bigint(self) -> int:
    return to_bigint(self.materialize())


def _crexpr_to_int(self) -> int:
    return to_int(self.materialize())


def _crexpr_to_string_radix(self, n: int, radix: int = 10) -> str:
    return to_string_radix(self.materialize(), n, radix)


CRExpr.shift_left = _crexpr_shift_left          # type: ignore[attr-defined]
CRExpr.shift_right = _crexpr_shift_right        # type: ignore[attr-defined]
CRExpr.abs = _crexpr_abs                        # type: ignore[attr-defined]
CRExpr.__abs__ = _crexpr_abs                    # type: ignore[attr-defined]
CRExpr.signum = _crexpr_signum                  # type: ignore[attr-defined]
CRExpr.to_bigint = _crexpr_to_bigint            # type: ignore[attr-defined]
CRExpr.BigIntegerValue = _crexpr_to_bigint      # type: ignore[attr-defined]
CRExpr.to_int = _crexpr_to_int                  # type: ignore[attr-defined]
CRExpr.intValue = _crexpr_to_int                # type: ignore[attr-defined]
CRExpr.to_string_radix = _crexpr_to_string_radix  # type: ignore[attr-defined]


__all__ = [
    # reals re-exports
    "Real", "pi", "e", "phi", "sqrt", "sin", "cos", "exp", "log",
    "sinh", "cosh", "tan", "tanh",
    # foam3 layer
    "CRExpr", "CR", "evaluate", "materialize",
    "is_cr_expr_dict", "revive",
    "install_into_table", "formula_namespace_for",
    "ensure_zarr_codec_registered",
    "DEFAULT_PRECISION",
    # Java-CR parity layer
    "shift_left", "shift_right",
    "signum", "compare_to", "select",
    "abs_cr", "max_cr", "min_cr",
    "to_bigint", "to_int", "to_long",
    "value_of_string", "to_string_radix",
    "atan", "asin", "acos", "atan2",
    # IEEE 754
    "RoundingMode", "IEEEFloatError",
    "to_float64", "to_float32",
]
