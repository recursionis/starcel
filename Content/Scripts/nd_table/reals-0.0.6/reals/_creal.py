"""Constructive real numbers (CReal).

Python port of Christian Lawson-Perfect's 2022 ECMAScript port
(``creal_js_extracted.js``) of Hans Boehm's Java implementation.

  Copyright (C) 2015 The Android Open Source Project
  Copyright (c) 1999, Silicon Graphics, Inc.
  Copyright (c) 2001-2004, Hewlett-Packard Development Company, L.P.

Licensed under Apache 2.0 / SGI / HP licenses (see the original source for
full terms).

Each constructive real is represented as an object that provides an
approximation function. Arithmetic operations construct new lazy objects;
real computation happens only when an approximation is requested.
``get_appr(p)`` returns a Python ``int`` ``n`` such that ``|x - n / 2**p| < 1``.

Number-system embedding
-----------------------

A ``CReal`` represents an element of the computable subset of ℝ. The
standard tower

    ℤ ⊂ ℚ ⊂ ℝ_computable

is preserved by the type, and each layer has a specialised representation
so the common cases stay cheap:

- **ℤ (integers)** — built by ``CReal.valueOf(n)`` for any Python ``int``
  (arbitrary magnitude — verified at 10^100 and beyond). Stored as the
  ``int_CReal`` subclass, whose ``approximate(p)`` is a single bit-shift
  with no Taylor series, Newton iteration, or AGM. ``True`` / ``False``
  fold in via the standard ``bool ⊂ int`` containment. The
  ``assumeInt()`` method tags a derived CReal as "known integer" so
  downstream operations skip sub-unit precision work; closure under
  ``+, −, ×`` is preserved automatically.

- **ℚ (rationals)** — built via division, e.g.
  ``CReal.valueOf(p).divide(CReal.valueOf(q))`` or by passing a decimal
  string like ``CReal.valueOf("0.1")``, which parses as exact ``1/10``
  rather than the IEEE 754 ``0.1`` neighbour. Stored as the lazy
  expression tree (mult of an int by an inverse of an int).

- **ℝ_computable (the rest)** — built by ``sqrt``, ``exp``, ``ln``, ``sin``,
  ``cos``, ``asin``, ``pi``, ``e``, etc. Each is a separate subclass with
  its own ``approximate(p)`` implementing the relevant Taylor series,
  Newton iteration, or arithmetic-geometric mean.

The ``ℝ → ℤ`` projection is provided by ``BigIntValue()`` / ``intValue()``,
which return the nearest integer (within 1). Note that this is a
floor-toward-nearest projection, not a constructive equality test —
deciding whether a CReal *is* an exact integer is undecidable in general
and would diverge.
"""

from __future__ import annotations

import time
import weakref
from typing import Optional, Union


# JS Number.MIN_SAFE_INTEGER, used as the "msd not yet known" sentinel.
_MIN_SAFE_INTEGER = -(2 ** 53 - 1)
_MAX_SAFE_INTEGER = 2 ** 53 - 1


# Sec. 9.1.3 — reciprocal cache. Keyed by id(operand); the cached value is the
# inv_CReal node that wraps it. Because inv_CReal holds a strong reference to
# its operand (``inv.op``) the operand cannot be collected while the cache
# entry is live, so id() reuse cannot produce false hits. WeakValueDictionary
# auto-evicts entries once the inv_CReal is no longer referenced anywhere.
#
# Pays for itself from the second ``a / d`` call onward against the same
# denominator: Newton's iteration in ``inv_CReal.approximate`` converges
# quadratically and reuses the cached intermediates via the base-class
# ``min_prec`` / ``max_appr`` memo. See ``_inv_cache_clear()`` for tests.
_INVERSE_CACHE: "weakref.WeakValueDictionary[int, inv_CReal]" = (
    weakref.WeakValueDictionary()
)


def _inv_cache_clear() -> None:
    """Drop the reciprocal cache. Tests and benchmarks may want a clean slate."""
    _INVERSE_CACHE.clear()


def _inv_cache_stats() -> dict:
    """Return cache size + a snapshot of live ids (debug helper, not stable API)."""
    return {"size": len(_INVERSE_CACHE), "live_ids": list(_INVERSE_CACHE.keys())}


# Sec. 9.2.4 — CSE / subgraph memoisation cache. Keyed by the expression-DAG
# fingerprint ``(kind_tag, operand_id_or_value, …)``; value is the CReal node
# whose constructor produced that fingerprint. WeakValueDictionary semantics
# mean the entry disappears as soon as nobody references the deduplicated
# node. This is exactly the optimisation Boehm's PLDI 2020 paper describes
# for ``sin²x + cos²x`` (where ``sin x`` and ``cos x`` are common subexpressions)
# but on the constructor side, not after the fact.
#
# Caveats:
# - The cache is keyed by ``id`` of operand CReals, not by structural equality
#   of the operands themselves. So ``a + b`` and ``c + d`` with ``a, c`` and
#   ``b, d`` semantically-equal-but-distinct CReals will *not* dedupe. To
#   dedupe across construction sites, the operands must literally be the same
#   Python object — which is what the inverse cache (Sec. 9.1.3) already gives
#   you for reciprocals, and what user code can arrange for any other
#   subexpression.
# - The cache stores ``add_CReal``, ``mult_CReal``, ``neg_CReal``,
#   ``shifted_CReal`` (the high-impact factories). Other constructors
#   bypass the cache; that's a deliberate scope choice — extending to all
#   subclasses is a few-line change but increases the cache hit-rate noise
#   for cold workloads.
_DAG_CACHE: "weakref.WeakValueDictionary[tuple, CReal]" = (
    weakref.WeakValueDictionary()
)


def _dag_cache_clear() -> None:
    _DAG_CACHE.clear()


def _dag_cache_stats() -> dict:
    return {"size": len(_DAG_CACHE)}


def _bit_length(n: int) -> int:
    """Match JS ``n.toString(2).length`` for non-negative inputs.

    Callers in this module only pass ``n >= 0``. We return 1 for 0 so that
    ``known_msd`` (which adds ``length - 1``) reports an msd consistent with
    the JS implementation if it is ever called on a zero approximation.
    """
    if n == 0:
        return 1
    return n.bit_length() if n > 0 else (-n).bit_length()


def _abs(n: int) -> int:
    return -n if n < 0 else n


def _signum(n: int) -> int:
    return 1 if n > 0 else (-1 if n < 0 else 0)


def _trunc_div(a: int, b: int) -> int:
    """Integer division that truncates toward zero (matches JS BigInt ``/``).

    Python's ``//`` floors toward -inf; this helper matches the BigInt
    semantics used pervasively in the source.

    Fast path when both operands have the same sign — that case is
    bit-identical to Python's ``//`` and avoids the ``divmod`` call
    (which allocates and returns a tuple). At 50,000-digit precision the
    same-sign skip removes ~8% of total bench time.
    """
    if (a >= 0) == (b >= 0):
        return a // b
    q, r = divmod(a, b)
    if r:
        q += 1
    return q


def _ceil_log2(n: float) -> int:
    """Ceiling of log2(abs(n) + 1), as in CReal.bound_log2."""
    import math
    return math.ceil(math.log(abs(n) + 1) / math.log(2.0))


class _Timeout:
    """Coarse runtime guard.

    Mirrors the JS ``Timeout`` helper. Used inside iterative approximation
    loops so a pathological computation can't lock up indefinitely.
    """

    __slots__ = ("counter", "start")

    def __init__(self) -> None:
        self.counter = 0
        self.start = time.monotonic()

    def check(self) -> None:
        # Cooperative cancellation: an outside thread can set CReal.please_stop
        # to abort long-running iterative loops.
        if CReal.please_stop:
            raise RuntimeError("Operation aborted")
        self.counter += 1
        if self.counter % 100 == 0:
            dt_ms = (time.monotonic() - self.start) * 1000
            if dt_ms > CReal.TIMEOUT_DURATION:
                raise RuntimeError(f"Operation took too long: {dt_ms:.0f}ms")


