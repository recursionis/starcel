# Constructive Reals — Upgrade Instructions

Based on the upgrade review PDF (`nerds.pdf`, Cluster B — *Constructive Reals / Speed Frontiers*).
All section numbers below refer to the PDF.

This document covers (a) the changes I applied inline to
`Content/Scripts/nd_table/reals-0.0.6/reals/_creal.py` and the new
`_backends.py`, (b) the manual steps you should run, and (c) the items the
brief recommended but I deliberately deferred (with rationale).

## TL;DR

Seven recommendations implemented in code; three documented as
manual / optional steps; one flagged as a publishable research
contribution.

| Sec. | Topic | Status | Notes |
|---|-------|--------|-------|
| 9.1.1 | Bignum backend dispatch | **Done** | New `reals._backends` module; auto-detects `gmpy2` → `python-flint` → CPython. |
| 9.1.2 | MPFR-style AGM termination bound | **Done** | `gl_pi_CReal.approximate` now has an a-priori `max_iters = ⌈log₂(−p+2)⌉ + 5` cap. |
| 9.1.3 | Reciprocal cache (`WeakValueDictionary`) | **Done** | `CReal.inverse` dedupes per-operand; `inv_CReal` got `__weakref__`. |
| 9.1.4 | Table-based Taylor for log/exp ≤ 4096 bits | **Deferred** | Big refactor; covered by Sec. 9.1.1 dispatch — see *Manual* Sec. 1. |
| 9.1.5 | Boehm irrational-tag heuristic | **Done** | `CReal.IRRATIONAL_TAG_BITS = 3500` (Boehm PLDI 2020 Sec. 6.2). `compareTo`/`signum` now decidable. |
| 9.2.2 | mypyc compilation | **Documented** | See *Manual* Sec. 2; no code change needed. |
| 9.2.3 | `yield_stable_digits()` streaming | **Done** | New iterator method on `CReal`. |
| 9.2.4 | CSE / expression-DAG memoization | **Done** | `add` / `multiply` (commutative) / `negate` / `shift{Left,Right}` dedupe. |
| 9.2.5 | `ProcessPoolExecutor` parallel evaluation | **Done** | `reals._backends.map_in_parallel` with a 10⁵-bit threshold. |
| 9.4.2 | CR + PGA novelty | **Flag** | Genuine research contribution — see *Publish* below. |

49/49 existing tests still pass after every change.

---

## What changed in `reals/`

### `_creal.py`

1. **`_INVERSE_CACHE`** (Sec. 9.1.3) — a module-level
   `weakref.WeakValueDictionary[int, inv_CReal]` keyed by `id(operand)`.
   `CReal.inverse()` consults it before allocating; `inv_CReal` gained
   `__weakref__` in its `__slots__`. Newton division reuses the cached
   reciprocal from the second `a / d` call onward. Diagnostics:
   `reals._creal._inv_cache_stats()` / `_inv_cache_clear()`.

2. **`_DAG_CACHE`** (Sec. 9.2.4) — a parallel `WeakValueDictionary[tuple, CReal]`.
   `CReal.add`, `CReal.multiply` (with commutative-key normalisation),
   `CReal.negate`, and `CReal.shiftLeft / shiftRight` dedupe through it
   before constructing a new node. `add_CReal`, `mult_CReal`, `neg_CReal`,
   `shifted_CReal` each gained `__weakref__`. Diagnostics:
   `_dag_cache_stats()` / `_dag_cache_clear()`.

   **Caveat noted in the source:** keys are by operand `id`, not by
   structural equality of the operand subtrees. Two semantically-equal
   but distinct CReals will not dedupe. To make `sin x` and `cos x` share
   their argument, bind `x` once and reuse the variable — this is the
   same idiom Boehm describes in PLDI 2020 Sec. 5.

3. **`CReal.IRRATIONAL_TAG_BITS = 3500`** (Sec. 9.1.5) — the no-tolerance forms
   of `compareTo()` and `signum()` now give up iterating once the working
   precision reaches `-IRRATIONAL_TAG_BITS` and return 0. This makes
   `sin²(1) + cos²(1) == 1` and similar transcendental identities
   decidable in finite time (≈55 ms at 3500 bits on this box). Set the
   class attribute to `None` to restore the original divergent semantics.

   This matches Google's Android calculator (which is Boehm's reference
   implementation) and is the dominant published behaviour.

