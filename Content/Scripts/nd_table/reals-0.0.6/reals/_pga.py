"""3D Projective Geometric Algebra with CReal coefficients.

Bridges the ``kingdon`` PGA implementation to this package's ``CReal``
constructive-real type so PGA computations can run at arbitrary precision.
Floats also work — the module accepts either, and converts on demand.

Algebra: ``Cl(3, 0, 1)`` (kingdon ``Algebra(3, 0, 1)``).
Basis: ``e0`` (null, ``e0**2 = 0``), ``e1``, ``e2``, ``e3`` (``e_i**2 = 1``).

Convention (Klein / modern PGA):

    point at (x, y, z, w=1)         P  = w·e₁₂₃ - x·e₀₂₃ + y·e₀₁₃ - z·e₀₁₂
    plane  ax + by + cz + d = 0     pi = a·e₁ + b·e₂ + c·e₃ + d·e₀
    ideal point ("direction")        D  = -x·e₀₂₃ + y·e₀₁₃ - z·e₀₁₂
    line through P1, P2              L  = P1 & P2     (regressive)
    plane through P1, P2, P3         pi = P1 & P2 & P3
    intersection of planes pi1, pi2   L  = pi1 ^ pi2   (outer)
    reflection in plane pi            obj' = pi · obj · pi  (sandwich)

All constructors accept ``int``, ``float``, ``str`` (parsed exactly), or
``CReal``. Pass a single ``CReal`` anywhere and the whole result tree carries
that precision through kingdon's symbolic-friendly arithmetic.

Example::

    from reals import CReal, pga
    P1 = pga.point(CReal.PI, CReal.E, CReal.valueOf(2).sqrt())
    P2 = pga.point(0, 0, 0)
    L  = pga.line(P1, P2)                  # CReal-coefficient bivector
    pi = pga.plane(1, 0, 0, -1)            # plane x = 1
    Q  = pga.reflect(P1, pi)               # mirror P1 across x=1

Limitations:
- Requires ``kingdon >= 1.4``. ``ImportError`` if not installed.
- Heavy operations (e.g. ``exp`` of a CReal-coefficient bivector) may be
  slow — kingdon doesn't specialise for our type, so each scalar coefficient
  goes through the full constructive-real machinery.
"""

from __future__ import annotations

from typing import Any, Union

try:
    from kingdon import Algebra
    _HAS_KINGDON = True
except ImportError:  # pragma: no cover - import-time only
    _HAS_KINGDON = False
    Algebra = None  # type: ignore[assignment]

from reals._creal import CReal


__all__ = [
    "PGA",
    "e0", "e1", "e2", "e3",
    "point", "direction", "plane",
    "line", "plane_through", "meet", "join",
    "reflect", "rotor_from_planes", "motor", "apply",
    "to_xyz", "normalize",
    "Number",
]


Number = Union[int, float, str, CReal]


# ---------------------------------------------------------------------------
# Algebra setup
# ---------------------------------------------------------------------------


def _require_kingdon() -> None:
    if not _HAS_KINGDON:
        raise ImportError(
            "reals.pga requires the 'kingdon' package. Install with: "
            "pip install kingdon"
        )


_require_kingdon()

PGA = Algebra(3, 0, 1)
"""The 3D PGA algebra instance. ``Cl(3, 0, 1)``."""

e0 = PGA.blades.e0  # null basis vector (e0**2 = 0)
e1 = PGA.blades.e1
e2 = PGA.blades.e2
e3 = PGA.blades.e3

_e123 = PGA.blades.e123
_e023 = PGA.blades.e023
_e013 = PGA.blades.e013
_e012 = PGA.blades.e012


# ---------------------------------------------------------------------------
# Coefficient coercion
# ---------------------------------------------------------------------------


def _coef(x: Number) -> Any:
    """Pass through CReal/int/float; parse strings as exact decimals.

    We deliberately leave plain ``int`` and ``float`` untouched so kingdon's
    optimised numeric paths apply when the user hasn't asked for arbitrary
    precision. Once a single ``CReal`` enters the expression tree, kingdon's
    operator-protocol falls back to ``CReal.__rmul__``/``__radd__`` and the
    whole result carries CReal precision.
    """
    if isinstance(x, CReal):
        return x
    if isinstance(x, str):
        return CReal.valueOf(x)
    return x  # int / float / anything else kingdon can handle


def _has_creal(*xs: Any) -> bool:
    return any(isinstance(x, CReal) for x in xs)


def _maybe_promote(value: Number, others: tuple) -> Any:
    """If any partner is CReal, promote ``value`` so arithmetic stays exact."""
    if _has_creal(*others) and not isinstance(value, CReal):
        if isinstance(value, str):
            return CReal.valueOf(value)
        if isinstance(value, (int, float)):
            return CReal.valueOf(value)
    return _coef(value)


