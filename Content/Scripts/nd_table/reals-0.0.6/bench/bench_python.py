"""Speed benchmark: CReal Python port vs mpmath.

ANALYSIS ONLY — this file is not imported by the package and is not part of
the test suite. Run directly:

    python bench/bench_python.py

The C++ counterparts (Boost.Multiprecision + MPFR, MPFUN20-MPFR) live in
``bench_boost_mpfr.cpp`` and ``bench_mpfun.cpp`` — build separately per the
README and compare the printed times.

Why mpmath as the comparison?
  - With ``gmpy2`` installed (``pip install gmpy2`` — comes with prebuilt
    GMP/MPFR DLLs in the wheel), mpmath autodetects it and routes all
    arbitrary-precision arithmetic through MPFR. The Python wrapper
    overhead is ~µs per op, which is invisible at any precision where the
    MPFR work itself takes longer than that.
  - In that mode, **these mpmath numbers ARE the MPFR numbers** — within
    a few percent of what a direct C++ ``bench_boost_mpfr`` would print.
  - Without gmpy2, mpmath falls back to pure-Python ints (still much
    better optimised than CReal — log_2 of the precision difference is the
    main factor — but not MPFR-fast).

Check ``mpmath.libmp.BACKEND`` in the output below: ``'gmpy'`` means MPFR
is in use, ``'python'`` means it isn't.

Operations: PI, E, sqrt(2), sin(1), ln(2), and the Boehm-paper showcase
``100000 * (22873*e - 19791*pi)``. Precisions: 50, 100, 500, 1000, 5000.

We time the *full digit-string production* — that's the unit of work users
care about (and the only thing CReal and mpmath both compute end-to-end).
"""

import os
import sys
import time

# Make the package importable from bench/ without installing.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from reals._creal import CReal
from reals._creal import gl_pi_CReal  # for cold PI

import mpmath
from mpmath import mp, mpf


PRECISIONS = [50, 100, 500, 1000, 5000]


# ---------------------------------------------------------------------------
# Timing helpers
# ---------------------------------------------------------------------------


def timeit(fn, *, target_seconds=0.5, warmups=1, repeats=3):
    """Run ``fn`` repeatedly; return the *minimum* wall-clock over runs.

    For very fast operations we'd ideally repeat thousands of times. CReal at
    5000 digits can take seconds, though — so we cap by elapsed budget rather
    than fixed repeat counts. Minimum (not mean) cancels out scheduler noise.
    """
    # Warm caches.
    for _ in range(warmups):
        fn()
    best = float("inf")
    elapsed = 0.0
    runs = 0
    while elapsed < target_seconds and runs < repeats:
        t0 = time.perf_counter()
        fn()
        dt = time.perf_counter() - t0
        elapsed += dt
        runs += 1
        if dt < best:
            best = dt
    return best


# ---------------------------------------------------------------------------
# CReal benchmark functions
# ---------------------------------------------------------------------------


def cr_pi(n):
    # Each call uses the cached PI singleton; toString re-scales for n.
    return CReal.PI.toString(n)


def cr_pi_cold(n):
    # Fresh AGM each time — no cache reuse. Apples-to-apples vs MPFR's
    # ``boost::math::constants::pi<>()`` which recomputes per call.
    return gl_pi_CReal().toString(n)


def cr_e(n):
    return CReal.E.toString(n)


def cr_e_cold(n):
    return CReal.ONE.exp().toString(n)


def cr_sqrt2(n):
    return CReal.valueOf(2).sqrt().toString(n)


def cr_sin1(n):
    return CReal.ONE.sin().toString(n)


def cr_ln2(n):
    return CReal.ln2.toString(n)


def cr_compound(n):
    expr = CReal.valueOf(100000) * (
        CReal.valueOf(22873) * CReal.E - CReal.valueOf(19791) * CReal.PI
    )
    return expr.toString(n)


# ---------------------------------------------------------------------------
# mpmath benchmark functions
# ---------------------------------------------------------------------------


def mp_pi(n):
    mp.dps = n + 10
    return mp.nstr(mp.pi, n)


def mp_e(n):
    mp.dps = n + 10
    return mp.nstr(mp.e, n)


def mp_sqrt2(n):
    mp.dps = n + 10
    return mp.nstr(mp.sqrt(2), n)


def mp_sin1(n):
    mp.dps = n + 10
    return mp.nstr(mp.sin(1), n)


def mp_ln2(n):
    mp.dps = n + 10
    return mp.nstr(mp.log(2), n)


def mp_compound(n):
    mp.dps = n + 10
    return mp.nstr(
        mpf(100000) * (mpf(22873) * mp.e - mpf(19791) * mp.pi),
        n,
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


BENCHES = [
    ("pi(cold)", cr_pi_cold,  mp_pi),
    ("pi(warm)", cr_pi,       mp_pi),
    ("e(cold)",  cr_e_cold,   mp_e),
    ("e(warm)",  cr_e,        mp_e),
    ("sqrt(2)",  cr_sqrt2,    mp_sqrt2),
    ("sin(1)",   cr_sin1,     mp_sin1),
    ("ln(2)",    cr_ln2,      mp_ln2),
    ("compound", cr_compound, mp_compound),
]


def main():
    print("# Python benchmark — CReal vs mpmath")
    print()
    print(f"Python {sys.version.split()[0]} / mpmath {mpmath.__version__}")
    print(f"mpmath backend: {mpmath.libmp.BACKEND}",
          "(gmpy2 not installed; using pure-Python ints)"
          if mpmath.libmp.BACKEND == "python" else "(using gmpy/gmpy2)")
    print()
    print("Times are minimum of 3 runs (post-warmup), in milliseconds.")
    print()
    header = (
        "| Operation | digits | CReal (ms) | mpmath (ms) | CReal / mpmath |"
    )
    sep = "|" + "|".join(["-" * len(c) for c in header.split("|")[1:-1]]) + "|"
    print(header)
    print(sep)

    rows = []
    for n in PRECISIONS:
        for name, cr_fn, mp_fn in BENCHES:
            cr_t = timeit(lambda: cr_fn(n))
            mp_t = timeit(lambda: mp_fn(n))
            ratio = cr_t / mp_t if mp_t > 0 else float("inf")
            rows.append((name, n, cr_t, mp_t, ratio))
            print(
                f"| {name:8} | {n:6} | {cr_t*1000:10.2f} | {mp_t*1000:11.2f} | "
                f"{ratio:13.0f}x |"
            )
    print()
    print("Save this table for comparison with bench_boost_mpfr.cpp output.")


if __name__ == "__main__":
    main()
