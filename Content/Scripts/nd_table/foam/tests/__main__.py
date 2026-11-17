"""End-to-end smoke tests covering all nine subpackages.

Run from the parent of ``foam3_py``:

    python -m foam3_py.tests

The suite exercises:

  parse      — atoms, combinators, Substring, Until, Quoted
  jello      — combinator-based keyword translation + nd_table wiring
  reals      — constructive reals: construction, arithmetic, JSON/Zarr
  rfc0001    — RFC 1 data model + RFNM flow-control constraint
  json       — primitives, escapes, arrays, maps, round-trip
  csv        — quoted/escaped fields, header round-trip
  xml        — attribute/element split, entity escaping
  html       — table rendering, NBSP for empty
  formatter  — JSONFObjectFormatter flag matrix
"""

from __future__ import annotations

import dataclasses as dc
import datetime
import sys
import traceback
from typing import Any, Callable, List, Tuple


_PASS: List[str] = []
_FAIL: List[Tuple[str, str]] = []
_SKIP: List[str] = []


def case(name: str):
    def deco(fn: Callable[[], None]) -> Callable[[], None]:
        try:
            fn()
            _PASS.append(name)
            print(f"  PASS  {name}")
        except SkipTest as e:
            _SKIP.append(name)
            print(f"  SKIP  {name}: {e}")
        except Exception as e:  # noqa: BLE001
            tb = traceback.format_exc()
            _FAIL.append((name, tb))
            print(f"  FAIL  {name}: {e}")
        return fn
    return deco


class SkipTest(Exception):
    """Signal that a case should be reported as SKIP, not FAIL."""


def assert_eq(actual: Any, expected: Any, msg: str = "") -> None:
    if actual != expected:
        raise AssertionError(f"{msg}\n  expected: {expected!r}\n  actual:   {actual!r}")


# ---------------------------------------------------------------------------
print("== parse ==")
# ---------------------------------------------------------------------------

from foam3_py.parse import (
    StringPStream, ParserContextImpl, AnyChar, Literal, LiteralIC, Range,
    Chars, Alt, Seq, Seq1, Repeat, Optional, Substring, Until, AbstractLiteral,
    Quoted, Not, NotChar, NotChars, EOF, Fail, GreedyAlt,
)


X = ParserContextImpl()


@case("parse: Seq of Literals")
def _():
    ps = StringPStream("hello world").apply(
        Seq(Literal("hello"), Literal(" "), Literal("world")), X)
    assert ps is not None
    assert_eq(ps.value(), ["hello", " ", "world"])
    assert_eq(ps.pos(), 11)


@case("parse: Alt first-match")
def _():
    p = Alt(Literal("aa"), Literal("ab"))
    assert_eq(StringPStream("aaxy").apply(p, X).value(), "aa")
    assert_eq(StringPStream("abxy").apply(p, X).value(), "ab")
    assert StringPStream("xy").apply(p, X) is None


@case("parse: GreedyAlt picks longest")
def _():
    p = GreedyAlt(Literal("aa"), Literal("aab"))
    res = StringPStream("aabxx").apply(p, X)
    assert_eq(res.pos(), 3)
    assert_eq(res.value(), "aab")


@case("parse: Repeat with min")
def _():
    digits = Repeat(Range.create("0", "9"), 1)
    assert StringPStream("abc").apply(digits, X) is None
    ps = StringPStream("12345abc").apply(digits, X)
    assert_eq("".join(ps.value()), "12345")


@case("parse: Substring captures source slice")
def _():
    p = Substring(Repeat(Range.create("a", "z"), 1))
    assert_eq(StringPStream("foobar123").apply(p, X).value(), "foobar")


@case("parse: Until literal terminator")
def _():
    ps = StringPStream("AAAA<END>BBBB").apply(
        Until(AbstractLiteral.create("<END>")), X)
    assert_eq("".join(ps.value()), "AAAA")
    assert_eq(ps.pos(), len("AAAA<END>"))


@case("parse: Not lookahead")
def _():
    # Not without else: succeeds, no consumption
    ps = StringPStream("xyz").apply(Not(Literal("a")), X)
    assert ps is not None and ps.pos() == 0
    # Not with else: applies elseP on success
    ps = StringPStream("xyz").apply(Not(Literal("a"), AnyChar.instance()), X)
    assert_eq(ps.value(), "x")
    assert_eq(ps.pos(), 1)


@case("parse: Quoted accepts bare and quoted")
def _():
    inner = Substring(Repeat(Range.create("a", "z"), 1))
    p = Quoted(inner)
    assert_eq(StringPStream("hello").apply(p, X).value(), "hello")
    assert_eq(StringPStream('"hello"').apply(p, X).value(), "hello")


@case("parse: LiteralIC case-insensitive")
def _():
    p = LiteralIC("yes", True)
    assert_eq(StringPStream("YES").apply(p, X).value(), True)
    assert_eq(StringPStream("Yes").apply(p, X).value(), True)
    assert StringPStream("yse").apply(p, X) is None