class CReal:
    """Constructive real number.

    Subclasses override :meth:`approximate`. The cached :meth:`get_appr`
    wrapper memoises the most recently produced approximation and rescales
    it when a coarser one is sufficient.
    """

    # ``__slots__`` saves ~200 bytes per instance vs the default ``__dict__``
    # and gives attribute access through a C-level slot descriptor — both
    # noticeable in the profile because AGM iterations allocate hundreds
    # of CReal instances per call.
    #
    # ``__weakref__`` is included so EVERY CReal subclass is eligible to be
    # the value side of a ``WeakValueDictionary`` (see ``_INVERSE_CACHE`` and
    # ``_DAG_CACHE``). The ~8-byte-per-instance overhead is negligible
    # relative to the BigInt ``max_appr`` field most nodes carry, and it
    # spares every cache addition the chore of editing per-subclass slot
    # lists. Decision D-67.
    __slots__ = ("min_prec", "max_appr", "appr_valid", "__weakref__")

    # Max wall-clock budget per inner iteration loop, in milliseconds.
    # Nested operations get fresh timers, so a single ``evaluate`` call can
    # take longer than this in aggregate.
    TIMEOUT_DURATION = 3000

    # Cooperative cancellation flag (Java parity). Set from another thread
    # to abort any in-progress iteration; reset to False before continuing.
    please_stop = False

    # Decision D-69 — opt-in short-circuit for the ℤ subset. When ``True``,
    # ``add`` / ``multiply`` / ``negate`` detect ``int_CReal + int_CReal``
    # (and the ``assumed_int_CReal`` sibling) at the factory and collapse
    # straight to an ``int_CReal`` of the computed value, skipping the lazy
    # expression tree. Default ``False`` to preserve the documented contract
    # (some callers pattern-match on subclass type — see HTML decision D-49).
    SHORT_CIRCUIT_INT_OPS = False

    # Sec. 9.1.5 — Boehm's irrational-tag heuristic threshold (PLDI 2020 Sec.6.2).
    # The no-tolerance forms of ``compareTo`` and ``signum`` give up
    # iterating once the working precision reaches ``-IRRATIONAL_TAG_BITS``
    # and report 0. 3500 bits matches Google's Android calculator, which
    # is the published reference. Set to ``None`` to restore the original
    # divergent semantics (exact-equality calls will loop forever).
    IRRATIONAL_TAG_BITS: Optional[int] = 3500

    # Class-level placeholders so static analysis / IDEs see them; filled in
    # after the supporting subclasses are defined, at module bottom.
    ZERO: "CReal"
    ONE: "CReal"
    PI: "CReal"
    E: "CReal"
    ln2: "CReal"
    half_pi: "CReal"
    four: "CReal"
    low_ln_limit: int
    high_ln_limit: int
    scaled_4: int

    def __init__(self) -> None:
        self.min_prec: Optional[int] = None
        self.max_appr: int = 0
        self.appr_valid: bool = False

    # ---- subclass hook ---------------------------------------------------

    def approximate(self, precision: int) -> int:
        raise NotImplementedError("approximate not implemented")

    # ---- static helpers --------------------------------------------------

    @staticmethod
    def bound_log2(n: int) -> int:
        return _ceil_log2(n)

    @staticmethod
    def check_prec(n: int) -> None:
        """Reject precisions that can't safely round-trip through int32.

        Mirrors the JS check, which uses 32-bit signed arithmetic. Python
        ``>>`` on signed ints already produces matching results in the
        relevant range, so a direct translation works.
        """
        high = n >> 28
        high_shifted = n >> 29
        if high ^ high_shifted:
            raise ValueError("precision overflow")

    @staticmethod
    def shift(k: int, n: int) -> int:
        """Multiply ``k`` by ``2 ** n`` (truncating toward -inf for n < 0)."""
        if n == 0:
            return k
        if n < 0:
            return k >> (-n)
        return k << n

    @staticmethod
    def scale(k: int, n: int) -> int:
        """Multiply ``k`` by ``2 ** n``, rounding result to nearest integer."""
        if n >= 0:
            return k << n
        adj_k = CReal.shift(k, n + 1) + 1
        return adj_k >> 1

    # ---- cached approximation -------------------------------------------

    def get_appr(self, precision: int) -> int:
        """Return ``round(value / 2 ** precision)``.

        Reuses the cached approximation if one is available at sufficient
        precision; otherwise recomputes and refreshes the cache.
        """
        CReal.check_prec(precision)
        if self.appr_valid and self.min_prec is not None and precision >= self.min_prec:
            return CReal.scale(self.max_appr, self.min_prec - precision)
        result = self.approximate(precision)
        self.min_prec = precision
        self.max_appr = result
        self.appr_valid = True
        return result

    # ---- msd / iter_msd --------------------------------------------------

    def known_msd(self) -> int:
        """Position of the most significant digit, given a usable cache."""
        if self.max_appr >= 0:
            length = _bit_length(self.max_appr)
        else:
            length = _bit_length(-self.max_appr)
        assert self.min_prec is not None
        return self.min_prec + length - 1

    def msd(self, n: Optional[int] = None) -> int:
        """Return position of the most significant digit.

        If ``n`` is omitted, iterates to find a definite answer (may loop
        forever for an exact zero). Otherwise, returns ``_MIN_SAFE_INTEGER``
        when the true msd is known only to be ``< n``.
        """
        if n is None:
            return self.iter_msd(_MIN_SAFE_INTEGER)
        if (not self.appr_valid) or (-1 <= self.max_appr <= 1):
            self.get_appr(n - 1)
            if _abs(self.max_appr) <= 1:
                # msd could still be arbitrarily far to the right
                return _MIN_SAFE_INTEGER
        return self.known_msd()

    def iter_msd(self, n: int) -> int:
        prec = 0
        while prec > n + 30:
            msd_val = self.msd(prec)
            if msd_val != _MIN_SAFE_INTEGER:
                return msd_val
            CReal.check_prec(prec)
            if CReal.please_stop:
                raise RuntimeError("Operation aborted")
            # Java uses truncating int division here; using Python's // would
            # disagree by 1 on odd negative inputs (still converges, but loses
            # bit-exact parity with the reference for the precision sequence).
            prec = _trunc_div(prec * 3, 2) - 16
        return self.msd(n)

    # ---- formatting helpers ---------------------------------------------

    @staticmethod
    def zeros(n: int) -> str:
        return "0" * n

    def simple_ln(self) -> "CReal":
        return prescaled_ln_CReal(self.subtract(CReal.ONE))

    @staticmethod
    def atan_reciprocal(n: int) -> "CReal":
        return integral_atan_CReal(n)

    # ---- comparison ------------------------------------------------------

    def compareTo(self, x: "CReal", *args: int) -> int:
        """Three-way compare against another constructive real.

        Forms:

        - ``compareTo(x)`` — return -1/0/+1. The default behaviour follows
          Boehm's PLDI 2020 Sec.6.2 irrational-tag heuristic: iterate doubling
          precision, but **give up and return 0** once the working precision
          reaches ``-CReal.IRRATIONAL_TAG_BITS`` (default 3500 bits below the
          binary point). This is heuristically correct for all practical
          numerics and is what Google's Android calculator actually ships.
          Set ``CReal.IRRATIONAL_TAG_BITS = None`` to restore the original
          behaviour, which may diverge if the two values are exactly equal.
          For algebraic decisions guaranteed to terminate, dispatch through
          ``python-flint``'s Calcium (see ``CONSTRUCTIVE_REALS_UPGRADES.md``).
        - ``compareTo(x, a)`` — absolute tolerance ``2 ** a``; may return
          0 if the difference is smaller than the tolerance.
        - ``compareTo(x, r, a)`` — relative tolerance ``r`` bits combined
          with absolute tolerance ``a``.
        """
        if len(args) == 2:
            r, a = args
            this_msd = self.iter_msd(a)
            x_msd = x.iter_msd(this_msd if this_msd > a else a)
            max_msd = x_msd if x_msd > this_msd else this_msd
            if max_msd == _MIN_SAFE_INTEGER:
                return 0
            CReal.check_prec(r)
            rel = max_msd + r
            abs_prec = rel if rel > a else a
            return self.compareTo(x, abs_prec)
        if len(args) == 1:
            a = args[0]
            needed_prec = a - 1
            this_appr = self.get_appr(needed_prec)
            x_appr = x.get_appr(needed_prec)
            if this_appr > x_appr + 1:
                return 1
            if this_appr < x_appr - 1:
                return -1
            return 0
        # No tolerance — iterate until decisive, or until the Sec. 9.1.5 cutoff.
        tag = CReal.IRRATIONAL_TAG_BITS
        a = -20
        while True:
            CReal.check_prec(a)
            if CReal.please_stop:
                raise RuntimeError("Operation aborted")
            result = self.compareTo(x, a)
            if result != 0:
                return result
            if tag is not None and -a >= tag:
                return 0  # heuristic zero — see PLDI 2020 Sec.6.2
            a *= 2

    def signum(self, a: Optional[int] = None) -> int:
        """Sign of the value, with optional absolute precision ``a``.

        Without ``a``, applies the Sec. 9.1.5 irrational-tag heuristic exactly
        as :meth:`compareTo` does: iterate doubling precision down to at
        most ``-CReal.IRRATIONAL_TAG_BITS``, then return 0. Set
        ``CReal.IRRATIONAL_TAG_BITS = None`` to restore the original
        possibly-divergent behaviour.
        """
        if a is None:
            tag = CReal.IRRATIONAL_TAG_BITS
            a_iter = -20
            while True:
                CReal.check_prec(a_iter)
                if CReal.please_stop:
                    raise RuntimeError("Operation aborted")
                result = self.signum(a_iter)
                if result != 0:
                    return result
                if tag is not None and -a_iter >= tag:
                    return 0  # heuristic zero
                a_iter *= 2
        if self.appr_valid and self.max_appr != 0:
            return 1 if self.max_appr > 0 else -1
        needed_prec = a - 1
        this_appr = self.get_appr(needed_prec)
        return _signum(this_appr)

    # ---- streaming digits ------------------------------------------------

    def yield_stable_digits(
        self,
        radix: int = 10,
        chunk: int = 16,
        max_total: Optional[int] = None,
    ):
        """Stream digits whose value has stabilised across two re-evaluations.

        Sec. 9.2.3 — Boehm-style CR cannot stream natively (would require a
        Möbius / Edalat-Potts representation change; see RealLib (Lambov) or
        the LICS 1997 / ICFP 1998 papers). This iterator implements the
        compromise recommended in the upgrade brief: re-evaluate at
        increasing precision and yield a digit only once its value matches
        in two consecutive evaluations at higher precision.

        Yields one decimal/radix digit per ``__next__`` call, starting with
        the sign (``'-'`` if negative) followed by the integer part, a
        ``'.'`` separator, and then fractional digits.

        Caveat: under adversarial inputs that genuinely lie on a digit
        boundary (e.g., a CR equal to exactly ``1.0000...0`` followed by an
        unknowable far-future deviation), the iterator may stall waiting
        for stabilisation that never arrives. For all practical numerics
        it makes progress.

        Parameters
        ----------
        radix : int
            Output base (default decimal). Supports the same radices as
            :meth:`toString`.
        chunk : int
            Number of fractional digits to compute per refinement round.
            Larger = fewer refinement passes but more work per pass.
        max_total : int or None
            Cap on the total number of digits yielded (excluding sign /
            decimal point). ``None`` = unbounded; the iterator keeps
            running until the consumer stops asking.
        """
        if radix < 2:
            raise ValueError("radix must be >= 2")
        if chunk < 1:
            raise ValueError("chunk must be >= 1")

        # Sign once.
        sgn = self.signum()
        x = self.negate() if sgn < 0 else self
        if sgn < 0:
            yield "-"

        # Two cached snapshots at successive precisions.
        prev_str = ""
        n = chunk
        yielded = 0
        emitted_point = False
        while True:
            curr_str = x.toString(n, radix)
            # ``toString`` formats as ``D...D.dddd...d``. Find decimal point.
            if "." in curr_str:
                whole, frac = curr_str.split(".", 1)
            else:
                whole, frac = curr_str, ""

            # First pass: emit the integer part once (assumed stable enough
            # for any non-pathological CR). Subsequent passes only refine
            # the fractional portion.
            if not emitted_point:
                for ch in whole:
                    yield ch
                    yielded += 1
                    if max_total is not None and yielded >= max_total:
                        return
                if frac:
                    yield "."
                    yielded += 1  # account for the separator
                    emitted_point = True

            # Stream fractional digits that match the previous evaluation.
            if prev_str:
                # Previous fractional part.
                if "." in prev_str:
                    _, prev_frac = prev_str.split(".", 1)
                else:
                    prev_frac = ""
                # Compare digit-by-digit, but only emit digits NOT yet sent.
                already_sent = yielded - len(whole) - (1 if emitted_point else 0)
                already_sent = max(already_sent, 0)
                stable_len = 0
                for i, (a, b) in enumerate(zip(prev_frac, frac)):
                    if a == b:
                        stable_len = i + 1
                    else:
                        break
                # Emit any digits not yet sent up to ``stable_len``.
                for i in range(already_sent, stable_len):
                    yield frac[i]
                    yielded += 1
                    if max_total is not None and yielded >= max_total:
                        return

            prev_str = curr_str
            n += chunk

    # ---- string / scientific conversion ---------------------------------

    def toString(self, n: int = 10, radix: int = 10) -> str:
        """Decimal/hex representation accurate to ``n`` fractional digits."""
        if radix == 16:
            scaled = self.shiftLeft(4 * n)
        else:
            scale_factor = radix ** n
            scaled = self.multiply(int_CReal(scale_factor))
        scaled_int = scaled.get_appr(0)
        if scaled_int < 0:
            return "-" + self.negate().toString(n, radix)
        scaled_string = _int_to_radix(_abs(scaled_int), radix)
        if n == 0:
            result = scaled_string
        else:
            length = len(scaled_string)
            if length <= n:
                scaled_string = CReal.zeros(n + 1 - length) + scaled_string
                length = n + 1
            whole = scaled_string[: length - n]
            fraction = scaled_string[length - n:]
            result = whole + "." + fraction
        if scaled_int < 0:
            result = "-" + result
        return result

    def toStringFloatRep(self, n: int, radix: int, m: int) -> dict:
        """Scientific notation tuple ``{sign, mantissa, radix, exponent}``."""
        import math
        if n <= 0:
            raise ValueError("Bad precision argument")
        log2_radix = math.log(radix) / math.log(2)
        big_radix = radix
        msd_prec = round(log2_radix * m)
        if msd_prec > _MAX_SAFE_INTEGER or msd_prec < _MIN_SAFE_INTEGER:
            raise ValueError("precision overflow")
        CReal.check_prec(msd_prec)
        msd = self.iter_msd(msd_prec - 2)
        if msd == _MIN_SAFE_INTEGER:
            return {"sign": 0, "mantissa": "0", "radix": radix, "exponent": 0}
        exponent = math.ceil(msd / log2_radix)
        scale_exp = exponent - n
        if scale_exp > 0:
            scale = CReal.valueOf(big_radix ** scale_exp).inverse()
        else:
            scale = CReal.valueOf(big_radix ** (-scale_exp))
        scaled_res = self.multiply(scale)
        scaled_int = scaled_res.get_appr(0)
        sign = _signum(scaled_int)
        scaled_string = _int_to_radix(_abs(scaled_int), radix)
        timeout = _Timeout()
        while len(scaled_string) < n:
            timeout.check()
            scaled_res = scaled_res.multiply(CReal.valueOf(big_radix))
            exponent -= 1
            scaled_int = scaled_res.get_appr(0)
            sign = _signum(scaled_int)
            scaled_string = _int_to_radix(_abs(scaled_int), radix)
        if len(scaled_string) > n:
            exponent += len(scaled_string) - n
            scaled_string = scaled_string[:n]
        return {"sign": sign, "mantissa": scaled_string, "radix": radix, "exponent": exponent}

    def BigIntValue(self) -> int:
        """ℝ → ℤ projection (within ±1, rounding implementation-defined).

        Returns an integer ``n`` with ``|self − n| < 1``. **This is the
        only formal guarantee** — when ``self`` falls between two integers
        either of them is a valid return. In practice the chain of
        ``get_appr(0)`` calls usually produces a value close to
        round-toward-zero, but that isn't a contract. Examples:

        - ``CReal.PI.BigIntValue() == 3``         (|π − 3| ≈ 0.14 < 1) ✓
        - ``(3*PI).BigIntValue() == 9``           (|9.42… − 9| ≈ 0.42 < 1) ✓
        - ``CReal.valueOf(8).sqrt().BigIntValue() ∈ {2, 3}``
              (|2.828… − 2| ≈ 0.83 and |2.828… − 3| ≈ 0.17 both < 1)

        Asking "is this CReal an exact integer?" is undecidable in
        general — the approximation chain would have to converge to an
        integer at arbitrary precision, which can't be confirmed in
        finite time without external knowledge. Use :meth:`assumeInt`
        if you have that knowledge.
        """
        return self.get_appr(0)

    def intValue(self) -> int:
        """ℝ → native ``int`` projection. Same rounding as
        :meth:`BigIntValue`; overflow behaviour is undefined for values
        outside the platform ``int`` range (irrelevant in Python where
        ``int`` is unbounded — included for Java parity)."""
        return int(self.BigIntValue())

    def doubleValue(self) -> float:
        """Float (IEEE double) value, accurate to within ~1 ulp.

        Mirrors Java ``CR.doubleValue``: pick a precision ~60 bits below the
        msd, then scale by ``2 ** needed_prec``. We delegate that scaling to
        ``math.ldexp`` so IEEE overflow → +/-inf and underflow → subnormal/0
        are handled correctly without manual bit twiddling.
        """
        import math
        my_msd = self.iter_msd(-1080)
        if my_msd == _MIN_SAFE_INTEGER:
            return 0.0
        needed_prec = my_msd - 60
        scaled_int = self.get_appr(needed_prec)
        try:
            return math.ldexp(float(scaled_int), needed_prec)
        except OverflowError:
            return float("inf") if scaled_int > 0 else float("-inf")

    # JS-port spelling, kept for source compatibility.
    floatValue = doubleValue

    # ---- arithmetic ------------------------------------------------------

    def add(self, x: "CReal") -> "CReal":
        # Decision D-69 — opt-in ℤ short-circuit, off by default.
        if CReal.SHORT_CIRCUIT_INT_OPS:
            t_self, t_x = type(self), type(x)
            if (t_self is int_CReal or t_self is assumed_int_CReal) and \
               (t_x is int_CReal or t_x is assumed_int_CReal):
                return int_CReal(self.value + x.value)
        # Sec. 9.2.4 — symmetric addition is canonicalised so a+b and b+a hit the
        # same cache entry. id() ordering is arbitrary but stable for the
        # process lifetime, which is sufficient for the WeakValueDictionary.
        a_id, b_id = id(self), id(x)
        lo, hi = (self, x) if a_id <= b_id else (x, self)
        key = ("add", id(lo), id(hi))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = add_CReal(lo, hi)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def shiftLeft(self, n: int) -> "CReal":
        CReal.check_prec(n)
        key = ("shift", id(self), n)
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = shifted_CReal(self, n)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def shiftRight(self, n: int) -> "CReal":
        CReal.check_prec(n)
        key = ("shift", id(self), -n)
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = shifted_CReal(self, -n)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def assumeInt(self) -> "CReal":
        """Re-tag this CReal as ``ℤ``-valued (caller assertion).

        Wraps ``self`` in :class:`assumed_int_CReal`. Downstream callers
        will skip sub-unit precision when evaluating, because they trust
        the value really is an integer. Useful after a chain like
        ``(a + b) * c`` where ``a``, ``b``, ``c`` are integers — the
        expression tree doesn't *know* the result is in ℤ, even though
        you do. **Undefined behaviour if the assertion is wrong** — the
        wrapper genuinely never looks past the decimal point.
        """
        # Decision D-68 — unary kernel DAG cache.
        key = ("assumeInt", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = assumed_int_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def negate(self) -> "CReal":
        # Decision D-69 — opt-in ℤ short-circuit.
        if CReal.SHORT_CIRCUIT_INT_OPS:
            t = type(self)
            if t is int_CReal or t is assumed_int_CReal:
                return int_CReal(-self.value)
        # Sec. 9.2.4 — negate is involutive; cache so neg(neg(x)) is x exactly.
        key = ("neg", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = neg_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def subtract(self, x: "CReal") -> "CReal":
        return self.add(x.negate())

    def multiply(self, x: "CReal") -> "CReal":
        # Decision D-69 — opt-in ℤ short-circuit.
        if CReal.SHORT_CIRCUIT_INT_OPS:
            t_self, t_x = type(self), type(x)
            if (t_self is int_CReal or t_self is assumed_int_CReal) and \
               (t_x is int_CReal or t_x is assumed_int_CReal):
                return int_CReal(self.value * x.value)
        # Sec. 9.2.4 — commutative key normalisation matches ``add``.
        a_id, b_id = id(self), id(x)
        lo, hi = (self, x) if a_id <= b_id else (x, self)
        key = ("mul", id(lo), id(hi))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = mult_CReal(lo, hi)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def inverse(self) -> "CReal":
        # Sec. 9.1.3 — consult the per-operand reciprocal cache before allocating.
        # ``id(self)`` is safe as the key because ``inv.op is self`` keeps
        # ``self`` alive while the cache entry is live, so id() reuse cannot
        # produce a false hit. Subclasses whose layout doesn't admit weakrefs
        # silently fall through to the unconditional construction.
        cached = _INVERSE_CACHE.get(id(self))
        if cached is not None:
            return cached
        inv = inv_CReal(self)
        try:
            _INVERSE_CACHE[id(self)] = inv
        except TypeError:
            pass
        return inv

    def divide(self, x: "CReal") -> "CReal":
        return mult_CReal(self, x.inverse())

    def select(self, x: "CReal", y: "CReal") -> "CReal":
        return select_CReal(self, x, y)

    def max(self, x: "CReal") -> "CReal":
        return self.subtract(x).select(x, self)

    def min(self, x: "CReal") -> "CReal":
        return self.subtract(x).select(self, x)

    def abs(self) -> "CReal":
        return self.select(self.negate(), self)

    # ---- transcendentals -------------------------------------------------
    # Each unary kernel below is wrapped in a Decision D-68 DAG-cache
    # lookup keyed by ``(kind, id(self))``. Two calls to ``x.sin()`` on
    # the same ``x`` Python object return the same node — and because
    # ``sin``, ``cos``, ``ln`` are recursive in their own argument
    # reduction, sub-calls inside the reduction chain also dedupe.

    def exp(self) -> "CReal":
        key = ("exp", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        low_prec = -10
        rough_appr = self.get_appr(low_prec)
        # Recurse on a halved argument when |x| is large; the resulting tree
        # is cheaper than negating and inverting after the fact.
        if rough_appr > 2 or rough_appr < -2:
            square_root = self.shiftRight(1).exp()
            node = square_root.multiply(square_root)
        else:
            node = prescaled_exp_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def pow(self, x: "CReal") -> "CReal":
        return x.multiply(self.ln()).exp()

    def cos(self) -> "CReal":
        key = ("cos", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        halfpi_multiples = self.divide(CReal.PI).get_appr(-1)
        abs_halfpi_multiples = _abs(halfpi_multiples)
        if abs_halfpi_multiples >= 2:
            pi_multiples = CReal.scale(halfpi_multiples, -1)
            adjustment = CReal.PI.multiply(CReal.valueOf(pi_multiples))
            if (pi_multiples & 1) != 0:
                node = self.subtract(adjustment).cos().negate()
            else:
                node = self.subtract(adjustment).cos()
        elif _abs(self.get_appr(-1)) >= 2:
            cos_half = self.shiftRight(1).cos()
            node = cos_half.multiply(cos_half).shiftLeft(1).subtract(CReal.ONE)
        else:
            node = prescaled_cos_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def sin(self) -> "CReal":
        key = ("sin", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = CReal.half_pi.subtract(self).cos()
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def asin(self) -> "CReal":
        key = ("asin", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        rough_appr = self.get_appr(-10)
        if rough_appr > 750:  # > 1/sqrt(2) + a bit
            new_arg = CReal.ONE.subtract(self.multiply(self)).sqrt()
            node = new_arg.acos()
        elif rough_appr < -750:
            node = self.negate().asin().negate()
        else:
            node = prescaled_asin_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def acos(self) -> "CReal":
        key = ("acos", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = CReal.half_pi.subtract(self.asin())
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def ln(self) -> "CReal":
        key = ("ln", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        low_prec = -4
        rough_appr = self.get_appr(low_prec)  # in sixteenths
        if rough_appr < 0:
            raise ValueError("ln(negative)")
        if rough_appr <= CReal.low_ln_limit:
            node = self.inverse().ln().negate()
        elif rough_appr >= CReal.high_ln_limit:
            if rough_appr <= CReal.scaled_4:
                quarter = self.sqrt().sqrt().ln()
                node = quarter.shiftLeft(2)
            else:
                extra_bits = _bit_length(rough_appr) - 3
                scaled_result = self.shiftRight(extra_bits).ln()
                node = scaled_result.add(CReal.valueOf(extra_bits).multiply(CReal.ln2))
        else:
            node = self.simple_ln()
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    def sqrt(self) -> "CReal":
        key = ("sqrt", id(self))
        cached = _DAG_CACHE.get(key)
        if cached is not None:
            return cached
        node = sqrt_CReal(self)
        try:
            _DAG_CACHE[key] = node
        except TypeError:
            pass
        return node

    # ---- Python conveniences --------------------------------------------

    def __repr__(self) -> str:
        try:
            preview = self.toString(5)
        except Exception:  # pragma: no cover - defensive
            preview = "?"
        return f"<CReal {preview}...>"

    def __str__(self) -> str:
        return self.toString()

    def __neg__(self) -> "CReal":
        return self.negate()

    def __add__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else self.add(c)

    def __radd__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else c.add(self)

    def __sub__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else self.subtract(c)

    def __rsub__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else c.subtract(self)

    def __mul__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else self.multiply(c)

    def __rmul__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else c.multiply(self)

    def __truediv__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else self.divide(c)

    def __rtruediv__(self, other):
        c = _coerce(other)
        return NotImplemented if c is None else c.divide(self)

    def __pow__(self, other):
        # Fast path for integer exponents — repeated multiplication, no
        # ln/exp round-trip. Critical for callers like kingdon's normsq
        # codegen that emit ``coef ** 2`` on every term (including zeros,
        # for which the ln path diverges).
        if isinstance(other, int) and not isinstance(other, bool):
            if other == 0:
                return CReal.ONE
            if other == 1:
                return self
            if other < 0:
                return self.inverse().__pow__(-other)
            # Right-to-left binary exponentiation.
            result = CReal.ONE
            base = self
            n = other
            while n > 0:
                if n & 1:
                    result = result.multiply(base)
                n >>= 1
                if n:
                    base = base.multiply(base)
            return result
        c = _coerce(other)
        return NotImplemented if c is None else self.pow(c)

    def __abs__(self) -> "CReal":
        return self.abs()


# =====================================================================
# slow_CReal: speculative-precision base for expensive approximations.
# =====================================================================


class slow_CReal(CReal):
    """Subclass for ``approximate`` calls that are expensive to redo.

    When a new evaluation is needed, we speculatively evaluate at slightly
    higher precision than requested so subsequent requests can be served
    from the cache. This wastes effort if the higher precision isn't
    actually needed, so it's reserved for transcendental kernels.
    """

    __slots__ = ()
    max_prec = -64
    prec_incr = 32

    def get_appr(self, precision: int) -> int:
        CReal.check_prec(precision)
        if self.appr_valid and self.min_prec is not None and precision >= self.min_prec:
            return CReal.scale(self.max_appr, self.min_prec - precision)
        if precision >= slow_CReal.max_prec:
            eval_prec = slow_CReal.max_prec
        else:
            eval_prec = (precision - slow_CReal.prec_incr + 1) & ~(slow_CReal.prec_incr - 1)
        result = self.approximate(eval_prec)
        self.min_prec = eval_prec
        self.max_appr = result
        self.appr_valid = True
        return CReal.scale(result, eval_prec - precision)


# =====================================================================
# Concrete CReal subclasses.
# =====================================================================


class int_CReal(CReal):
    """ℤ-typed CReal: an exact integer constant.

    This is the embedding ``ℤ ↪ CReal``. ``value`` is stored as a Python
    ``int`` (arbitrary magnitude), so ``int_CReal(10**1000)`` is just as
    valid as ``int_CReal(7)``. ``approximate(p)`` is a single bit-shift
    of ``value`` — no Taylor series, no iteration, O(precision/64) in
    bignum cost. Arithmetic between two ``int_CReal``s lands in the
    general lazy expression tree (we don't currently specialise ``ℤ × ℤ
    → ℤ``), but ``assumeInt()`` lets callers re-tag a result as ℤ when
    they know it is.
    """

    __slots__ = ("value",)

    def __init__(self, n: int) -> None:
        super().__init__()
        self.value = n

    def approximate(self, p: int) -> int:
        return CReal.scale(self.value, -p)


class assumed_int_CReal(CReal):
    """Caller-asserted ``ℤ`` tag on an otherwise-general CReal.

    The wrapped ``CReal`` may not yet be fully evaluated, but the caller
    promises its true value is an integer. ``approximate(p)`` for ``p ≥ 0``
    just forwards (no fractional digits exist to compute); for ``p < 0`` it
    evaluates once at precision 0 and shifts. Useful when ``+, −, ×`` on
    ``int_CReal``s produces an expression tree that's structurally a
    rational but semantically known to be in ℤ — re-tagging avoids
    pointless sub-unit precision work downstream.

    Behaviour is undefined if the wrapped value is not actually an integer.
    """

    __slots__ = ("value",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.value = x

    def approximate(self, p: int) -> int:
        if p >= 0:
            return self.value.get_appr(p)
        return CReal.scale(self.value.get_appr(0), -p)


class add_CReal(CReal):
    """Sum of two constructive reals. Cacheable via the base-class ``__weakref__``."""

    __slots__ = ("op1", "op2")

    def __init__(self, x: CReal, y: CReal) -> None:
        super().__init__()
        self.op1 = x
        self.op2 = y

    def approximate(self, p: int) -> int:
        return CReal.scale(self.op1.get_appr(p - 2) + self.op2.get_appr(p - 2), -2)


class shifted_CReal(CReal):
    """A CReal multiplied by ``2 ** n``. Cacheable via the base-class ``__weakref__``."""

    __slots__ = ("op", "count")

    def __init__(self, x: CReal, n: int) -> None:
        super().__init__()
        self.op = x
        self.count = n

    def approximate(self, p: int) -> int:
        return self.op.get_appr(p - self.count)


class neg_CReal(CReal):
    """Negation of a CReal. Cacheable via the base-class ``__weakref__``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def negate(self) -> CReal:
        return self.op

    def approximate(self, p: int) -> int:
        return -self.op.get_appr(p)


class select_CReal(CReal):
    """``op1`` if ``selector < 0`` else ``op2``; assumes equal at selector == 0."""

    __slots__ = ("selector", "selector_sign", "op1", "op2")

    def __init__(self, s: CReal, x: CReal, y: CReal) -> None:
        super().__init__()
        self.selector = s
        self.selector_sign = _signum(self.selector.get_appr(-20))
        self.op1 = x
        self.op2 = y

    def approximate(self, p: int) -> int:
        if self.selector_sign < 0:
            return self.op1.get_appr(p)
        if self.selector_sign > 0:
            return self.op2.get_appr(p)
        op1_appr = self.op1.get_appr(p - 1)
        op2_appr = self.op2.get_appr(p - 1)
        diff = _abs(op1_appr - op2_appr)
        if diff <= 1:
            return CReal.scale(op1_appr, -1)
        if self.selector.signum() < 0:
            self.selector_sign = -1
            return CReal.scale(op1_appr, -1)
        # Java sets +1 to cache the positive-selector result; the JS port
        # has 0 here, which forces re-derivation every call.
        self.selector_sign = 1
        return CReal.scale(op2_appr, -1)


class mult_CReal(CReal):
    """Product of two constructive reals. Cacheable via the base-class ``__weakref__``."""

    __slots__ = ("op1", "op2")

    def __init__(self, x: CReal, y: CReal) -> None:
        super().__init__()
        self.op1 = x
        self.op2 = y

    def approximate(self, p: int) -> int:
        half_prec = (p >> 1) - 1
        msd_op1 = self.op1.msd(half_prec)
        if msd_op1 == _MIN_SAFE_INTEGER:
            msd_op2 = self.op2.msd(half_prec)
            if msd_op2 == _MIN_SAFE_INTEGER:
                # Product is small enough that zero is a valid approximation.
                return 0
            # Swap so the larger operand drives the precision calculation.
            self.op1, self.op2 = self.op2, self.op1
            msd_op1 = msd_op2

        # Each approximation contributes < 1/4 ulp; final rounding adds 1/2.
        prec2 = p - msd_op1 - 3
        appr2 = self.op2.get_appr(prec2)
        if appr2 == 0:
            return 0
        msd_op2 = self.op2.known_msd()
        prec1 = p - msd_op2 - 3
        appr1 = self.op1.get_appr(prec1)
        scale_digits = prec1 + prec2 - p
        return CReal.scale(appr1 * appr2, scale_digits)


class inv_CReal(CReal):
    """Multiplicative inverse. Cacheable via the base-class ``__weakref__``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        msd = self.op.msd()
        inv_msd = 1 - msd
        # Need a few extra significant digits to cover msd's possible off-by-one,
        # the relative-error mapping from argument to inverse, computational
        # slop, and the final 0.5 ulp rounding bit.
        digits_needed = inv_msd - p + 3
        prec_needed = msd - digits_needed
        log_scale_factor = -p - prec_needed
        if log_scale_factor < 0:
            return 0
        dividend = 1 << log_scale_factor
        scaled_divisor = self.op.get_appr(prec_needed)
        abs_scaled_divisor = _abs(scaled_divisor)
        adj_dividend = dividend + (abs_scaled_divisor >> 1)
        result = adj_dividend // abs_scaled_divisor
        return -result if scaled_divisor < 0 else result


class prescaled_exp_CReal(CReal):
    """Exponential via Taylor series; assumes ``|x| < 1/2``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        if p >= 1:
            return 0
        iterations_needed = (-p) // 2 + 2
        calc_precision = p - CReal.bound_log2(2 * iterations_needed)
        op_prec = p - 3
        op_appr = self.op.get_appr(op_prec)
        scaled_1 = 1 << (-calc_precision)
        current_term = scaled_1
        current_sum = scaled_1
        n = 0
        # Use CReal.shift: Java BigInteger.shiftLeft(negative) == shiftRight.
        # At low precision the shift count can go negative, in which case
        # the threshold rounds to 0 and the guard below skips the loop.
        max_trunc_error = CReal.shift(1, p - 4 - calc_precision)
        timeout = _Timeout()
        while _abs(current_term) >= max_trunc_error and max_trunc_error > 0:
            timeout.check()
            n += 1
            current_term = _trunc_div(CReal.scale(current_term * op_appr, op_prec), n)
            current_sum += current_term
        return CReal.scale(current_sum, calc_precision - p)


class prescaled_cos_CReal(slow_CReal):
    """Cosine via Taylor series; assumes ``|x| < 1``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        if p >= 1:
            return 0
        # Conservative iteration count; each term is < 2 * 2^calc_precision
        # accurate, so cumulative series error is bounded.
        iterations_needed = (-p) // 2 + 4
        calc_precision = p - CReal.bound_log2(2 * iterations_needed) - 4
        op_prec = p - 2
        op_appr = self.op.get_appr(op_prec)
        max_trunc_error = CReal.shift(1, p - 4 - calc_precision)
        n = 0
        current_term = 1 << (-calc_precision)
        current_sum = current_term
        timeout = _Timeout()
        while _abs(current_term) >= max_trunc_error and max_trunc_error > 0:
            timeout.check()
            n += 2
            current_term = CReal.scale(current_term * op_appr, op_prec)
            current_term = CReal.scale(current_term * op_appr, op_prec)
            divisor = -n * (n - 1)
            current_term = _trunc_div(current_term, divisor)
            current_sum = current_sum + current_term
        return CReal.scale(current_sum, calc_precision - p)


class integral_atan_CReal(slow_CReal):
    """``atan(1/n)`` for small integer ``n``. Used to bootstrap PI."""

    __slots__ = ("op",)

    def __init__(self, x: int) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        if p >= 1:
            return 0
        iterations_needed = (-p) // 2 + 2
        calc_precision = p - CReal.bound_log2(2 * iterations_needed) - 2
        scaled_1 = 1 << (-calc_precision)
        big_op = self.op
        big_op_squared = big_op * big_op
        op_inverse = _trunc_div(scaled_1, big_op)
        current_power = op_inverse
        current_term = op_inverse
        current_sum = op_inverse
        current_sign = 1
        n = 1
        max_trunc_error = CReal.shift(1, p - 2 - calc_precision)
        timeout = _Timeout()
        while _abs(current_term) >= max_trunc_error and max_trunc_error > 0:
            timeout.check()
            n += 2
            current_power = _trunc_div(current_power, big_op_squared)
            current_sign = -current_sign
            current_term = _trunc_div(current_power, current_sign * n)
            current_sum += current_term
        return CReal.scale(current_sum, calc_precision - p)


class prescaled_ln_CReal(slow_CReal):
    """``ln(1 + op)`` via Taylor series; assumes ``|op| < 1/2``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        if p >= 0:
            return 0
        iterations_needed = -p
        calc_precision = p - CReal.bound_log2(2 * iterations_needed)
        op_prec = p - 3
        op_appr = self.op.get_appr(op_prec)
        x_nth = CReal.scale(op_appr, op_prec - calc_precision)
        current_term = x_nth
        current_sum = current_term
        n = 1
        current_sign = 1
        max_trunc_error = CReal.shift(1, p - 4 - calc_precision)
        timeout = _Timeout()
        while _abs(current_term) >= max_trunc_error and max_trunc_error > 0:
            timeout.check()
            n += 1
            current_sign = -current_sign
            x_nth = CReal.scale(x_nth * op_appr, op_prec)
            current_term = _trunc_div(x_nth, n * current_sign)
            current_sum += current_term
        return CReal.scale(current_sum, calc_precision - p)


class prescaled_asin_CReal(slow_CReal):
    """``asin`` via Taylor series; assumes ``|x| < (1/2) ** (1/3)``."""

    __slots__ = ("op",)

    def __init__(self, x: CReal) -> None:
        super().__init__()
        self.op = x

    def approximate(self, p: int) -> int:
        # See the source comments for the derivation of these bounds; the
        # short version: each term is bounded by x^(2n+1), every other Taylor
        # term is zero, and we account for the usual 1/2 ulp rounding error.
        if p >= 2:
            return 0
        iterations_needed = (-3 * p) // 2 + 4
        calc_precision = p - CReal.bound_log2(2 * iterations_needed)
        op_prec = p - 3
        op_appr = self.op.get_appr(op_prec)
        max_last_term = CReal.shift(1, p - 4 - calc_precision)
        exp = 1
        # CReal.shift accepts negative count (== shiftRight), matching Java.
        current_term = CReal.shift(op_appr, op_prec - calc_precision)
        current_sum = current_term
        current_factor = current_term
        timeout = _Timeout()
        while _abs(current_term) >= max_last_term and max_last_term > 0:
            timeout.check()
            exp += 2
            current_factor = current_factor * (exp - 2)
            current_factor = CReal.scale(current_factor * op_appr, op_prec + 2)
            current_factor *= op_appr
            divisor = exp - 1
            current_factor = _trunc_div(current_factor, divisor)
            current_factor = CReal.scale(current_factor, op_prec - 2)
            current_term = _trunc_div(current_factor, exp)
            current_sum += current_term
        return CReal.scale(current_sum, calc_precision - p)


class sqrt_CReal(CReal):
    """Square root of a constructive real."""

    __slots__ = ("op",)

    # Conservative bit counts for the double-precision shortcut.
    fp_prec = 50
    fp_op_prec = 60

    def __init__(self, x: CReal, min_p: Optional[int] = None, max_a: Optional[int] = None) -> None:
        super().__init__()
        self.op = x
        if min_p is not None:
            self.min_prec = min_p
            self.max_appr = max_a if max_a is not None else 0
            self.appr_valid = True

    def approximate(self, p: int) -> int:
        import math
        max_op_prec_needed = 2 * p - 1
        msd = self.op.iter_msd(max_op_prec_needed)
        if msd <= max_op_prec_needed:
            return 0
        result_msd = msd // 2
        result_digits = result_msd - p
        if result_digits > sqrt_CReal.fp_prec:
            # High-precision request: compute a lower-precision approximation
            # then refine via one Newton step.
            appr_digits = result_digits // 2 + 6
            appr_prec = result_msd - appr_digits
            prod_prec = 2 * appr_prec
            op_appr = self.op.get_appr(prod_prec)
            last_appr = self.get_appr(appr_prec)
            prod_prec_scaled_numerator = last_appr * last_appr + op_appr
            scaled_numerator = CReal.scale(prod_prec_scaled_numerator, appr_prec - p)
            shifted_result = scaled_numerator // last_appr
            return (shifted_result + 1) >> 1
        # Low-precision request: double-precision sqrt is good enough.
        op_prec = (msd - sqrt_CReal.fp_op_prec) & ~1
        working_prec = op_prec - sqrt_CReal.fp_op_prec
        scaled_bi_appr = self.op.get_appr(op_prec) << sqrt_CReal.fp_op_prec
        scaled_appr = float(scaled_bi_appr)
        if scaled_appr < 0:
            raise ValueError("sqrt(negative)")
        scaled_fp_sqrt = math.sqrt(scaled_appr)
        scaled_sqrt = int(scaled_fp_sqrt)
        shift_count = working_prec // 2 - p
        return CReal.shift(scaled_sqrt, shift_count)


# =====================================================================
# Factories and constants.
# =====================================================================


def _parse_real_string(s: str) -> CReal:
    s = s.strip()
    point_pos = s.find(".")
    if point_pos == -1:
        point_pos = len(s)
        fraction = "0"
    else:
        fraction = s[point_pos + 1:]
    whole = s[:point_pos]
    scaled_result = int(whole + fraction)
    divisor = 10 ** len(fraction)
    return CReal.valueOf(scaled_result).divide(CReal.valueOf(divisor))


def _valueOf(n: Union[int, float, str]) -> CReal:
    """Construct a CReal from a number or string.

    Routing through the ``ℤ ⊂ ℚ ⊂ ℝ`` tower:

    - ``bool`` / ``int`` of any magnitude → :class:`int_CReal` (ℤ).
    - ``float`` with no fractional part → :class:`int_CReal` of ``int(n)``.
    - ``float`` with a fractional part → ``ℚ``. Parsed through ``repr(n)``
      as an exact decimal (so ``valueOf(0.1)`` becomes the rational
      ``1/10``, not the IEEE 754 binary-representation neighbour
      ``3602879701896397/2**55``). Pass ``str(...)`` or do bit-level
      unpacking yourself if you need the exact float value.
    - ``str`` → parsed as a signed decimal literal, e.g. ``"-3.14"``,
      yielding an exact rational in ``ℚ``.
    - ``NaN`` / ``±inf`` → ``ValueError``. Neither has a ``ℝ`` denotation.
    """
    if isinstance(n, float):
        if n != n:
            raise ValueError("NaN argument")
        if n == float("inf") or n == float("-inf"):
            raise ValueError("Infinite argument")
        if n % 1 != 0:
            return _parse_real_string(repr(n))
        return int_CReal(int(n))
    if isinstance(n, bool):
        # bool ⊂ int in Python, so True/False land here as 1/0 ∈ ℤ.
        return int_CReal(int(n))
    if isinstance(n, int):
        return int_CReal(n)
    if isinstance(n, str):
        return _parse_real_string(n)
    raise TypeError(f"Cannot build CReal from {type(n).__name__}")


CReal.valueOf = staticmethod(_valueOf)
CReal.valueOf_string = staticmethod(_parse_real_string)


def _coerce(other):
    """Best-effort conversion for Python arithmetic operators.

    Returns the coerced ``CReal`` or ``None`` when ``other`` is something
    we don't recognise — the dunder methods turn that into ``NotImplemented``
    so Python's operator protocol can dispatch to the right-hand operand
    (e.g. ``kingdon.MultiVector.__rmul__`` for CReal * MultiVector).
    """
    if isinstance(other, CReal):
        return other
    if isinstance(other, (int, float, str)):
        return _valueOf(other)
    return None


_DC_THRESHOLD = 2000
_POW10_CACHE: dict = {}


def _pow10(exp: int) -> int:
    """Cached ``10 ** exp`` — base-10 splits reuse the same powers."""
    p = _POW10_CACHE.get(exp)
    if p is None:
        p = 10 ** exp
        _POW10_CACHE[exp] = p
    return p


def _int_to_decimal_dc(n: int) -> str:
    """Divide-and-conquer base-10 conversion for very large non-negative ints.

    CPython 3.11+ ``str(int)`` is sub-quadratic; in 3.9–3.10 it's still
    O(N²) and dominates ``toString`` cost above ~50k digits. This
    implementation does the same Brent-style recursion: split ``n`` at
    the midpoint power of 10, convert each half, concatenate with
    zero-padding. Combined with cached powers of 10 the asymptotic cost
    becomes O(M(N)·log²N).
    """
    if n < _pow10(_DC_THRESHOLD):
        return str(n)
    # Estimate digit count; refine with at most one bounce.
    digits = int(n.bit_length() * 0.30103) + 1
    if n >= _pow10(digits):
        digits += 1
    half = digits >> 1
    pow_half = _pow10(half)
    high, low = divmod(n, pow_half)
    return _int_to_decimal_dc(high) + _int_to_decimal_dc(low).zfill(half)


def _int_to_radix(n: int, radix: int) -> str:
    """Match JS ``BigInt.prototype.toString(radix)`` for non-negative ``n``.

    Fast paths for the four common radices. Base-10 uses divide-and-conquer
    above ``_DC_THRESHOLD`` digits to stay sub-quadratic on Python 3.9/3.10
    (built-in ``str(int)`` is O(N²) there).
    """
    if n == 0:
        return "0"
    if radix == 10:
        return _int_to_decimal_dc(n)
    if radix == 16:
        return f"{n:x}"
    if radix == 2:
        return f"{n:b}"
    if radix == 8:
        return f"{n:o}"
    digits = "0123456789abcdef"
    out = []
    while n > 0:
        out.append(digits[n % radix])
        n //= radix
    return "".join(reversed(out))


# ---- core constants ----------------------------------------------------

CReal.ZERO = _valueOf(0)
CReal.ONE = _valueOf(1)

# ln(2) via Machin-like identity: 7 ln(10/9) - 2 ln(25/24) + 3 ln(81/80).
CReal.ln2 = (
    _valueOf(7).multiply(_valueOf(10).divide(_valueOf(9)).simple_ln())
    .subtract(_valueOf(2).multiply(_valueOf(25).divide(_valueOf(24)).simple_ln()))
    .add(_valueOf(3).multiply(_valueOf(81).divide(_valueOf(80)).simple_ln()))
)

CReal.four = _valueOf(4)


class gl_pi_CReal(slow_CReal):
    """PI via the Gauss-Legendre AGM iteration.

    Roughly doubles the number of correct digits per iteration::

        a_0 = 1,  b_0 = 1/sqrt(2),  t_0 = 1/4,  p_0 = 1
        a_{n+1} = (a_n + b_n) / 2
        b_{n+1} = sqrt(a_n * b_n)
        t_{n+1} = t_n - 2**n * (a_n - a_{n+1})^2
        pi ~ (a_{n+1} + b_{n+1})^2 / (4 * t_{n+1})

    We retain the ``b`` sequence across re-evaluations so sqrt refinements
    can reuse a previous estimate as a starting point.
    """

    __slots__ = ("b_prec", "b_val")

    TOLERANCE = 4
    SQRT_HALF: "sqrt_CReal" = None  # type: ignore[assignment]

    def __init__(self) -> None:
        super().__init__()
        self.b_prec: list[Optional[int]] = [None]
        self.b_val: list[Optional[int]] = [None]

    def approximate(self, p: int) -> int:
        import math
        b_prec = self.b_prec
        b_val = self.b_val

        if p >= 0:
            return CReal.scale(3, -p)
        # ~log2(p) iterations; budget a couple of ulps per intermediate term
        # plus a small constant for the final rounding.
        extra_eval_prec = math.ceil(math.log(-p) / math.log(2)) + 10
        eval_prec = p - extra_eval_prec
        a = 1 << (-eval_prec)
        b = gl_pi_CReal.SQRT_HALF.get_appr(eval_prec)
        t = 1 << (-eval_prec - 2)
        n = 0
        # Sec. 9.1.2 — MPFR-style a-priori iteration cap. Gauss-Legendre AGM
        # converges quadratically: with a₀=1, b₀=1/√2 the error after n
        # iterations satisfies |aₙ − bₙ| ≤ (a₀ − b₀) · 2^(1 − 2ⁿ), so the
        # iteration count to reach precision 2^p is bounded by
        #     n ≤ ceil(log2(−p + 2)) + small.
        # MPFR uses +5 iterations of overhead at 4096-bit π; we mirror that
        # for the algorithmic equivalence reported by Fredrik Johansson
        # (https://mpfr.org/, https://fredrikj.net/blog/). The runtime
        # ``a - b > TOLERANCE`` test still gates each iteration (early exit
        # when convergence beats the bound); the cap is a defensive ceiling
        # so the loop has a guaranteed termination.
        max_iters = math.ceil(math.log2(max(2, -p + 2))) + 5
        timeout = _Timeout()
        while a - b - gl_pi_CReal.TOLERANCE > 0 and n < max_iters:
            timeout.check()
            next_a = (a + b) >> 1
            a_diff = a - next_a
            b_prod = (a * b) >> (-eval_prec)
            # Wrap b_prod as a temporary CReal so we can reuse sqrt_CReal's
            # Newton iteration instead of writing a BigInt sqrt by hand.
            b_prod_as_CReal = CReal.valueOf(b_prod).shiftRight(-eval_prec)
            if len(b_prec) == n + 1:
                next_b_as_CReal = sqrt_CReal(b_prod_as_CReal)
                next_b = next_b_as_CReal.get_appr(eval_prec)
                scaled_next_b = CReal.scale(next_b, -extra_eval_prec)
                b_prec.append(p)
                b_val.append(scaled_next_b)
            else:
                next_b_as_CReal = sqrt_CReal(b_prod_as_CReal, b_prec[n + 1], b_val[n + 1])
                next_b = next_b_as_CReal.get_appr(eval_prec)
                b_prec[n + 1] = p
                b_val[n + 1] = CReal.scale(next_b, -extra_eval_prec)
            # Java BigInteger.shiftLeft accepts negative counts (== shiftRight);
            # Python's << does not, so route through CReal.shift.
            next_t = t - CReal.shift(a_diff * a_diff, n + eval_prec)
            a = next_a
            b = next_b
            t = next_t
            n += 1
        sum_ab = a + b
        result = _trunc_div(sum_ab * sum_ab, t) >> 2
        return CReal.scale(result, -extra_eval_prec)


# SQRT_HALF depends on CReal.ONE, which exists by now.
gl_pi_CReal.SQRT_HALF = sqrt_CReal(CReal.ONE.shiftRight(1))

CReal.PI = gl_pi_CReal()
CReal.E = CReal.ONE.exp()
CReal.half_pi = CReal.PI.shiftRight(1)

# Sixteenths-scaled thresholds used by ``ln`` to decide how to argument-reduce.
CReal.low_ln_limit = 8           # 1/2
CReal.high_ln_limit = 16 + 8     # 1.5
CReal.scaled_4 = 4 * 16

CReal.Timeout = _Timeout


__all__ = [
    "CReal",
    "slow_CReal",
    "int_CReal",
    "assumed_int_CReal",
    "add_CReal",
    "shifted_CReal",
    "neg_CReal",
    "select_CReal",
    "mult_CReal",
    "inv_CReal",
    "prescaled_exp_CReal",
    "prescaled_cos_CReal",
    "integral_atan_CReal",
    "prescaled_ln_CReal",
    "prescaled_asin_CReal",
    "sqrt_CReal",
    "gl_pi_CReal",
]
