"""Smoke tests for jello_integration.

Run from the parent of nd_table/:

    PYTHONIOENCODING=utf-8 python -m nd_table.test_jello_integration

or directly:

    python test_jello_integration.py
"""
from __future__ import annotations

import sys
import traceback
from typing import Callable, List, Tuple

import jello_integration as ji
from ndtable import Table, Axis


_PASS: List[str] = []
_FAIL: List[Tuple[str, str]] = []


def case(name: str):
    def deco(fn: Callable[[], None]) -> Callable[[], None]:
        try:
            fn()
            _PASS.append(name)
            print(f"  PASS  {name}")
        except Exception as e:  # noqa: BLE001
            _FAIL.append((name, traceback.format_exc()))
            print(f"  FAIL  {name}: {e}")
        return fn
    return deco


def assert_eq(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg}\n  expected: {expected!r}\n  actual:   {actual!r}")


print("== translation ==")


@case("counts add up to ~155")
def _():
    total = len(ji.all_keywords())
    assert total >= 150, total


@case("single atom: abs -> A")
def _():
    assert_eq(ji.translate("abs"), "A")


@case("chained atoms: abs neg -> AN")
def _():
    assert_eq(ji.translate("abs neg"), "AN")


@case("dyadic chain: + * pow")
def _():
    # + -> +,  * -> ×,  pow -> *
    assert_eq(ji.translate("+ * pow"), "+×*")  # ×


@case("quick: fold +")
def _():
    assert_eq(ji.translate("fold +"), "/+")


@case("grouping parens are preserved")
def _():
    assert_eq(ji.translate("( abs neg ) each"), "(AN)€")  # €


@case("nilad array literal passes through")
def _():
    assert ji.is_nilad_array("[1,2,3]")
    assert_eq(ji.translate("[1,2,3]"), "[1,2,3]")


@case("unknown keyword raises KeyError")
def _():
    try:
        ji.translate("not_a_real_keyword")
    except KeyError:
        return
    raise AssertionError("expected KeyError")


@case("arity classification")
def _():
    assert_eq(ji.keyword_arity("abs"), 1)
    assert_eq(ji.keyword_arity("+"), 2)
    assert_eq(ji.keyword_arity("fold"), -3)
    assert_eq(ji.keyword_arity("each"), -10)
    assert_eq(ji.keyword_arity("."), -20)
    assert_eq(ji.keyword_arity("[1,2]"), 0)


print("== execution / fallback ==")


@case("is_jelly_available returns bool")
def _():
    assert isinstance(ji.is_jelly_available(), bool)


@case("translation_only mode never shells out")
def _():
    f = ji.JelloFormula(translation_only=True)
    r = f("abs neg", 5)
    assert isinstance(r, dict), r
    assert_eq(r["atoms"], "AN")
    assert_eq(r["args"], [5])
    assert r["executed"] is False


@case("run_jelly raises clean error when jelly missing")
def _():
    if ji.is_jelly_available():
        return  # skip on machines that do have jelly
    try:
        ji.run_jelly("A", -5)
    except RuntimeError as e:
        assert "jelly executable" in str(e).lower(), str(e)
        return
    raise AssertionError("expected RuntimeError")


print("== nd_table wiring ==")


@case("install_into_table adds JELLY to formula context")
def _():
    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    ji.install_into_table(t, translation_only=True)
    ctx = t._get_formula_context()
    for n in ("JELLY", "jello", "jelly"):
        assert n in ctx, list(ctx.keys())[:30]


@case("cell formula =JELLY(\"abs neg\", A1) evaluates")
def _():
    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    ji.install_into_table(t, translation_only=True)
    t[0, 0] = 7
    t[0, 1] = '=JELLY("abs neg", A1)'
    r = t[0, 1]
    assert isinstance(r, dict), r
    assert_eq(r["atoms"], "AN")
    # The A1 reference got substituted to 7
    assert r["args"] == [7] or r["args"] == ["7"], r["args"]


@case("install_into_table is idempotent")
def _():
    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    ji.install_into_table(t, translation_only=True)
    ji.install_into_table(t, translation_only=True)
    ctx = t._get_formula_context()
    assert "JELLY" in ctx


@case("formula context still has math / max / np")
def _():
    t = Table(axes=[Axis(0, 2, name="r"), Axis(0, 2, name="c")])
    ji.install_into_table(t, translation_only=True)
    ctx = t._get_formula_context()
    for n in ("math", "max", "min", "sum", "abs", "np"):
        assert n in ctx, f"{n} missing"


# ---------------------------------------------------------------------------
total = len(_PASS) + len(_FAIL)
print()
print(f"== Result: {len(_PASS)}/{total} passed ==")
if _FAIL:
    print()
    for name, tb in _FAIL:
        print(f"--- {name} ---")
        print(tb)
    sys.exit(1)