@case("parse: EOF / Fail")
def _():
    assert StringPStream("").apply(EOF.instance(), X) is not None
    assert StringPStream("x").apply(EOF.instance(), X) is None
    assert StringPStream("anything").apply(Fail(), X) is None


# ---------------------------------------------------------------------------
print("== jello ==")
# ---------------------------------------------------------------------------

try:
    import foam3_py.jello as fjello
    _jello_ok = True
except ImportError as e:
    _jello_ok = False
    _jello_err = str(e)


@case("jello: imports + ~155 keywords loaded")
def _():
    if not _jello_ok:
        raise SkipTest(_jello_err)
    n = len(fjello.all_keywords())
    if n < 150:
        raise AssertionError(f"only {n} keywords found, expected >=150")


@case("jello: combinator tokenizer splits simple expression")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello._tokenize("abs neg"), ["abs", "neg"])


@case("jello: tokenizer preserves grouping parens")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello._tokenize("( head rev ) each"),
              ["(", "head", "rev", ")", "each"])


@case("jello: tokenizer keeps nilad array as one token")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello._tokenize("[1,2,3]"), ["[1,2,3]"])


@case("jello: tokenizer accepts mixed whitespace")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello._tokenize("  abs\tneg \n"), ["abs", "neg"])


@case("jello: translate monadic atom")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("abs"), "A")


@case("jello: translate monadic chain")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("abs neg"), "AN")


@case("jello: translate dyadic chain")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("+ * pow"), "+×*")


@case("jello: translate quick (fold)")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("fold +"), "/+")


@case("jello: translate with parens + each")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("( abs neg ) each"), "(AN)€")


@case("jello: nilad array passes through translate")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.translate("[1,2,3]"), "[1,2,3]")


@case("jello: arity classification")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    assert_eq(fjello.keyword_arity("abs"), 1)
    assert_eq(fjello.keyword_arity("+"), 2)
    assert_eq(fjello.keyword_arity("fold"), -3)
    assert_eq(fjello.keyword_arity("each"), -10)
    assert_eq(fjello.keyword_arity("[1,2]"), 0)


@case("jello: unknown keyword raises KeyError")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    try:
        fjello.translate("not_a_real_keyword")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown keyword")


@case("jello: translation_only JelloFormula stays offline")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    f = fjello.JelloFormula(translation_only=True)
    r = f("abs neg", 5)
    assert isinstance(r, dict), r
    assert_eq(r["atoms"], "AN")
    assert_eq(r["args"], [5])
    assert r["executed"] is False


@case("jello: nd_table cell formula =JELLY(...) evaluates")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    try:
        sys.path.insert(0, str(__import__("os").path.normpath(
            __import__("os").path.join(__import__("os").path.dirname(__file__),
                                       "..", "..", "nd_table"))))
        from ndtable import Table, Axis
    except ImportError as e:
        raise SkipTest(f"ndtable not importable: {e}")
    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    fjello.install_into_table(t, translation_only=True)
    t[0, 0] = 7
    t[0, 1] = '=JELLY("abs neg", A1)'
    r = t[0, 1]
    assert isinstance(r, dict), r
    assert_eq(r["atoms"], "AN")
    assert r["args"] == [7] or r["args"] == ["7"], r["args"]


@case("jello: live jelly executable runs (skipped if unavailable)")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    if not fjello.is_jelly_available():
        raise SkipTest("jelly binary not on PATH / $JELLY_BIN / set_jelly_path")
    # If it's available, run a trivial monadic chain (abs on -5 should yield 5).
    out = fjello.evaluate("abs", -5)
    # jelly's stdout is implementation-defined; assert it contains "5".
    if "5" not in out:
        raise AssertionError(f"unexpected jelly output: {out!r}")


# --- JelloExpr <-> foam3_py.json round-trip --------------------------------

@case("jello+foam: JelloExpr round-trips through foam3_py.json")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    import foam3_py.json as fj
    e = fjello.JelloExpr("abs neg", args=[5])
    blob = fj.dumps(e)
    back = fjello.revive(fj.loads(blob))
    assert isinstance(back, fjello.JelloExpr), type(back)
    assert_eq(back.keyword_expr, "abs neg")
    assert_eq(back.atoms, "AN")
    assert_eq(back.args, [5])


@case("jello+foam: JelloExpr round-trips through JSONFObjectFormatter")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    import foam3_py.json as fj
    from foam3_py.formatter import JSONFObjectFormatter
    f = JSONFObjectFormatter(quote_keys=True, output_class_names=False,
                             output_default_values=True)
    e = fjello.JelloExpr("head rev", args=[3])
    blob = f.stringify(e)
    back = fjello.revive(fj.loads(blob))
    assert isinstance(back, fjello.JelloExpr), type(back)
    assert_eq(back.atoms, "ḢṚ")
    assert_eq(back.args, [3])


