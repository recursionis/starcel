"""2D Projective Geometric Algebra with CReal coefficients.

The 2D analog of :mod:`reals._pga`. Same Klein convention, same
operator-protocol bridge to ``CReal`` for arbitrary precision.

Algebra: ``Cl(2, 0, 1)`` (kingdon ``Algebra(2, 0, 1)``).
Basis: ``e0`` (null, ``e0**2 = 0``), ``e1``, ``e2`` (``e_i**2 = 1``).

Convention (Klein / modern PGA):

    point at (x, y, w=1)         P = w·e₁₂ - x·e₀₂ + y·e₀₁
    line  ax + by + c = 0         L = a·e₁ + b·e₂ + c·e₀
    ideal point in dir (x, y)     D = -x·e₀₂ + y·e₀₁
    line through P1, P2           L  = P1 & P2     (regressive)
    intersection L1 ∩ L2          P  = L1 ^ L2     (outer)
    reflection in line L          obj' = L · obj · L  (sandwich)

Example::

    from reals import CReal, pga
    P1 = pga.d2.point(CReal.PI, CReal.E)
    P2 = pga.d2.point(0, 0)
    L  = pga.d2.line_through(P1, P2)          # CReal-coefficient vector
    Lx = pga.d2.line(0, 1, 0)                 # x-axis (y = 0)
    Q  = pga.d2.reflect(P1, Lx)               # mirror P1 across the x-axis
    x, y = pga.d2.to_xy(Q)                    # → (CReal.PI, -CReal.E)
"""

from __future__ import annotations

from typing import Any, Union

try:
    from kingdon import Algebra
    _HAS_KINGDON = True
except ImportError:  # pragma: no cover
    _HAS_KINGDON = False
    Algebra = None  # type: ignore[assignment]

from reals._creal import CReal


__all__ = [
    "PGA",
    "e0", "e1", "e2",
    "point", "direction", "line",
    "line_through", "meet", "join",
    "reflect", "rotor_from_lines", "rotor_around", "translator",
    "motor", "apply",
    "to_xy", "normalize",
    "Number",
]


Number = Union[int, float, str, CReal]


def _require_kingdon() -> None:
    if not _HAS_KINGDON:
        raise ImportError(
            "reals.pga.d2 requires the 'kingdon' package. Install with: "
            "pip install kingdon"
        )


_require_kingdon()

PGA = Algebra(2, 0, 1)
"""The 2D PGA algebra instance. ``Cl(2, 0, 1)``."""

e0 = PGA.blades.e0   # null basis vector (e0**2 = 0)
e1 = PGA.blades.e1
e2 = PGA.blades.e2

_e01 = PGA.blades.e01
_e02 = PGA.blades.e02
_e12 = PGA.blades.e12


# ---------------------------------------------------------------------------
# Coefficient coercion (mirror of _pga.py)
# ---------------------------------------------------------------------------


def _coef(x: Number) -> Any:
    if isinstance(x, CReal):
        return x
    if isinstance(x, str):
        return CReal.valueOf(x)
    return x


def _has_creal(*xs: Any) -> bool:
    return any(isinstance(x, CReal) for x in xs)


def _maybe_promote(value: Number, others: tuple) -> Any:
    if _has_creal(*others) and not isinstance(value, CReal):
        if isinstance(value, (str, int, float)):
            return CReal.valueOf(value)
    return _coef(value)


# ---------------------------------------------------------------------------
# Constructors
# ---------------------------------------------------------------------------


def point(x: Number, y: Number, w: Number = 1) -> Any:
    """Projective point at affine coordinates ``(x, y)`` with weight ``w``.

    Default ``w=1`` produces a normalised Euclidean point. Use :func:`direction`
    for the ``w=0`` case (point at infinity).
    """
    others = (x, y, w)
    x_, y_, w_ = (_maybe_promote(v, others) for v in others)
    return w_ * _e12 - x_ * _e02 + y_ * _e01


def direction(x: Number, y: Number) -> Any:
    """Ideal point (direction) ``(x, y)``."""
    return point(x, y, w=0)


def line(a: Number, b: Number, c: Number) -> Any:
    """Line ``a·x + b·y + c = 0``."""
    others = (a, b, c)
    a_, b_, c_ = (_maybe_promote(v, others) for v in others)
    return a_ * e1 + b_ * e2 + c_ * e0


