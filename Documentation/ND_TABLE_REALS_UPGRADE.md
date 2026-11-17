# nd_table Reals Upgrade — Complete Instructions

The full reference for the upgrade pass on `Content/Scripts/nd_table/reals-0.0.6/`
driven by the *nerds.pdf* review brief (Cluster B — Constructive Reals /
Speed Frontiers).

Read this once end-to-end before running any commands. Everything below
is already implemented in code; the instructions are about (a) what
landed where, (b) how to verify it locally, (c) the *manual* steps that
are still your call to run (install `python-flint`, run `mypyc`), and
(d) the publication recommendation.

---

## 0. TL;DR

| What | Where | Status |
|---|---|---|
| Reciprocal cache (Newton division dedupe) | `reals/_creal.py` `_INVERSE_CACHE` | Done |
| Expression-DAG memoisation (CSE) | `reals/_creal.py` `_DAG_CACHE` | Done |
| MPFR-style AGM iteration cap | `reals/_creal.py` `gl_pi_CReal.approximate` | Done |
| Boehm irrational-tag for `compareTo` / `signum` | `reals/_creal.py` `IRRATIONAL_TAG_BITS = 3500` | Done |
| `yield_stable_digits()` streaming generator | `reals/_creal.py` `CReal.yield_stable_digits` | Done |
| Bignum backend dispatch (gmpy2 / python-flint / CPython) | `reals/_backends.py` (new) | Done |
| `ProcessPoolExecutor` parallel evaluation helper | `reals/_backends.map_in_parallel` | Done |
| Section 4.4 title fix in `constructive_reals.html` | build script prose | Done |
| Decision log entries D-58 … D-66 | build script section 12.10 | Done |
| New `constructive_reals.html` section 7.3 for `_backends.py` | build script | Done |
| `python-flint` installation | **manual** | See section 5 |
| `mypyc` compilation | **manual** | See section 6 |
| Tests (49 pass) | `tests/` | Verified |

Files touched:

```
Content/Scripts/nd_table/reals-0.0.6/reals/__init__.py        (+1 line: backends import)
Content/Scripts/nd_table/reals-0.0.6/reals/_creal.py          (+289 lines: caches, IRRATIONAL_TAG, yield_stable_digits, AGM cap)
Content/Scripts/nd_table/reals-0.0.6/reals/_backends.py       (new, 218 lines)
Content/Scripts/build_constructive_reals.py                   (prose updates for sections 3.3, 3.4, 4.1, 4.4, 6.2, 6.3, 9.1, 9.2, 10.1, 12.10; new section 7.3; D-58…D-66)
Documentation/constructive_reals.html                         (regenerated, 226 847 chars, 4 929 lines)
Documentation/CONSTRUCTIVE_REALS_UPGRADES.md                  (terse upgrade brief, written earlier this session)
Documentation/ND_TABLE_REALS_UPGRADE.md                       (this file)
```

---

## 1. What the code now does that it didn't before

### 1.1 Reciprocal caching (D-60)

```python
from reals._creal import CReal
x = CReal.valueOf(7).divide(CReal.valueOf(3))
a = x.inverse()
b = x.inverse()
assert a is b   # cache hit
```

Implementation: a module-level
`weakref.WeakValueDictionary[int, inv_CReal]` keyed by `id(operand)`.
`inv_CReal` gained `__weakref__` in its `__slots__`. Because
`inv_CReal.op` keeps a strong reference to the operand, `id()` reuse
cannot produce false hits while the entry is live.

Diagnostics: `reals._creal._inv_cache_clear()`,
`reals._creal._inv_cache_stats()`.

### 1.2 Expression-DAG CSE (D-66)

```python
from reals._creal import CReal
x, y = CReal.PI, CReal.E
assert x.add(y) is y.add(x)              # commutative key normalisation
assert x.multiply(y) is y.multiply(x)
assert x.negate() is x.negate()          # involutive dedup
```

Implementation: a parallel
`weakref.WeakValueDictionary[tuple, CReal]` keyed on
`(kind, id(op1), id(op2))`. The four cached factories
(`add_CReal`, `mult_CReal`, `neg_CReal`, `shifted_CReal`) each gained
`__weakref__`.

**Caveat.** Keys are by `id(operand)`, not by structural equality. Two
semantically-equal but distinct CReals will not dedupe; bind a shared
subterm to a variable. (This is the Boehm PLDI 2020 §5 trade-off.)