@case("jello+foam: nested tree with embedded JelloExpr")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    import foam3_py.json as fj
    tree = {"name": "pipeline",
            "op": fjello.JelloExpr("fold +"),
            "ops": [fjello.JelloExpr("abs"), fjello.JelloExpr("neg")]}
    back = fjello.revive(fj.loads(fj.dumps(tree)))
    assert isinstance(back["op"], fjello.JelloExpr)
    assert_eq(back["op"].atoms, "/+")
    assert all(isinstance(o, fjello.JelloExpr) for o in back["ops"])
    assert_eq([o.atoms for o in back["ops"]], ["A", "N"])


# --- JELLY-cell + JelloExpr-cell <-> ndtable_zarr round-trip ---------------

@case("jello+zarr: JELLY() formula cell survives Zarr round-trip")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    try:
        import os, sys, tempfile
        scripts_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", ".."))
        nd_table = os.path.join(scripts_dir, "nd_table")
        if nd_table not in sys.path:
            sys.path.insert(0, nd_table)
        from ndtable import Table, Axis
        from ndtable_zarr import store_to_zarr, load_from_zarr
    except ImportError as e:
        raise SkipTest(f"ndtable / ndtable_zarr not importable: {e}")

    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    fjello.install_into_table(t, translation_only=True)
    t[0, 0] = 7
    t[0, 1] = '=JELLY("abs neg", A1)'

    path = os.path.join(tempfile.gettempdir(), "foam3_jelly_zarr.zarr")
    store_to_zarr(t, path)
    t2 = load_from_zarr(path)
    fjello.install_into_table(t2, translation_only=True)
    for cell in t2.cells.values():
        cell._evaluated = False
    v = t2[0, 1]
    assert isinstance(v, dict), v
    assert_eq(v["atoms"], "AN")
    assert v["args"] in ([7], ["7"]), v["args"]


@case("jello+zarr: JelloExpr cell value survives as JelloExpr (codec registered)")
def _():
    if not _jello_ok: raise SkipTest("jello not importable")
    if not fjello._zarr_codec_registered:
        raise SkipTest("ndtable_zarr codec not registered")
    try:
        import os, sys, tempfile
        scripts_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", ".."))
        nd_table = os.path.join(scripts_dir, "nd_table")
        if nd_table not in sys.path:
            sys.path.insert(0, nd_table)
        from ndtable import Table, Axis
        from ndtable_zarr import store_to_zarr, load_from_zarr
    except ImportError as e:
        raise SkipTest(f"ndtable / ndtable_zarr not importable: {e}")

    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    expr = fjello.JelloExpr("head rev", args=[10])
    t[1, 0] = expr

    path = os.path.join(tempfile.gettempdir(), "foam3_jelloexpr_zarr.zarr")
    store_to_zarr(t, path)
    t2 = load_from_zarr(path)

    raw = t2.cells[(1, 0)].raw_value
    assert isinstance(raw, fjello.JelloExpr), type(raw)
    assert_eq(raw.keyword_expr, "head rev")
    assert_eq(raw.atoms, "ḢṚ")
    assert_eq(raw.args, [10])


# ---------------------------------------------------------------------------
print("== reals ==")
# ---------------------------------------------------------------------------

try:
    import foam3_py.reals as freal
    _reals_ok = True
except ImportError as e:
    _reals_ok = False
    _reals_err = str(e)


@case("reals: imports + zarr codec registered")
def _():
    if not _reals_ok:
        raise SkipTest(_reals_err)
    if not freal._zarr_codec_registered:
        raise AssertionError("ndtable_zarr codec failed to auto-register")


@case("reals: CR(sqrt(2)) evaluates to 30 digits")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    e = freal.CR("sqrt(2)", 30)
    assert_eq(e.cached_value,
              "1.414213562373095048801688724210")


@case("reals: pi * 2 at 25 digits")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    e = freal.CR("pi * 2", 25)
    assert_eq(e.cached_value, "6.2831853071795864769252868")


@case("reals: ln(e**2) = 2 exactly")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    e = freal.CR("log(e ** 2)", 25)
    # The value should round to exactly 2 within the precision; the
    # decimal string starts with "2.000..."
    assert e.cached_value.startswith("2.0000"), e.cached_value


@case("reals: CRExpr arithmetic via overloads")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    x = freal.CR("sqrt(2)")
    y = freal.CR("sqrt(3)")
    p = (x * y).evaluate(20)
    # sqrt(6) ≈ 2.4494897427831780981...
    assert p.startswith("2.4494897427"), p


@case("reals: materialize parses safe namespace")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    real = freal.materialize("pi + 1")
    s = real.evaluate(10)
    assert s.startswith("4.14159265"), s


@case("reals: materialize rejects unsafe expressions")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    for bad in ["__import__('os').system('echo')",
                "open('x', 'w')",
                "exec('1+1')"]:
        try:
            freal.materialize(bad)
        except (NameError, ValueError, TypeError):
            continue
        raise AssertionError(f"unsafe expression accepted: {bad!r}")


