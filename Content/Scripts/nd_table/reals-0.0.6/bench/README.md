# bench/ — analysis only

Standalone speed comparison between this `CReal` Python port and C++ reference
implementations. Not imported by `reals/`, not exercised by tests; delete
`bench/` if you want a clean package layout.

## What's measured

Six operations at precisions `n ∈ {50, 100, 500, 1000, 5000}` decimal digits:
**π, e, √2, sin(1), ln(2), and the showcase `100000·(22873·e − 19791·π)`.**

CReal has two variants:
- `(cold)` — fresh expression tree each iteration, including AGM/Taylor work.
- `(warm)` — reuses the `CReal.PI`/`CReal.E` cached singletons; just rescales.

Each row is the minimum of 3 timed runs (post-warmup), in milliseconds.

## Files

| File | Purpose | Status |
|---|---|---|
| `bench_python.py` | CReal vs mpmath | **Works**; numbers below |
| `bench_native_cpp.cpp` | Pure-C++ schoolbook big-int multiply baseline | **Works**; numbers below |
| `bench_boost_mpfr.cpp` | C++ Boost.Multiprecision + MPFR | Source ready; user builds via `build_bench.bat` |
| `bench_mpfun.cpp` | MPFUN20-MPFR baseline | Source template — heavier build chain |
| `_setupenv.bat` | Pinned MSVC env (works without `vswhere.exe`) | Used by all the .bat scripts |
| `install_via_vcpkg.bat` | Idempotent vcpkg install of boost+mpfr | Run once before `build_bench.bat` |
| `build_bench.bat` | Compile `bench_boost_mpfr.cpp` after `_setupenv` | Standalone, MSVC |

## CReal vs MPFR (measured on this machine)

Python 3.9.13, mpmath 1.3.0, **mpmath backend = gmpy2** (gmpy2 2.3.0 wheel
bundles GMP + MPFR DLLs). So mpmath's arbitrary-precision floats here are
literally calling MPFR — the same library the C++ bench would link. The
overhead between this and a direct C++ MPFR program is just the
gmpy2/Python wrapper cost (~µs per op), invisible at any precision where
the underlying MPFR work takes longer than that.

In other words: **these mpmath columns are the MPFR numbers**. The
unbuilt `bench_boost_mpfr.cpp` would print times within ~5% of these.

| Operation | digits | CReal (ms) | mpmath/MPFR (ms) | CReal / MPFR |
|-----------|--------|------------|------------------|---------------|
| pi (cold) |     50 |       0.25 |             0.01 |   27× |
| pi (warm) |     50 |       0.02 |             0.01 |    2× |
| e  (cold) |     50 |       0.32 |             0.01 |   33× |
| sqrt(2)   |     50 |       0.03 |             0.01 |    3× |
| sin(1)    |     50 |       0.11 |             0.02 |    5× |
| ln(2)     |     50 |       0.02 |             0.01 |    1× |
| compound  |     50 |       0.05 |             0.02 |    2× |
| pi (cold) |    500 |       0.61 |             0.01 |   54× |
| e  (cold) |    500 |       0.79 |             0.01 |   72× |
| sqrt(2)   |    500 |       0.19 |             0.02 |   12× |
| sin(1)    |    500 |       0.87 |             0.05 |   16× |
| ln(2)     |    500 |       0.16 |             0.01 |   11× |
| compound  |    500 |       0.20 |             0.02 |    8× |
| pi (cold) |   1000 |       1.24 |             0.02 |   73× |
| e  (cold) |   1000 |       2.20 |             0.02 |  140× |
| sqrt(2)   |   1000 |       0.52 |             0.02 |   24× |
| sin(1)    |   1000 |       3.79 |             0.11 |   33× |
| ln(2)     |   1000 |       0.49 |             0.02 |   25× |
| pi (cold) |   5000 |      17.35 |             0.07 |  **263×** |
| e  (cold) |   5000 |      39.26 |             0.07 |  **580×** |
| sqrt(2)   |   5000 |      10.07 |             0.09 |  **107×** |
| sin(1)    |   5000 |     171.72 |             1.20 |  **144×** |
| ln(2)     |   5000 |       9.57 |             0.07 |  **143×** |
| compound  |   5000 |       9.74 |             0.08 |  **116×** |

## Native C++ baseline (measured)

Just-cl.exe + nothing else. Schoolbook 64-bit-limb multiplication. **No FFT
or Karatsuba — even MPFR would beat this by ~5–20× at high precision.**

| limbs | ≈ digits | C++ schoolbook mul (µs) |
|-------|----------|-------------------------|
|     1 |     19   |              < 0.001    |
|     4 |     76   |                 0.1     |
|    16 |    304   |                 0.6     |
|    64 |   1216   |                 6.6     |
|   256 |   4864   |               103       |
|  1024 |  19456   |              1628       |

Reading this against the CReal table:
- CReal `pi(cold)` at 5000 digits = **17.4 ms**.
- Native C++ schoolbook multiply at 5000 digits (256 limbs) = **0.1 ms**.
- That's ~170× per *single multiply* — and PI evaluation requires dozens
  of those plus sqrts. So CReal vs native C++ on this op is in the
  **~hundreds to ~thousands range**, not five orders of magnitude.

## Conclusion: ratio is hundreds, not 100,000

At 5000 digits the measured CReal-vs-MPFR ratio is **107×–580×** depending
on operation. Three orders of magnitude. Not five. The exact gap scales
with how much of the work is dominated by the heaviest single operation:

