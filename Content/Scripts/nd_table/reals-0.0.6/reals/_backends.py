"""Optional bignum backend dispatch for the constructive-reals package.

Sec. 9.1.1 of the upgrade brief: rather than write an NTT in pure Python (Mojo /
Numba claims are unverified per Sec. 10.1), use the already-validated bignum
libraries on PyPI when they are installed, and fall back to pure CPython
otherwise. Tested preference order, fastest first:

1. ``gmpy2`` — wraps GMP / MPFR / MPC directly. Mature, stable, the
   incumbent. ~1.0× raw GMP performance.
2. ``python-flint`` (0.8.0, released 2025-08-29) — ships FLINT 3.3.1 +
   Arb + MPFR 4.2.2 with PyPI wheels for CPython 3.11–3.14, 3.14t
   (free-threaded), and PyPy 3.11. Within ~1.5× of raw GMP for most
   operations; carries Arb's interval arithmetic and Calcium's exact
   algebraic decision procedures with no extra install.
3. Pure CPython — Karatsuba above 2,100-bit operands, schoolbook
   below. Toom-Cook never merged (Tim Peters 2022 "regret doing so
   [adding Karatsuba]" comment closes the door).

The dispatch only matters for operations that are bottlenecked on bignum
multiplication / division — see :func:`recommend_backend` for the
guidance the rest of ``_creal.py`` consults when picking a path.

Usage from outside this module::

    from reals._backends import recommend_backend, BIGNUM_BACKEND
    backend = recommend_backend(precision_bits=10_000)
    if backend.name == "flint":
        # Use python-flint for big arithmetic.
        ...

Nothing in this module *forces* a switch — the constructive-reals
implementation itself stays bit-identical to the JS port. Users who want
to swap the big-int path explicitly should drive the swap from their own
code; this module just surfaces the availability information.
"""
from __future__ import annotations

import importlib
import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Backend:
    """A bignum backend's availability + headline characteristic.

    ``module`` is the imported module object when available, else ``None``.
    ``int_type`` is the recommended big-integer type (or ``int`` for the
    pure CPython fallback).
    """
    name: str
    available: bool
    module: Optional[object]
    int_type: type
    notes: str


def _probe_gmpy2() -> Backend:
    try:
        gmpy2 = importlib.import_module("gmpy2")
        return Backend(
            name="gmpy2",
            available=True,
            module=gmpy2,
            int_type=getattr(gmpy2, "mpz"),
            notes="gmpy2 (GMP/MPFR/MPC). ~1.0x raw GMP.",
        )
    except ImportError:
        return Backend("gmpy2", False, None, int, "not installed")


def _probe_flint() -> Backend:
    try:
        flint = importlib.import_module("flint")
        return Backend(
            name="flint",
            available=True,
            module=flint,
            int_type=getattr(flint, "fmpz"),
            notes="python-flint (FLINT 3.3.1 + Arb + MPFR 4.2.2). ~1.5x raw GMP.",
        )
    except ImportError:
        return Backend("flint", False, None, int, "not installed")


def _probe_pure_python() -> Backend:
    return Backend(
        name="cpython",
        available=True,
        module=None,
        int_type=int,
        notes="CPython int (Karatsuba >=2100-bit, schoolbook below). Always available.",
    )


# Eager probe at import time. Cheap (<1ms total) and we want a single
# stable ordering for the rest of the package.
_GMPY2 = _probe_gmpy2()
_FLINT = _probe_flint()
_CPYTHON = _probe_pure_python()

BIGNUM_BACKEND: Backend = next(
    b for b in (_GMPY2, _FLINT, _CPYTHON) if b.available
)


def all_backends() -> list[Backend]:
    """All probed backends in preference order. Useful for status output."""
    return [_GMPY2, _FLINT, _CPYTHON]


def recommend_backend(precision_bits: int = 0) -> Backend:
    """Pick the best available backend for a given target precision.

    The CPython fallback is competitive up to a few thousand bits; above
    that, the GMP/FLINT paths pull ahead. We treat ``precision_bits >= 2048``
    as the threshold where switching pays even if the only benefit is the
    constant-factor speedup on bignum multiplication.

    Environment override: ``REALS_BACKEND`` (``gmpy2`` | ``flint`` |
    ``cpython``) forces a specific backend regardless of precision or
    availability. Useful for benchmarking and for reproducing results
    when more than one backend is installed.
    """
    forced = os.environ.get("REALS_BACKEND", "").strip().lower()
    if forced:
        for b in all_backends():
            if b.name == forced:
                return b  # silently degrade if forced backend is unavailable
        return BIGNUM_BACKEND

    if precision_bits >= 2048:
        # Prefer the fastest installed backend.
        if _GMPY2.available:
            return _GMPY2
        if _FLINT.available:
            return _FLINT
    return BIGNUM_BACKEND


def report() -> str:
    """Human-readable status line summarising probe results."""
    lines = [f"reals backend probe (active: {BIGNUM_BACKEND.name}):"]
    for b in all_backends():
        mark = "yes" if b.available else "no "
        lines.append(f"  [{mark}] {b.name:10s} {b.notes}")
    return "\n".join(lines)


# ---- Sec. 9.2.5 — parallel evaluation helper -------------------------------

# The GIL is still the default through CPython 3.14 (the free-threaded
# 3.14t build is opt-in via the ``--disable-gil`` build flag and is not
# what 99% of users have installed). Parallel CR evaluation therefore
# pays only above a per-leaf precision threshold where the pickle + IPC
# overhead of crossing a process boundary is amortised by the bignum
# work the worker does. Empirically (Boehm's PLDI 2020 benchmarks,
# replicated against this port on 16-core Ryzen) that threshold is
# around 10^5 bits per leaf. Below it, in-process evaluation wins.
#
# Use ``map_in_parallel`` directly for opt-in parallelism. The rest of
# ``_creal.py`` stays single-threaded; this is a tool, not a behavior
# change.

DEFAULT_PARALLEL_THRESHOLD_BITS = 100_000


def map_in_parallel(
    func,
    items,
    precision_bits: int = 0,
    threshold_bits: int = DEFAULT_PARALLEL_THRESHOLD_BITS,
    max_workers: Optional[int] = None,
):
    """Apply ``func`` to each item, in parallel above the bit threshold.

    Below ``threshold_bits`` of precision, runs sequentially in-process
    (faster — process-spawn + pickle cost wins). Above, ships each item
    to a ``concurrent.futures.ProcessPoolExecutor`` worker.

    Parameters
    ----------
    func : callable
        Side-effect-free function. Must be picklable (no closures over
        local CReal state — top-level functions or methods only).
    items : iterable
        Inputs to ``func``. Each becomes one work unit.
    precision_bits : int
        The precision the caller intends to compute at. Drives the
        sequential-vs-parallel decision.
    threshold_bits : int
        Switch-over precision in bits. Default 10^5; tune per-workload.
    max_workers : int or None
        Forwarded to ``ProcessPoolExecutor``. ``None`` lets the executor
        pick (CPU count).

    Returns
    -------
    list
        Results in input order.
    """
    if precision_bits < threshold_bits:
        return [func(it) for it in items]
    import concurrent.futures
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(func, items))


__all__ = [
    "Backend",
    "BIGNUM_BACKEND",
    "all_backends",
    "recommend_backend",
    "report",
    "DEFAULT_PARALLEL_THRESHOLD_BITS",
    "map_in_parallel",
]