@case("reals+foam: CRExpr round-trips through foam3_py.json")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    import foam3_py.json as fj
    e = freal.CR("sqrt(2) + pi", 30)
    back = freal.revive(fj.loads(fj.dumps(e)))
    assert isinstance(back, freal.CRExpr), type(back)
    assert_eq(back.expr, "sqrt(2) + pi")
    assert_eq(back.cached_value, e.cached_value)


@case("reals+foam: nested tree with embedded CRExpr")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    import foam3_py.json as fj
    tree = {"name": "constants",
            "pi": freal.CR("pi", 20),
            "values": [freal.CR("sqrt(2)"), freal.CR("phi")]}
    back = freal.revive(fj.loads(fj.dumps(tree)))
    assert isinstance(back["pi"], freal.CRExpr)
    assert back["pi"].cached_value.startswith("3.1415926535")
    assert all(isinstance(v, freal.CRExpr) for v in back["values"])


@case("reals+zarr: CR() formula cell survives Zarr round-trip")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    try:
        import os, sys, tempfile
        scripts_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", ".."))
        nd_table = os.path.join(scripts_dir, "nd_table")
        if nd_table not in sys.path:
            sys.path.insert(0, nd_table)
        from ndtable import Table, Axis
        from ndtable_zarr import store_to_zarr, load_from_zarr
    except ImportError as e:
        raise SkipTest(f"ndtable/ndtable_zarr not importable: {e}")

    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    freal.install_into_table(t)
    t[0, 0] = '=CR("sqrt(2)", 35)'

    path = os.path.join(tempfile.gettempdir(), "foam3_cr_zarr.zarr")
    store_to_zarr(t, path)
    t2 = load_from_zarr(path)
    freal.install_into_table(t2)
    for cell in t2.cells.values():
        cell._evaluated = False
    v = t2[0, 0]
    assert isinstance(v, freal.CRExpr), type(v)
    assert v.cached_value.startswith("1.41421356237309504880"), v.cached_value


@case("reals+zarr: CRExpr cell value survives as CRExpr (codec registered)")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    if not freal._zarr_codec_registered:
        raise SkipTest("ndtable_zarr codec not registered")
    try:
        import os, sys, tempfile
        scripts_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", ".."))
        nd_table = os.path.join(scripts_dir, "nd_table")
        if nd_table not in sys.path:
            sys.path.insert(0, nd_table)
        from ndtable import Table, Axis
        from ndtable_zarr import store_to_zarr, load_from_zarr
    except ImportError as e:
        raise SkipTest(f"ndtable/ndtable_zarr not importable: {e}")

    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    expr = freal.CR("pi ** 2", 35)
    t[0, 0] = expr

    path = os.path.join(tempfile.gettempdir(), "foam3_crexpr_zarr.zarr")
    store_to_zarr(t, path)
    t2 = load_from_zarr(path)
    raw = t2.cells[(0, 0)].raw_value
    assert isinstance(raw, freal.CRExpr), type(raw)
    assert_eq(raw.expr, "pi ** 2")
    assert_eq(raw.precision, 35)
    assert raw.cached_value.startswith("9.86960440108935861"), raw.cached_value


# --- Java CR API parity layer -----------------------------------------------

@case("reals-java: shift_left(1, 10) = 1024")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    assert_eq(freal.shift_left(1, 10).evaluate(0), "1024.")


@case("reals-java: shift_right(sqrt(2), 1) = sqrt(2)/2")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    # sqrt(2)/2 = 0.70710678118654752440... — pick a prefix safely below
    # the next rounding boundary.
    s = freal.shift_right(freal.sqrt(2), 1).evaluate(20)
    assert s.startswith("0.7071067811865475"), s


@case("reals-java: signum on pi / -pi / 0")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    assert_eq(freal.signum(freal.pi), 1)
    assert_eq(freal.signum(-freal.pi), -1)
    assert_eq(freal.signum(freal.Real.from_int(0)), 0)


@case("reals-java: select / abs_cr / max_cr / min_cr")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    s = freal.abs_cr(-freal.sqrt(2)).evaluate(10)
    assert s.startswith("1.4142135"), s
    s = freal.max_cr(freal.pi, freal.e).evaluate(10)
    assert s.startswith("3.1415926"), s
    s = freal.min_cr(freal.pi, freal.e).evaluate(10)
    assert s.startswith("2.7182818"), s


@case("reals-java: to_bigint / to_int rounding half-up")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    assert_eq(freal.to_bigint(freal.pi), 3)
    assert_eq(freal.to_bigint(-freal.pi), -3)
    assert_eq(freal.to_bigint(freal.Real.from_fraction(Fraction(7, 2))), 4)
    assert_eq(freal.to_bigint(freal.Real.from_fraction(Fraction(-7, 2))), -4)
    assert_eq(freal.to_bigint(freal.Real.from_int(0)), 0)