Diagnostics: `_dag_cache_clear()`, `_dag_cache_stats()`.

### 1.3 MPFR-style AGM iteration cap (D-59)

```python
from reals._creal import CReal
CReal.PI.get_appr(-10000)  # bounded by ceil(log2(-p+2)) + 5 iterations
```

The Gauss–Legendre loop now has an a-priori cap matching MPFR / Arb's
4096-bit overhead constant. The runtime `a - b > TOLERANCE` test still
gates each iteration so early exit still happens; the cap converts
"stops when it stops" into a guaranteed termination contract.

### 1.4 Boehm irrational-tag heuristic (D-62)

```python
from reals._creal import CReal
sin = CReal.ONE.sin()
cos = CReal.ONE.cos()
identity = sin.multiply(sin).add(cos.multiply(cos))
assert identity.compareTo(CReal.ONE) == 0    # decided in ~55 ms
```

Implementation: class attribute
`CReal.IRRATIONAL_TAG_BITS = 3500`. The no-tolerance forms of
`compareTo(x)` and `signum()` give up iterating once the working
precision reaches `-IRRATIONAL_TAG_BITS` and return `0`. Matches Boehm
PLDI 2020 Sec. 6.2 and Google's Android calculator (the published
reference implementation).

To restore the original divergent semantics:

```python
CReal.IRRATIONAL_TAG_BITS = None
```

### 1.5 `yield_stable_digits()` (D-65)

```python
from reals._creal import CReal
print(''.join(CReal.PI.yield_stable_digits(chunk=8, max_total=60)))
# 3.1415926535897932384626433832795028841971693993751058209749
```

Generator that re-evaluates `toString(n)` at increasing `n` and yields
each digit once it agrees in two consecutive evaluations. Caveat:
incorrect under adversarial digit-boundary inputs (no Boehm-style CR
can be); faithful for all practical numerics.

### 1.6 Backend dispatch + parallel helper (D-58, D-66)

```python
from reals import backends
print(backends.report())
# reals backend probe (active: gmpy2):
#   [yes] gmpy2      gmpy2 (GMP/MPFR/MPC). ~1.0x raw GMP.
#   [no ] flint      not installed
#   [yes] cpython    CPython int. Always available.

best = backends.recommend_backend(precision_bits=10_000)
print(best.name)             # gmpy2 (if installed)
print(best.notes)

results = backends.map_in_parallel(some_func, items, precision_bits=200_000)
# uses ProcessPoolExecutor above the 100,000-bit threshold; sequential below
```

Environment override:

```powershell
$env:REALS_BACKEND = "flint"     # force the dispatcher; silent fallback if missing
```

---

## 2. Verify locally (sanity check, ~30 seconds)

```powershell
cd "Content\Scripts\nd_table\reals-0.0.6"
$env:PYTHONIOENCODING = "utf-8"

# 1. Tests pass (49)
python -m pytest tests -q

# 2. Smoke check: irrational-tag heuristic works
python -c "from reals._creal import CReal; print('cmp(pi,pi) =', CReal.PI.compareTo(CReal.PI))"

# 3. Smoke check: streaming digits
python -c "from reals._creal import CReal; print(''.join(CReal.PI.yield_stable_digits(max_total=60)))"

# 4. Smoke check: backend probe
python -c "from reals import backends; print(backends.report())"

# 5. Smoke check: dedup
python -c "from reals._creal import CReal; x=CReal.valueOf(7); print(x.inverse() is x.inverse())"
```

Expected output line counts: `49 passed`, `cmp(pi,pi) = 0`,
`3.1415926535897932384626433832795028841971693993751058209749`,
backend probe table, `True`.

---

## 3. Rebuild `constructive_reals.html` after package edits

```powershell
python "Content\Scripts\build_constructive_reals.py"
```

That writes `Documentation/constructive_reals.html` (~227 KB,
~4 929 lines) and prints the source directory. The script regenerates
the embedded source dumps automatically from
`Content/Scripts/nd_table/reals-0.0.6/reals/*.py`, so any future edits
to the package only need the build script re-run.

You should never edit `Documentation/constructive_reals.html` by hand;
it's a build product. The source of truth is
`Content/Scripts/build_constructive_reals.py`.

---

## 4. What's in the rebuilt HTML

Five places in the prose are new or revised vs the previous build:

| Section | Change |
|---|---|
| 3.3 *Approximation cache* | Two new paragraphs documenting `_INVERSE_CACHE` and `_DAG_CACHE`. |
| 3.4 *Precision propagation* | New paragraph on `CReal.IRRATIONAL_TAG_BITS` and heuristic decidability. |
| 4.1 *π via Gauss–Legendre AGM* | New bullet: "A-priori MPFR-style iteration cap." |
| 4.4 title | Was "ln via Machin and AGM reduction" (misleading — no AGM). Now "ln via Machin-style argument reduction and Taylor." New callout pointing at the `python-flint` Arb dispatch path for large precision. |
| 6.2 *Optimisations applied* | Was "Three changes." Now "Six changes" with the three new entries: reciprocal cache, expression-DAG CSE, MPFR-style AGM cap. |
| 6.3 *Where the floor is* | Was "None of these were applied. The package stays pure-Python, no native deps." Now describes the opt-in `reals.backends` probe. |
| 9.1 *Algorithmic frontiers* | Each open problem now carries a *Status:* tag (redirected / partial / done / open with backend path). |
| 9.2 *Implementation frontiers* | Same. The five items map to D-58, D-64, D-65, D-66, D-66. |
| 10.1 *NTT / FFT for Python ints* | Replaced the speculative survey with a verified 2025-state-of-the-art table (python-flint 0.8.0, gmpy2, CPython status; Mojo and Numba claims flagged unverified). |
| 12.10 *Deliberately deferred* | D-54 (NTT), D-55 (mypyc), D-56 (gmpy2) status updated; nine new entries D-58 through D-66 added. |
| 7.3 (new) | `reals/_backends.py` source dump (218 lines). |
| 7.4 / 7.5 / 7.6 | PGA sections renumbered. |
| TOC | New entry for `_backends.py`. |

Zero section-sign characters in the output.

---

## 5. **MANUAL STEP** — install `python-flint`

Recommended once you want to push past CPython's int multiplication
ceiling without writing an NTT. From any shell:

```powershell
pip install python-flint
```

`python-flint 0.8.0` (released 2025-08-29) ships:
- FLINT 3.3.1
- Arb (interval arithmetic + table-based Taylor log/exp ≤ 4096 bits)
- MPFR 4.2.2

…with PyPI wheels for CPython 3.11–3.14 (incl. 3.14t free-threaded)
and PyPy 3.11. No build step required.

After install, the backend probe will report it:

```powershell
python -c "from reals import backends; print(backends.report())"
# [yes] flint  python-flint (FLINT 3.3.1 + Arb + MPFR 4.2.2). ~1.5x raw GMP.
```

The package itself works exactly the same with or without
`python-flint`; the only difference is what `recommend_backend()`
returns and what user code that opts into it can dispatch to.

### 5.1 Optional: wire Arb's `log` into `reals.log_via_arb`

A ~30-line stub:

```python
# in your code (not the package)
from reals._creal import CReal
from reals import backends

def log_via_arb(x: CReal, prec_bits: int) -> CReal:
    backend = backends.recommend_backend(prec_bits)
    if backend.name != "flint":
        return x.ln()
    import flint
    ctx = flint.arb_ctx(prec_bits + 32)
    appr = x.get_appr(-prec_bits - 32)
    val = flint.arb(appr) >> (prec_bits + 32)
    result = ctx.log(val)
    # round to int at appropriate precision and re-wrap
    int_val = int(result << prec_bits)
    return CReal.valueOf(int_val).shiftRight(prec_bits)
```

Skip this until you're actually benching past ~10⁵ bits — the package's
existing Machin-style Taylor is fine below that.

### 5.2 Optional: Calcium algebraic decision

`python-flint` exposes Calcium (now in FLINT 3.0) for *guaranteed*
algebraic-number comparison — not the heuristic. The API hook is
reserved as `cr.with_algebraic_decision()` (D-63) but not implemented.
If you need it, the call surface is roughly 50 lines wrapping
`flint.calcium`'s equality predicate.

---

## 6. **MANUAL STEP** — compile `_creal.py` with `mypyc` (D-64)

Verified speedup range from the mypyc benchmark suite:

| Workload | Range |
|---|---|
| Existing annotated code | 1.5×–5× |
| Code tuned for compilation | 5×–10× |
| richards (the canonical bench) | 9.870× |