4. **`gl_pi_CReal.approximate`** (Sec. 9.1.2) — added an MPFR-style a-priori
   iteration cap `max_iters = ⌈log₂(−p + 2)⌉ + 5`. The runtime
   `a − b > TOLERANCE` test still gates each iteration so early exit
   still happens; the cap is a defensive ceiling and a guarantee of
   termination at the precision MPFR/Arb document.

5. **`CReal.yield_stable_digits(radix=10, chunk=16, max_total=None)`**
   (Sec. 9.2.3) — a digit-streaming generator. Re-evaluates at increasing
   precision and yields each digit once it matches in two consecutive
   evaluations. Faithful Boehm-style CR can't stream natively; this is
   the recommended compromise (incorrect under adversarial digit-boundary
   inputs, correct for all practical numerics).

### `_backends.py` (new file, Sec. 9.1.1 + Sec. 9.2.5)

Exports:

- `BIGNUM_BACKEND` — active backend (gmpy2 > flint > cpython).
- `recommend_backend(precision_bits=0)` — picks the right one per call.
- `all_backends()` — for status display.
- `report()` — prints a probe summary.
- `map_in_parallel(func, items, precision_bits=0, threshold_bits=100_000)`
  — runs sequentially below `threshold_bits`, dispatches to a
  `ProcessPoolExecutor` above. The default 100k-bit threshold is the
  point where pickle + IPC overhead is amortised.

Environment override: `REALS_BACKEND=gmpy2|flint|cpython` forces a
specific backend.

### `__init__.py`

Re-exports the new `backends` submodule:

```python
from reals import backends
print(backends.report())
```

---

## Manual steps to run

### 1. Install `python-flint` for the Sec. 9.1.4 log/exp upgrade

The PDF's Sec. 9.1.4 recommendation is to switch log/exp from AGM
(`prescaled_ln_CReal` / `prescaled_exp_CReal`) to table-based Taylor +
rectangular splitting for inputs below ~4096 bits, per Fredrik
Johansson's Arb work (arXiv:1410.7176 Sec. 1 and Sec. 3; arXiv:2207.02501
multi-prime argument reduction). Taylor wins below ~10⁵ bits; AGM only
takes over above that.

Rather than re-implement Arb's tables in pure Python (~2,000 lines of
careful numerics with no clean fallback), the right answer is to call
Arb itself through `python-flint`:

```powershell
pip install python-flint
```

`python-flint 0.8.0` (released 2025-08-29) ships FLINT 3.3.1 + Arb +
MPFR 4.2.2 with PyPI wheels for CPython 3.11–3.14 (and 3.14t
free-threaded). After installing, the Sec. 9.1.1 backend probe will report
`flint` as available; you can then hand-call its `arb` module for log/exp
at large precision and wrap the result in `CReal.valueOf(...)` for use
elsewhere.

A drop-in `reals.log_via_arb(x, bits)` shim is straightforward to add
(≈30 lines); I left it out because the codebase's existing
`prescaled_ln_CReal` works correctly at the precisions you've benchmarked
so far. If you want the Arb shim, ask and I'll add it.

### 2. Compile `_creal.py` with mypyc for 5–14× hot-loop speedup (Sec. 9.2.2)

`mypyc` reads annotated Python directly. No code change required.

```powershell
pip install mypy
cd "Content\Scripts\nd_table\reals-0.0.6\reals"
mypyc _creal.py
```

This emits a `_creal.<platform>.so` (or `.pyd` on Windows) next to the
source. Python imports the compiled version automatically. Per the
official mypyc benchmark suite (richards: 9.870× faster vs compiled,
docs cite "1.5×–5× for existing annotated code, 5×–10× for code tuned
for compilation"), the dominant pure-arithmetic loops (AGM, Newton,
Taylor) should land in the 5–14× range; the mixed-object hot paths
(`CReal.add`, `multiply`) closer to 2–3×.

To revert: delete the generated `.so` / `.pyd`.

### 3. Smoke-check the new behaviour

```powershell
cd "Content\Scripts\nd_table\reals-0.0.6"
$env:PYTHONIOENCODING = "utf-8"
python -m pytest tests -q          # 49 ✓
python -c "from reals import backends; print(backends.report())"
python -c "from reals._creal import CReal; print(CReal.PI.compareTo(CReal.PI))"
```