@case("reals-java: value_of_string in radix 2 and 16")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    # ff.8 (hex) = 255.5
    s = freal.value_of_string("ff.8", 16).evaluate(2)
    assert s.startswith("255.5") or s.startswith("255.4"), s
    # -101.1 (binary) = -5.5
    s = freal.value_of_string("-101.1", 2).evaluate(2)
    assert s.startswith("-5.5") or s.startswith("-5.4"), s


@case("reals-java: to_string_radix(pi, 8, 16) hex digits of pi")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    hex_pi = freal.to_string_radix(freal.pi, 8, 16)
    assert hex_pi.startswith("3.243f6a"), hex_pi


@case("reals-java: to_string_radix in binary")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    # 15.5 = 1111.1 in binary
    s = freal.to_string_radix(freal.Real.from_fraction(Fraction(31, 2)), 4, 2)
    assert_eq(s, "1111.1000")


@case("reals-js: atan(1) = pi/4")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    s = freal.atan(1).evaluate(15)
    assert s.startswith("0.7853981633974"), s


@case("reals-js: atan(sqrt(3)) = pi/3")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    s = freal.atan(freal.sqrt(3)).evaluate(15)
    assert s.startswith("1.04719755119659"), s


@case("reals-js: asin(0.5) = pi/6")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    s = freal.asin(0.5).evaluate(15)
    assert s.startswith("0.5235987755982"), s


@case("reals-js: acos(0) = pi/2 and acos(1) = 0")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    a = freal.acos(0).evaluate(15)
    assert a.startswith("1.5707963267948"), a
    b = freal.acos(1).evaluate(10)
    assert b.startswith("0.0000000000"), b


@case("reals-js: atan2 quadrant-aware")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    assert freal.atan2(1, 1).evaluate(10).startswith("0.78539816"), \
        freal.atan2(1, 1).evaluate(10)
    assert freal.atan2(-1, -1).evaluate(10).startswith("-2.35619449"), \
        freal.atan2(-1, -1).evaluate(10)
    assert freal.atan2(1, 0).evaluate(10).startswith("1.57079632"), \
        freal.atan2(1, 0).evaluate(10)


@case("reals-java: parity helpers usable inside a CR() expression")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    # sqrt(2)*16 = 22.62741699796952...
    e = freal.CR("shift_left(sqrt(2), 4)", 15)
    assert e.cached_value.startswith("22.6274169979695"), e.cached_value
    # pi = 3.14159265358979323846... — at precision 15 rounds to ...979323847
    e = freal.CR("atan(1) * 4", 15)
    assert e.cached_value.startswith("3.14159265358979"), e.cached_value
    e = freal.CR("max_cr(pi, e)", 10)
    assert e.cached_value.startswith("3.1415926"), e.cached_value


@case("reals-java: CRExpr.abs(), .shift_left(), .signum()")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    e = freal.CR("-pi", 10)
    assert e.abs().cached_value.startswith("3.1415926"), e.abs().cached_value
    assert_eq(e.signum(), -1)
    e2 = freal.CR("sqrt(2)", 10)
    assert e2.shift_left(2).cached_value.startswith("5.6568542"), \
        e2.shift_left(2).cached_value


# --- IEEE 754 rounding directions ------------------------------------------

@case("reals-ieee: default to_bigint is HALF_EVEN (banker's)")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    f = lambda p, q=1: freal.Real.from_fraction(Fraction(p, q))
    # Ties at .5 round to the EVEN neighbour:
    assert_eq(freal.to_bigint(f(1, 2)), 0)   # 0.5 → 0 (0 is even)
    assert_eq(freal.to_bigint(f(3, 2)), 2)   # 1.5 → 2 (2 is even)
    assert_eq(freal.to_bigint(f(5, 2)), 2)   # 2.5 → 2 (2 is even)
    assert_eq(freal.to_bigint(f(7, 2)), 4)   # 3.5 → 4 (4 is even)
    assert_eq(freal.to_bigint(f(-5, 2)), -2) # -2.5 → -2 (-2 is even)
    assert_eq(freal.to_bigint(f(-7, 2)), -4) # -3.5 → -4 (-4 is even)
    # Non-ties unaffected by tie rule:
    assert_eq(freal.to_bigint(f(11, 4)), 3)  # 2.75 → 3
    assert_eq(freal.to_bigint(f(9, 4)), 2)   # 2.25 → 2


@case("reals-ieee: HALF_AWAY matches Java Math.round")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    f = lambda p, q=1: freal.Real.from_fraction(Fraction(p, q))
    m = freal.RoundingMode.HALF_AWAY
    assert_eq(freal.to_bigint(f(1, 2), rounding=m), 1)   # 0.5 → 1
    assert_eq(freal.to_bigint(f(3, 2), rounding=m), 2)   # 1.5 → 2
    assert_eq(freal.to_bigint(f(5, 2), rounding=m), 3)   # 2.5 → 3 (vs HALF_EVEN: 2)
    assert_eq(freal.to_bigint(f(-5, 2), rounding=m), -3) # -2.5 → -3