# ---------------------------------------------------------------------------
# Element constructors
# ---------------------------------------------------------------------------


def point(x: Number, y: Number, z: Number, w: Number = 1) -> Any:
    """Projective point at affine coordinates ``(x, y, z)``.

    With the default ``w=1`` you get a Euclidean point; ``w=0`` would
    degenerate to an ideal point — use :func:`direction` for that instead.
    """
    others = (x, y, z, w)
    x_, y_, z_, w_ = (_maybe_promote(v, others) for v in others)
    return w_ * _e123 - x_ * _e023 + y_ * _e013 - z_ * _e012


def direction(x: Number, y: Number, z: Number) -> Any:
    """Ideal point ("point at infinity") in direction ``(x, y, z)``."""
    return point(x, y, z, w=0)


def plane(a: Number, b: Number, c: Number, d: Number) -> Any:
    """Plane ``a·x + b·y + c·z + d = 0``."""
    others = (a, b, c, d)
    a_, b_, c_, d_ = (_maybe_promote(v, others) for v in others)
    return a_ * e1 + b_ * e2 + c_ * e3 + d_ * e0


# ---------------------------------------------------------------------------
# Joins and meets
# ---------------------------------------------------------------------------


def line(p1: Any, p2: Any) -> Any:
    """Line through two points: ``P1 & P2`` (regressive product)."""
    return p1 & p2


def plane_through(p1: Any, p2: Any, p3: Any) -> Any:
    """Plane through three points: ``P1 & P2 & P3``."""
    return p1 & p2 & p3


def join(a: Any, b: Any) -> Any:
    """Regressive product of two PGA elements (incidence / span)."""
    return a & b


def meet(a: Any, b: Any) -> Any:
    """Outer product of two PGA elements (intersection)."""
    return a ^ b


# ---------------------------------------------------------------------------
# Motions
# ---------------------------------------------------------------------------


def reflect(obj: Any, pi: Any) -> Any:
    """Reflect ``obj`` in plane ``pi`` via the sandwich product.

    Uses kingdon's ``sw`` (sandwich) operator: ``pi.sw(obj)`` computes
    ``pi · obj · pi`` (with the appropriate sign for grade-preservation).
    For an unnormalised plane this scales the result; pass a normalised
    plane (``pi / |pi|``) when you need a true isometry.
    """
    return pi.sw(obj)


def rotor_from_planes(pi1: Any, pi2: Any) -> Any:
    """Rotor that rotates by twice the dihedral angle from ``pi1`` to ``pi2``.

    The rotor is just the geometric product ``pi1 · pi2`` (both planes
    assumed normalised). Apply via ``apply(R, obj)``.
    """
    return pi1 * pi2


def motor(line_: Any, angle: Number) -> Any:
    """Screw motor about ``line_`` by ``angle`` radians.

    Built as ``exp(-angle/2 · L)``. Requires kingdon's ``exp`` to converge;
    for symbolic CReal coefficients this can be slow. For Euclidean
    rotations (line through origin) this is a pure rotor.
    """
    half = _coef(angle)
    if isinstance(half, CReal):
        half = half * CReal.valueOf("0.5")
    else:
        half = 0.5 * half
    return (-half * line_).exp()


def apply(transform: Any, obj: Any) -> Any:
    """Apply a versor (rotor / motor / reflector) via sandwich product."""
    return transform.sw(obj)


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------


def normalize(mv: Any) -> Any:
    """Divide by ``|mv|`` (kingdon ``normalized``). Falls back gracefully."""
    return mv.normalized()


def to_xyz(p: Any) -> tuple:
    """Extract affine coordinates from a (Klein-convention) PGA point.

    Returns ``(x, y, z)`` as the original coefficient type (``CReal`` or
    float). Divides by the ``e₁₂₃`` weight so an unnormalised point still
    yields its Euclidean projection. Raises ``ZeroDivisionError`` for
    ideal points (zero weight).
    """
    coefs = {k: v for k, v in zip(p.keys(), p.values())}
    # Kingdon's blade index for e123, e023, e013, e012:
    w = coefs.get(_e123.keys()[0], 0)
    nx = coefs.get(_e023.keys()[0], 0)  # coefficient of e023, recall x → -e023
    y = coefs.get(_e013.keys()[0], 0)
    nz = coefs.get(_e012.keys()[0], 0)  # coefficient of e012, recall z → -e012
    if w == 0 or (isinstance(w, CReal) and w.signum(-50) == 0):
        raise ZeroDivisionError("Point has zero weight (ideal point)")
    return (-nx / w, y / w, -nz / w)