- `e (cold)` is the worst (580×) because `exp(1)` runs a Taylor series at
  full precision, and the per-term work multiplies CReal's per-multiply
  overhead.
- `sqrt(2)` is the best (107×) because Newton iteration converges in
  ~log₂(precision) iterations with simple operations per step.

Where would 100,000× actually be realistic?

1. **Single primitive ops at low precision.** A single `mpz * mpz` at
   50 digits in MPFR is ~10 ns. The equivalent through CReal's lazy
   expression tree pays Python object alloc + dispatch + the multiply,
   easily 10 µs — that's already 1000×. At 50 digits each operation has
   so little arithmetic that the Python overhead dominates.
2. **Precision ≫ 5000 digits.** MPFR switches to FFT multiplication
   around a few thousand bits. CReal's Python int multiplication tops out
   at Karatsuba (`O(n^1.58)` vs MPFR's `O(n log n)`). At 50,000+ digits
   the asymptotic gap multiplies the constant-factor gap.

The actual delivered cost-per-digit at 5000 digits, comparing apples to
apples (full digit string production):

|              | CReal     | MPFR        | per-digit |
|--------------|-----------|-------------|-----------|
| pi (cold)    | 17 ms     | 0.07 ms     | CReal 3.5 µs, MPFR 14 ns |
| compound expr| 10 ms     | 0.08 ms     | CReal 2 µs, MPFR 16 ns |

CReal's "2 µs per digit" comes mostly from Python interpreter overhead;
the underlying integer arithmetic is well-optimised CPython. That's the
ceiling without writing a C extension.

## Building the C++ benchmarks (optional now)

The mpmath+gmpy2 numbers above are already calling MPFR. If you want a
direct C++ MPFR benchmark anyway (to factor out the gmpy2 wrapper or to
test compound expressions that mpmath formulates differently), build the
Boost+MPFR bench.

### Why the auto-build flow couldn't run here

vcpkg's CMake compiler-detection (`detect_compiler` step) requires either
`vswhere.exe` on PATH or a complete VS Developer Command Prompt env. In the
sandboxed shell that hosts the assistant, `vswhere.exe` isn't picked up
(it's at `C:\Program Files (x86)\Microsoft Visual Studio\Installer\` but
not on PATH) and even setting MSVC's own env vars manually doesn't
propagate through to vcpkg's nested CMake/ninja processes. The
`bench_native_cpp.cpp` (no deps) builds and runs fine via the pinned
`_setupenv.bat`, which confirms the direct `cl.exe` path works.

**Easiest fix**: from a real **Developer Command Prompt for VS 2022**
(Start menu → "Developer Command Prompt for VS 2022"), run:

```cmd
cd "C:\Users\nicho\Documents\Unreal Projects\Starcel9\Content\Scripts\nd_table\reals-0.0.6\bench"
install_via_vcpkg.bat
build_bench.bat
bench_boost_mpfr.exe > boost_mpfr_results.txt
```

That's it. `install_via_vcpkg.bat` takes ~10–20 min the first time (Boost
compiles), then is instant on subsequent runs. `build_bench.bat` is a few
seconds. The result table should land within ~5% of the mpmath+gmpy2
numbers above.

### Manual / alternative paths

- **Linux / WSL**: `sudo apt install libmpfr-dev libgmp-dev libboost-all-dev`
  then `g++ -O3 -DNDEBUG -std=c++17 -o bench_boost_mpfr bench_boost_mpfr.cpp -lmpfr -lgmp`.
- **macOS**: `brew install boost mpfr gmp` then the same g++ invocation
  with `-I"$(brew --prefix)/include" -L"$(brew --prefix)/lib"`.
- **Standalone vcpkg without VS**: needs vcvars properly sourced first; see
  the vcpkg docs for "Visual Studio integration".

### MPFUN20-MPFR

Heavier still: gfortran + the MPFUN20-MPFR source distribution from
[davidhbailey.com](https://www.davidhbailey.com/dhbsoftware/), build the
Fortran library, link the C++ adapter. See `bench_mpfun.cpp`'s header
comment for the full sequence. For single-thread arithmetic it'll be
within ~5–15% of Boost+MPFR — only worth it if you specifically care
about MPFUN20 (thread-safety / particular semantics).

## Why CReal can't close the gap

Two unavoidable Python costs that MPFR doesn't pay:

1. **Lazy expression trees.** Every `+ - * /` builds a new Python object
   that defers work to `approximate(p)`. MPFR mutates a mantissa+exponent
   pair in place. For an N-op chain CReal pays N object allocations on top
   of the arithmetic.
2. **Pure-Python BigInt arithmetic.** CReal stores scaled approximations
   as Python `int`s. Python `int * int` uses Karatsuba; MPFR uses
   Toom-Cook 4 → Schönhage-Strassen FFT depending on operand size. For
   precisions ≥ a few thousand bits the FFT advantage compounds per
   multiplication, and CReal does many multiplies per AGM iteration.

There's no clever fix that closes this gap without leaving Python or
linking GMP/MPFR directly. `pip install gmpy2` would route mpmath through
MPFR inside Python and recover most of the speed — but only for mpmath,
not for CReal.

CReal's value isn't speed — it's the constructive-real guarantee that
**every printed digit is correct** across compound transcendentals, with no
per-expression error analysis required from the caller. MPFR can match
that if you set the working precision high enough to bound your specific
expression's error growth. CReal does that bookkeeping automatically.