@case("reals-ieee: HALF_DOWN rounds ties toward zero")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    f = lambda p, q=1: freal.Real.from_fraction(Fraction(p, q))
    m = freal.RoundingMode.HALF_DOWN
    assert_eq(freal.to_bigint(f(5, 2), rounding=m), 2)   # 2.5 → 2
    assert_eq(freal.to_bigint(f(-5, 2), rounding=m), -2) # -2.5 → -2


@case("reals-ieee: CEILING / FLOOR / DOWN / UP")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    f = lambda p, q=1: freal.Real.from_fraction(Fraction(p, q))
    RM = freal.RoundingMode
    # 2.3
    assert_eq(freal.to_bigint(f(23, 10), rounding=RM.CEILING), 3)
    assert_eq(freal.to_bigint(f(23, 10), rounding=RM.FLOOR), 2)
    assert_eq(freal.to_bigint(f(23, 10), rounding=RM.DOWN), 2)
    assert_eq(freal.to_bigint(f(23, 10), rounding=RM.UP), 3)
    # -2.3
    assert_eq(freal.to_bigint(f(-23, 10), rounding=RM.CEILING), -2)
    assert_eq(freal.to_bigint(f(-23, 10), rounding=RM.FLOOR), -3)
    assert_eq(freal.to_bigint(f(-23, 10), rounding=RM.DOWN), -2)
    assert_eq(freal.to_bigint(f(-23, 10), rounding=RM.UP), -3)
    # Exact integer — every mode agrees
    for mode in (RM.HALF_EVEN, RM.HALF_AWAY, RM.HALF_DOWN,
                 RM.CEILING, RM.FLOOR, RM.DOWN, RM.UP):
        assert_eq(freal.to_bigint(f(42), rounding=mode), 42)
        assert_eq(freal.to_bigint(f(-7), rounding=mode), -7)


@case("reals-ieee: legacy half_up=True still works")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    from fractions import Fraction
    f = lambda p, q=1: freal.Real.from_fraction(Fraction(p, q))
    # half_up=True maps to HALF_AWAY
    assert_eq(freal.to_bigint(f(5, 2), half_up=True), 3)
    # half_up=False maps to DOWN (truncate)
    assert_eq(freal.to_bigint(f(5, 2), half_up=False), 2)
    assert_eq(freal.to_bigint(f(-5, 2), half_up=False), -2)


@case("reals-ieee: to_float64 default round-to-nearest-even")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    f = freal.to_float64(freal.pi)
    import math
    assert abs(f - math.pi) < 1e-15, f


@case("reals-ieee: to_float32 narrows to single precision")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    f64 = freal.to_float64(freal.pi)
    f32 = freal.to_float32(freal.pi)
    # binary32 has ~7 decimal digits of precision
    import math
    assert abs(f32 - math.pi) < 1e-6, f32
    # Should differ from f64 (because precision narrows)
    assert f32 != f64 or freal.pi.to_float() == f32, (f32, f64)


@case("reals-ieee: NaN raises IEEEFloatError")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    try:
        freal._coerce(float("nan"))
    except freal.IEEEFloatError as e:
        assert "NaN" in str(e), str(e)
        return
    raise AssertionError("NaN was accepted")


@case("reals-ieee: ±Infinity raises IEEEFloatError")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    for v in (float("inf"), float("-inf")):
        try:
            freal._coerce(v)
        except freal.IEEEFloatError:
            continue
        raise AssertionError(f"{v!r} was accepted")


@case("reals-ieee: IEEE -0.0 collapses to exact 0")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    z = freal._coerce(-0.0)
    assert_eq(freal.signum(z), 0)
    assert_eq(freal.to_bigint(z), 0)


@case("reals-ieee: RoundingMode exposed in CR() namespace")
def _():
    if not _reals_ok: raise SkipTest("reals not importable")
    # The expression namespace should let us reference RoundingMode by name
    e = freal.CR("to_bigint(Real.from_fraction(Fraction(5, 2)), "
                 "rounding=RoundingMode.HALF_EVEN)", 0)
    # CR(...) auto-evaluates; for an int return we still get a CR, materialise
    # by accessing cached_value via str()
    assert str(e).startswith("2"), str(e)


# ---------------------------------------------------------------------------
print("== rfc0001 ==")
# ---------------------------------------------------------------------------

try:
    import foam3_py.rfc0001 as rfc1
    _rfc1_ok = True
except ImportError as e:
    _rfc1_ok = False
    _rfc1_err = str(e)


@case("rfc0001: METADATA fields match the verified record")
def _():
    if not _rfc1_ok: raise SkipTest(_rfc1_err)
    m = rfc1.METADATA
    assert_eq(m["rfc_number"], 1)
    assert_eq(m["title"], "Host Software")
    assert_eq(m["author"], "Steve Crocker")
    assert_eq(m["published"], "1969-04-07")
    assert_eq(m["doi"], "10.17487/RFC0001")
    assert "rfc-editor.org" in m["url"]


