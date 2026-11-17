"""n-dimensional Projective Geometric Algebra (factory).

Mirrors the 2D / 3D modules' API for arbitrary spatial dimension ``n``,
producing ``Cl(n, 0, 1)`` PGAs. Used internally to expose ``pga.d9``
(9-dimensional Euclidean PGA) and reusable for any other ``n`` (≥ 1).

Klein convention generalised:

    point at (x_1, ..., x_n, w=1)
        P = w·I_E + Σ_{i=1..n} (-1)^i · x_i · (I_E with e_i replaced by e_0)

    where I_E = e_1 ∧ e_2 ∧ ... ∧ e_n   (Euclidean pseudoscalar)

    hyperplane  Σ a_i·x_i + d = 0
        π = a_1·e_1 + ... + a_n·e_n + d·e_0

    direction in (x_1,...,x_n)            P with w = 0  (ideal point)
    join (line/k-flat through points)      P1 & P2 & ...
    meet (intersection)                    A ^ B
    reflect ``obj`` in hyperplane π        π · obj · π        (via .sw)

For ``n = 2`` and ``n = 3`` the dedicated modules (``reals._pga2d`` and
``reals._pga``) expose nicer-named convenience functions (``line``/``plane``
etc.); prefer those when working in those dimensions.

This factory is index-limited to ``n ≤ 9`` so the kingdon-internal blade
names stay single-digit (``e012345678`` etc.). For ``n ≥ 10`` kingdon's
naming becomes ambiguous (``e10`` could be ``e_{1,0}`` or ``e_{10}``) and
this factory would need a different blade-lookup path.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Tuple, Union

try:
    from kingdon import Algebra
    from kingdon.multivector import MultiVector
    _HAS_KINGDON = True
except ImportError:  # pragma: no cover
    _HAS_KINGDON = False
    Algebra = None  # type: ignore[assignment]
    MultiVector = None  # type: ignore[assignment]

from reals._creal import CReal


__all__ = ["make_pga", "Number"]


Number = Union[int, float, str, CReal]


def _require_kingdon() -> None:
    if not _HAS_KINGDON:
        raise ImportError(
            "reals.pga.d<n> requires the 'kingdon' package. Install with: "
            "pip install kingdon"
        )


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


def _blade_key(indices: Tuple[int, ...]) -> int:
    """kingdon's integer-bitmask key for the wedge of basis vectors ``indices``.

    Bit ``i`` set ⇔ ``e_i`` is in the blade. Works at any dimension —
    kingdon's string-name access (e.g. ``alg.blades.e123``) collides at
    ``n ≥ 10`` because ``e10`` is ambiguous, but the underlying integer
    key is unambiguous up to ``n+1`` bits.
    """
    key = 0
    for i in indices:
        key |= 1 << i
    return key


def _blade_mv(alg: "Algebra", indices: Tuple[int, ...]) -> "MultiVector":
    """Build a unit-coefficient basis blade from its index tuple."""
    return MultiVector.fromkeysvalues(alg, (_blade_key(indices),), (1,))


def make_pga(n: int) -> SimpleNamespace:
    """Build a PGA(n, 0, 1) namespace with the standard Klein-convention API.

    Returns a ``SimpleNamespace`` (so users can do ``pga.d9.point(...)``)
    populated with:

    - ``PGA``            : the kingdon Algebra instance
    - ``n``              : spatial dimension
    - ``e0`` … ``e<n>``  : basis vectors as multivectors
    - ``point(*coords)`` : Euclidean point (length-``n`` coord list)
    - ``direction(*coords)`` : ideal point (weight 0)
    - ``hyperplane(*a, d)`` : ``a_1 x_1 + ... + a_n x_n + d = 0``
    - ``join(a, b)``, ``meet(a, b)`` : ``&`` and ``^``
    - ``reflect(obj, h)`` : sandwich product
    - ``apply(t, o)``     : sandwich (versor application)
    - ``to_coords(p)``    : ``(x_1, ..., x_n)`` tuple from a Klein point
    - ``normalize(mv)``   : divide by ``|mv|``
    """
    _require_kingdon()
    if n < 1:
        raise ValueError(f"make_pga: n must be ≥ 1; got {n}")
    # Algebras above ~16 are technically buildable but quickly become slow
    # (every operation walks 2**(n+1) basis blades). Raise this cap if you
    # actually need it.
    if n > 16:
        raise ValueError(
            f"make_pga: n > 16 is supported in principle but very slow; "
            f"raise the cap manually if needed. Got {n}."
        )

    alg = Algebra(n, 0, 1)

    ns = SimpleNamespace()
    ns.PGA = alg
    ns.n = n

    # Basis vectors as multivectors. Build by integer key so dims ≥ 10 work
    # (kingdon's attribute-style ``alg.blades.e10`` is ambiguous there).
    for i in range(n + 1):
        setattr(ns, f"e{i}", _blade_mv(alg, (i,)))

    # The Euclidean pseudoscalar I_E = e_1 ∧ ... ∧ e_n is the "weight" blade
    # for a point; the i-th coordinate blade is I_E with e_i replaced by e_0.
    weight_blade = _blade_mv(alg, tuple(range(1, n + 1)))
    coord_blades = [
        _blade_mv(alg, tuple([0] + [j for j in range(1, n + 1) if j != i]))
        for i in range(1, n + 1)
    ]

    # ---- constructors ------------------------------------------------------

    def point(*coords: Number, w: Number = 1) -> Any:
        if len(coords) != n:
            raise TypeError(
                f"point expects {n} coordinates (got {len(coords)})"
            )
        promo = tuple(_maybe_promote(c, coords + (w,)) for c in coords) + (
            _maybe_promote(w, coords + (w,)),
        )
        x = promo[:-1]
        w_ = promo[-1]
        result = w_ * weight_blade
        for i in range(n):
            # Klein-sign pattern matches the 3D module: coord_i gets (-1)^(i+1)
            # (using 1-indexed i; the factor here uses 0-indexed i and adds 1).
            sign = -1 if (i + 1) % 2 == 1 else 1
            result = result + sign * x[i] * coord_blades[i]
        return result

    def direction(*coords: Number) -> Any:
        return point(*coords, w=0)

    def hyperplane(*args: Number) -> Any:
        if len(args) != n + 1:
            raise TypeError(
                f"hyperplane expects {n + 1} args "
                f"(a_1, ..., a_{n}, d); got {len(args)}"
            )
        promo = tuple(_maybe_promote(v, args) for v in args)
        a = promo[:n]
        d = promo[n]
        result = d * getattr(ns, "e0")
        for i in range(n):
            result = result + a[i] * getattr(ns, f"e{i + 1}")
        return result

    # ---- operations --------------------------------------------------------

    def join(a: Any, b: Any) -> Any:
        return a & b

    def meet(a: Any, b: Any) -> Any:
        return a ^ b

    def reflect(obj: Any, h: Any) -> Any:
        return h.sw(obj)

    def apply(transform: Any, obj: Any) -> Any:
        return transform.sw(obj)

    def normalize(mv: Any) -> Any:
        return mv.normalized()

    # ---- inspection --------------------------------------------------------

    def to_coords(p: Any) -> tuple:
        coefs = dict(zip(p.keys(), p.values()))
        w_key = weight_blade.keys()[0]
        w = coefs.get(w_key, 0)
        if w == 0 or (isinstance(w, CReal) and w.signum(-50) == 0):
            raise ZeroDivisionError("Point has zero weight (ideal point)")
        out = []
        for i in range(n):
            sign = -1 if (i + 1) % 2 == 1 else 1
            k = coord_blades[i].keys()[0]
            c = coefs.get(k, 0)
            out.append(sign * c / w)
        return tuple(out)

    ns.point = point
    ns.direction = direction
    ns.hyperplane = hyperplane
    ns.join = join
    ns.meet = meet
    ns.reflect = reflect
    ns.apply = apply
    ns.normalize = normalize
    ns.to_coords = to_coords

    return ns