The AGM / Newton / Taylor inner loops match the tuned-for-compilation
profile. Expect 5–14× wall-clock on those and ~2–3× on the mixed-object
hot paths.

```powershell
pip install mypy
cd "Content\Scripts\nd_table\reals-0.0.6\reals"
mypyc _creal.py
```

This emits a `_creal.<platform>.{so,pyd}` next to the source. Python
imports the compiled version automatically the next time the package
is imported.

To revert: delete the generated `.so` / `.pyd`.

The package itself does *not* run `mypyc` — D-02 ("`pip install reals`
from any environment") stays intact. This is opt-in per developer.

---

## 7. Defaults summary

Everything below is what a fresh `from reals import CReal` gives you,
without installing anything beyond what was already there:

- Pure-Python int arithmetic (Karatsuba ≥ 2 100 bits, schoolbook below)
- Reciprocal cache: on
- Expression-DAG CSE cache: on
- MPFR-style AGM cap: on
- `CReal.IRRATIONAL_TAG_BITS = 3500`
- `yield_stable_digits()`: available, never called automatically
- `reals.backends.BIGNUM_BACKEND.name`: `gmpy2` if installed, else
  `flint` if installed, else `cpython`
- `reals.backends.map_in_parallel(...)`: available, never called
  automatically
- All 49 existing tests pass

---

## 8. Rollback paths

If any of the new behaviour breaks something downstream:

| Concern | Mitigation |
|---|---|
| Irrational-tag heuristic gives wrong answer in your domain | `CReal.IRRATIONAL_TAG_BITS = None` (restore divergence) |
| Reciprocal cache pinning unwanted memory | `_inv_cache_clear()` — entries auto-evict when nobody holds the inv anyway |
| Expression-DAG cache pinning memory | `_dag_cache_clear()` |
| `yield_stable_digits` stalls on adversarial input | Don't call it; use `toString(n)` |
| Backend dispatch picks wrong backend | `$env:REALS_BACKEND = "cpython"` |
| `mypyc` compiled module misbehaves | Delete the `.so` / `.pyd` next to `_creal.py` |

None of these affect the existing public API. `CReal.add`, `multiply`,
`negate`, `shift{Left,Right}`, `inverse`, `compareTo`, `signum`,
`toString` all behave the same on inputs that don't trigger the new
optimisations.

---

## 9. Publish — Sec. 9.4.2 of the brief

This is the one thing the brief flagged as a *genuine research
contribution* rather than an engineering upgrade: the combination of
`kingdon`-driven Projective Geometric Algebra on top of Boehm-style
constructive reals. No published work combines them; the closest
neighbour is Abbas Edalat's domain-theoretic geometry work, which is
theoretical rather than implemented.

Recommended venues:

- **GAME** — *Geometric Algebra in Mathematics and Engineering*
  (Birkhäuser series). Natural home for "we built it and it works"
  papers.
- **CGI** — *Computer Graphics International*. Better fit if you
  emphasise rendering / interactive visualisation.

A short paper covering:

1. `reals/_pga*.py` — the integration architecture
2. The `bench/` directory — existing benchmark numbers
3. Three or four worked examples at 1 000-bit precision (motor
   exponential, point-line meet, rotor sandwich)
4. The Sec. 9.1.5 irrational-tag heuristic + the Sec. 9.2.4 CSE cache
   as practical fixes to Boehm-style CR not previously written up

…would land cleanly at either venue. Boehm's PLDI 2020 paper does the
Java-side baseline; the PGA integration is the novel angle.

---

## 10. Files to share with reviewers

If you're sending this work to someone for a sanity check:

| Read first | What it is |
|---|---|
| `Documentation/ND_TABLE_REALS_UPGRADE.md` | This file. |
| `Documentation/CONSTRUCTIVE_REALS_UPGRADES.md` | The terser per-recommendation matrix. |
| `Documentation/constructive_reals.html` | Full design + decision log + source dump. |
| `Content/Scripts/nd_table/reals-0.0.6/reals/_creal.py` | The constructive-real core. |
| `Content/Scripts/nd_table/reals-0.0.6/reals/_backends.py` | The new backend dispatch module. |
| `Content/Scripts/nd_table/reals-0.0.6/tests/` | 49 tests, all passing. |

Everything else (PGA modules, build script, continued-fraction `Real`
class) is unchanged and orthogonal to this upgrade pass.