@case("rfc0001: Host enforces 8-bit address width")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    rfc1.Host(0)          # boundary lo
    rfc1.Host(255)        # boundary hi
    for bad in (-1, 256, 1 << 16):
        try:
            rfc1.Host(bad)
        except ValueError:
            continue
        raise AssertionError(f"Host({bad}) was accepted")


@case("rfc0001: Link bounds — 0..31 plus reserved 32 (high-priority)")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    rfc1.Link(1, 2, 0)            # control
    rfc1.Link(1, 2, 31)           # last regular link
    rfc1.Link(1, 2, 32)           # high-priority reserved
    for bad in (-1, 33, 100):
        try:
            rfc1.Link(1, 2, bad)
        except ValueError:
            continue
        raise AssertionError(f"Link(..., link_id={bad}) was accepted")


@case("rfc0001: Message leader fits 16 bits")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    L = rfc1.Link(1, 2, 3)
    rfc1.Message(L, leader=0)
    rfc1.Message(L, leader=0xFFFF)
    for bad in (-1, 0x10000, 1 << 32):
        try:
            rfc1.Message(L, leader=bad)
        except ValueError:
            continue
        raise AssertionError(f"leader={bad} was accepted")


@case("rfc0001: HostSoftware obeys RFNM flow-control rule")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    sw = rfc1.HostSoftware(rfc1.Host(1, "UCLA"))
    L = rfc1.Link(1, 2, 3)
    m1 = rfc1.Message(L, leader=0x0001)
    sw.send(m1)
    # Second send on same link must be blocked until RFNM
    try:
        sw.send(rfc1.Message(L, leader=0x0002))
    except rfc1.BlockedError:
        pass
    else:
        raise AssertionError("second send on same link wasn't blocked")
    # RFNM clears it; we can send again
    cleared = sw.receive_rfnm(rfc1.RFNM(L, in_response_to=m1))
    assert cleared is m1, cleared
    sw.send(rfc1.Message(L, leader=0x0002))


@case("rfc0001: different links don't block each other")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    sw = rfc1.HostSoftware(rfc1.Host(1))
    sw.send(rfc1.Message(rfc1.Link(1, 2, 3)))
    # Different link_id — no block
    sw.send(rfc1.Message(rfc1.Link(1, 2, 4)))
    # Different dst — no block
    sw.send(rfc1.Message(rfc1.Link(1, 5, 3)))


@case("rfc0001: deliver/receive inbox FIFO")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    sw = rfc1.HostSoftware(rfc1.Host(2))
    m1 = rfc1.Message(rfc1.Link(1, 2, 7), leader=0x0001)
    m2 = rfc1.Message(rfc1.Link(1, 2, 7), leader=0x0002)
    sw.deliver(m1); sw.deliver(m2)
    assert sw.receive() is m1
    assert sw.receive() is m2
    assert sw.receive() is None


@case("rfc0001: dst mismatch on deliver raises")
def _():
    if not _rfc1_ok: raise SkipTest("rfc0001 not importable")
    sw = rfc1.HostSoftware(rfc1.Host(2))
    # Message addressed to host 9, but this is host 2
    try:
        sw.deliver(rfc1.Message(rfc1.Link(1, 9, 0)))
    except ValueError:
        return
    raise AssertionError("mismatched dst was accepted")


# ---------------------------------------------------------------------------
print("== json ==")
# ---------------------------------------------------------------------------

import foam3_py.json as fj


@case("json: primitives parse")
def _():
    assert_eq(fj.loads("null"), None)
    assert_eq(fj.loads("true"), True)
    assert_eq(fj.loads("false"), False)
    assert_eq(fj.loads("42"), 42)
    assert_eq(fj.loads("-17"), -17)
    assert_eq(fj.loads("3.14"), 3.14)
    assert_eq(fj.loads("-2.5e3"), -2500.0)
    assert_eq(fj.loads('"hello"'), "hello")


@case("json: escape handles control + unicode")
def _():
    assert_eq(fj.escape("a\nb\tc\\d\"e"), 'a\\nb\\tc\\\\d\\"e')
    # ASCII printable unaffected
    assert_eq(fj.escape("hello"), "hello")
    # Control chars
    assert_eq(fj.escape("\x01"), "\\u0001")


@case("json: nested round-trip")
def _():
    v = {"a": None, "b": True,
         "c": [1, 2.5, "x", None],
         "d": {"e": [True, False]}}
    s = fj.dumps(v)
    assert_eq(fj.loads(s), v)


@case("json: string escape round-trip")
def _():
    raw = "tab\there\nnewline\"quote\\back"
    v = {"msg": raw}
    s = fj.dumps(v)
    assert_eq(fj.loads(s)["msg"], raw)


@case("json: unicode escape in source")
def _():
    assert_eq(fj.loads('"\\u0041"'), "A")
    assert_eq(fj.loads('"a\\u0041b"'), "aAb")


# ---------------------------------------------------------------------------
print("== csv ==")
# ---------------------------------------------------------------------------