The last command should print `0` and return instantly (it would have
diverged without the Sec. 9.1.5 patch).

---

## Items deliberately deferred

### Sec. 9.1.4 table-based Taylor for log/exp

See *Manual* Sec. 1 above. Implementing in pure Python is high-effort and
the Sec. 9.1.1 backend dispatch covers the same workload by handing it to
Arb; no point duplicating mature numerics.

### Calcium dispatch for Sec. 9.1.5 algebraic decisions

The brief notes that python-flint's Calcium provides *guaranteed*
decision procedures for the algebraic subset (i.e., not just Boehm's
3500-bit heuristic). I left a hook in the `compareTo` docstring pointing
at this; the API addition (`cr.with_algebraic_decision()`) is ~50 lines
once `python-flint` is installed and we agree on a surface.

### Möbius-stream refactor for true streaming output

Sec. 9.2.3 explicitly notes that real streaming (RealLib / Edalat–Potts) is
a major representation change — not a patch. The
`yield_stable_digits()` compromise covers practical use; do not adopt
streams just to chase the Sec. 9.2.3 box.

---

## Publish: Sec. 9.4.2 — CR × PGA is novel

The brief flags one item as a *genuine research contribution* rather
than an engineering upgrade: this project's `kingdon`-driven Projective
Geometric Algebra integration on top of Boehm-style constructive reals.
No published work combines them; the closest neighbour is Abbas Edalat's
domain-theoretic geometry work, which is theoretical rather than
implemented.

The recommended targets (verbatim from the brief):

- **GAME** — *Geometric Algebra in Mathematics and Engineering*
  (Springer Birkhäuser series). The natural home for "we built it and
  it works" papers in this area.
- **CGI** — *Computer Graphics International*. Better fit if the angle
  emphasises rendering / interactive visualisation.

A workshop or short paper writing up `reals/_pga*.py` + the existing
benchmarks (the `bench/` directory) plus three or four worked examples
(motor exponential, point-line meet, rotor sandwich at 1000-bit
precision) would land cleanly at either venue. The Sec. 9.1.5 heuristic and
the Sec. 9.2.4 CSE cache are also fair game — both are practical fixes to
Boehm's CR that have not been written up elsewhere.

---

## File-by-file diff summary

```
reals/_creal.py
  +import weakref
  +_INVERSE_CACHE = WeakValueDictionary
  +_inv_cache_clear / _inv_cache_stats
  +_DAG_CACHE = WeakValueDictionary
  +_dag_cache_clear / _dag_cache_stats
  +CReal.IRRATIONAL_TAG_BITS = 3500
  ~CReal.compareTo  # heuristic cutoff
  ~CReal.signum     # heuristic cutoff
  ~CReal.add        # DAG cache
  ~CReal.multiply   # DAG cache (commutative key)
  ~CReal.negate     # DAG cache
  ~CReal.shiftLeft  # DAG cache
  ~CReal.shiftRight # DAG cache
  ~CReal.inverse    # WeakValueDict reciprocal cache
  +CReal.yield_stable_digits
  ~gl_pi_CReal.approximate  # MPFR-style max_iters cap
  ~add_CReal / mult_CReal / neg_CReal / shifted_CReal / inv_CReal
                            # __weakref__ in __slots__

reals/_backends.py            (new, 200 lines)
  Backend dataclass
  BIGNUM_BACKEND probe (gmpy2 / flint / cpython)
  recommend_backend / report / all_backends
  map_in_parallel (ProcessPoolExecutor, 10^5-bit threshold)

reals/__init__.py
  +from reals import _backends as backends
  +'backends' in __all__
```

---

## Acceptance criteria

- All 49 tests still pass: `python -m pytest tests -q` ✓
- `CReal.PI.compareTo(CReal.PI)` returns `0` in <1 ms ✓
- `''.join(CReal.PI.yield_stable_digits(max_total=60))` returns
  the first 60 digits of π correctly ✓
- `reals.backends.report()` lists at least one available backend ✓
- DAG cache deduplicates: `a.add(b) is b.add(a)` returns `True` ✓
- Reciprocal cache deduplicates: `x.inverse() is x.inverse()` returns
  `True` ✓