# ---------------------------------------------------------------------------
# Joins and meets
# ---------------------------------------------------------------------------


def line_through(p1: Any, p2: Any) -> Any:
    """Line through two points: ``P1 & P2`` (regressive product)."""
    return p1 & p2


def join(a: Any, b: Any) -> Any:
    """Regressive product (incidence / span)."""
    return a & b


def meet(a: Any, b: Any) -> Any:
    """Outer product (intersection). Lines meet at a point; parallel lines
    meet at an ideal point with weight 0."""
    return a ^ b


# ---------------------------------------------------------------------------
# Motions
# ---------------------------------------------------------------------------


def reflect(obj: Any, ln: Any) -> Any:
    """Reflect ``obj`` in line ``ln`` (sandwich product ``L · obj · L``).

    Pass a normalised line for a true isometry; an unnormalised line scales.
    """
    return ln.sw(obj)


def rotor_from_lines(l1: Any, l2: Any) -> Any:
    """Rotor that rotates by twice the angle between ``l1`` and ``l2``."""
    return l1 * l2


def rotor_around(center: Any, angle: Number) -> Any:
    """Rotor for rotation by ``angle`` (radians) around a Euclidean point.

    Built as ``exp(-angle/2 · C̃)`` where ``C̃`` is the centre point with its
    e₁₂ weight stripped to leave the pure-bivector rotation generator. May
    be slow when ``center`` carries CReal coefficients (kingdon's ``exp``
    is iterative).
    """
    half = _coef(angle)
    if isinstance(half, CReal):
        half = half * CReal.valueOf("0.5")
    else:
        half = 0.5 * half
    return (-half * center).exp()


def translator(dx: Number, dy: Number) -> Any:
    """Translator that shifts by ``(dx, dy)``.

    Closed form (no exp needed) because the translation generator squares
    to zero: ``T = 1 - ½·(dx·e₀₁ + dy·e₀₂)``. Apply via :func:`apply`.

    Sign sanity: under the Klein point convention ``P = w·e₁₂ - x·e₀₂ + y·e₀₁``,
    sandwich ``T·P·~T`` shifts the point's coordinates by ``+(dx, dy)``.
    """
    dx_ = _coef(dx)
    dy_ = _coef(dy)
    if isinstance(dx_, CReal) or isinstance(dy_, CReal):
        half = CReal.valueOf("0.5")
        if not isinstance(dx_, CReal):
            dx_ = CReal.valueOf(dx_)
        if not isinstance(dy_, CReal):
            dy_ = CReal.valueOf(dy_)
        return 1 - half * dx_ * _e01 - half * dy_ * _e02
    return 1 - 0.5 * dx_ * _e01 - 0.5 * dy_ * _e02


def motor(line_: Any, angle: Number) -> Any:
    """Screw motor (rotation about a Euclidean point — there's no separate
    translation axis in 2D PGA, so this is just :func:`rotor_around` if
    ``line_`` is a point and a translator if it's an ideal point).

    Provided for API symmetry with the 3D module.
    """
    half = _coef(angle)
    if isinstance(half, CReal):
        half = half * CReal.valueOf("0.5")
    else:
        half = 0.5 * half
    return (-half * line_).exp()


def apply(transform: Any, obj: Any) -> Any:
    """Apply a versor (rotor / translator / reflector) via sandwich product."""
    return transform.sw(obj)


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------


def normalize(mv: Any) -> Any:
    return mv.normalized()


def to_xy(p: Any) -> tuple:
    """Extract affine coordinates from a 2D PGA point.

    Returns ``(x, y)`` in the original coefficient type. Divides by the e₁₂
    weight so unnormalised points still yield their Euclidean projection.
    Raises ``ZeroDivisionError`` for ideal points (zero weight).
    """
    coefs = {k: v for k, v in zip(p.keys(), p.values())}
    w = coefs.get(_e12.keys()[0], 0)
    nx = coefs.get(_e02.keys()[0], 0)  # x → -e02
    y = coefs.get(_e01.keys()[0], 0)
    if w == 0 or (isinstance(w, CReal) and w.signum(-50) == 0):
        raise ZeroDivisionError("Point has zero weight (ideal point)")
    return (-nx / w, y / w)