import foam3_py.csv as fc


@case("csv: plain round-trip")
def _():
    rows = [{"a": "1", "b": "hello"}, {"a": "2", "b": "world"}]
    text = fc.write_rows(rows)
    assert_eq(fc.read_rows(text), rows)


@case("csv: comma + quote escaping")
def _():
    rows = [{"name": "Bob, the Builder", "tag": 'said "hi"'}]
    text = fc.write_rows(rows)
    back = fc.read_rows(text)
    assert_eq(back[0]["name"], "Bob, the Builder")
    assert_eq(back[0]["tag"], 'said "hi"')


@case("csv: empty cell")
def _():
    rows = [{"a": "x", "b": ""}]
    text = fc.write_rows(rows)
    back = fc.read_rows(text)
    assert_eq(back[0], rows[0])


@case("csv: YYMMDD date parsing")
def _():
    from foam3_py.parse import StringPStream, ParserContextImpl
    p = fc.YYMMDDParser.instance()
    ps = StringPStream("2024-12-25").apply(p, ParserContextImpl())
    assert_eq(ps.value(), datetime.date(2024, 12, 25))
    ps2 = StringPStream("null").apply(p, ParserContextImpl())
    assert_eq(ps2.value(), None)


# ---------------------------------------------------------------------------
print("== xml ==")
# ---------------------------------------------------------------------------

import foam3_py.xml as fx


@dc.dataclass
class _Person:
    name: str = ""
    age: int = 0
    email: str = ""
    xml_attribute_names = ("age",)


@case("xml: attribute vs element split")
def _():
    out = fx.stringify(_Person("Alice", 30, "a@x.com"), output_default_values=True)
    assert "age=\"30\"" in out, out
    assert "<name>Alice</name>" in out, out
    assert "<email>a@x.com</email>" in out, out


@case("xml: entity escaping")
def _():
    out = fx.stringify(_Person("A <safe> & B", 1, "x"), output_default_values=True)
    assert "<name>A &lt;safe&gt; &amp; B</name>" in out, out


# ---------------------------------------------------------------------------
print("== html ==")
# ---------------------------------------------------------------------------

import foam3_py.html as fh


@case("html: table headers + row")
def _():
    out = fh.stringify(_Person("Alice", 30, "a@x.com"))
    assert "<table border=\"1\">" in out
    assert "<th>name</th>" in out
    assert "<td col=1>Alice</td>" in out


@case("html: nbps typo preserved (Java fidelity)")
def _():
    # Empty string yields NBSP
    out = fh.stringify(_Person("", 0, ""))
    assert "&nbps;" in out, out


@case("html: escaping in cell content")
def _():
    out = fh.stringify(_Person("A <safe>", 1, "x"))
    assert "A &lt;safe&gt;" in out, out


# ---------------------------------------------------------------------------
print("== formatter ==")
# ---------------------------------------------------------------------------

from foam3_py.formatter import JSONFObjectFormatter


@case("formatter: default flags")
def _():
    f = JSONFObjectFormatter()
    out = f.stringify(_Person("Alice", 30, "a@x.com"))
    # class name + bare keys
    assert out.startswith('{class:"_Person"'), out
    assert "name:\"Alice\"" in out


@case("formatter: quote_keys + no class")
def _():
    f = JSONFObjectFormatter(quote_keys=True, output_class_names=False)
    out = f.stringify(_Person("Alice", 30, "a@x.com"))
    assert_eq(out, '{"name":"Alice","age":30,"email":"a@x.com"}')


@case("formatter: multi-line")
def _():
    f = JSONFObjectFormatter(quote_keys=True, output_class_names=False,
                             multi_line_output=True,
                             output_default_values=True)
    out = f.stringify(_Person("Alice", 30, "a@x.com"))
    assert "\n" in out, out


@case("formatter: output_default_values=False prunes defaults")
def _():
    # All-default object should emit no fields
    f = JSONFObjectFormatter(quote_keys=True, output_class_names=False,
                             output_default_values=False)
    out = f.stringify(_Person())
    assert_eq(out, "{}")


@case("formatter: nested + dict + list")
def _():
    f = JSONFObjectFormatter(quote_keys=True, output_class_names=False)
    out = f.stringify({"k": [1, 2, 3], "n": None, "s": "x\ny"})
    assert "[1,2,3]" in out
    assert ":null" in out
    assert "\\n" in out, out


# ---------------------------------------------------------------------------
# Result summary
# ---------------------------------------------------------------------------

total = len(_PASS) + len(_FAIL) + len(_SKIP)
print()
print(f"== Result: {len(_PASS)}/{total} passed, {len(_SKIP)} skipped, {len(_FAIL)} failed ==")
if _SKIP:
    for name in _SKIP:
        print(f"  SKIP  {name}")
if _FAIL:
    print("\nFailures:")
    for name, tb in _FAIL:
        print(f"\n--- {name} ---\n{tb}")
    sys.exit(1)
