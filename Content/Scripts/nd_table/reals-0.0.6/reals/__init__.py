from reals._real import Real
from reals._constants import e, phi, pi
from reals._exponential import exp
from reals._logarithm import log
from reals._sqrt import sqrt
from reals._trigonometric import sin, sinh, csc, csch, cos, cosh, sec, sech, tan, tanh, cot, coth
from reals._creal import CReal
from reals import _backends as backends  # Sec. 9.1.1 / Sec. 9.2.5 — optional dispatch

# PGA integration via kingdon. Imported lazily so the package still loads if
# kingdon isn't installed — users who want PGA opt in with ``from reals import pga``.
# ``pga`` exposes 3D PGA at the top level (backward compatible). 2D PGA is at
# ``pga.d2``; ``pga.d3`` is a self-alias for symmetry. Higher-dimensional PGAs
# (``pga.d4`` through ``pga.d9``) are built lazily via the n-D factory.
try:
    from reals import _pga as pga  # noqa: F401
    from reals import _pga2d
    from reals._pga_nd import make_pga as _make_pga
    pga.d2 = _pga2d
    pga.d3 = pga
    # Spatial dims 4..16 share the generic Klein-convention factory. Built
    # eagerly because kingdon Algebra construction is cheap; the heavy work
    # (blade enumeration, codegen) is deferred to first operation. At n≈16
    # operations begin to slow noticeably (Cl(16,0,1) has 2**17 = 131,072
    # basis blades), but they're correct.
    for _n in range(4, 17):
        setattr(pga, f"d{_n}", _make_pga(_n))
    pga.make_pga = _make_pga
    del _n
except ImportError:
    pga = None  # type: ignore[assignment]

__all__ = ['Real', 'CReal', 'pga', 'backends', 'e', 'phi', 'pi', 'exp', 'log', 'sqrt', 'sin', 'sinh', 'csc', 'csch',
           'cos', 'cosh', 'sec', 'sech', 'tan', 'tanh', 'cot', 'coth']
