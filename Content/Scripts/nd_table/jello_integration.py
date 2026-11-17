"""
Integration of codereport/jello (https://github.com/codereport/jello) with
the nD Table.

Jello is a CLI wrapper around the Jelly programming language (more
specifically Jellyfish, a fork of Jelly). It maps human-readable keywords
("abs", "head", "rev", "fold", ...) to Jelly's Unicode atoms ("A", "Ḣ", "Ṛ",
"/", ...) and pipes the result through the ``jelly`` executable.

This module exposes jello's keyword translation as a pure-Python API (no
external binary required) and gracefully wraps the ``jelly`` executable
when it is installed. It then plugs into the nD Table formula engine as
the ``JELLY(...)`` function so cells can write golfing-language chains
against their neighbours.

API:
    translate(keyword_expr)       keyword string → Jelly atom string
    keyword_arity(kw)             arity of a keyword (0/1/2 or Quick/Separator)
    is_jelly_available()          True iff the jelly executable is on PATH
    run_jelly(atom_expr, *args)   subprocess call to jelly; raises if missing
    evaluate(keyword_expr, *args) translate + run, returns result as a string
    JelloFormula                  callable wrapper usable inside nd_table cells
    install_into_table(table)     register a JELLY()/jello() formula function

nD Table cell example::

    from nd_table import Table, Axis
    from jello_integration import install_into_table

    t = Table(axes=[Axis(0, 4, name="rows"), Axis(0, 4, name="cols")])
    install_into_table(t)
    t[0, 0] = 5
    t[0, 1] = '=JELLY("abs neg", A1)'   # if jelly is on PATH, evaluates "abs neg" on 5
"""

from __future__ import annotations

import importlib
import os
import re
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Bootstrap: make jello's modules importable WITHOUT modifying the vendored
# source tree. jello uses bare imports (``import tokens``) so we add
# jello/src to sys.path and pull out the two pure-stdlib modules we need.
# ---------------------------------------------------------------------------

_HERE = os.path.dirname(os.path.abspath(__file__))
_JELLO_SRC = os.path.join(_HERE, "jello", "src")

_tokens = None
_utils = None
_import_error: Optional[BaseException] = None


def _ensure_jello_loaded() -> None:
    """Lazy-import jello's tokens + utils. Idempotent. Raises ImportError on
    first failure; subsequent calls re-raise the cached error so callers
    don't pay the import cost twice."""
    global _tokens, _utils, _import_error
    if _tokens is not None and _utils is not None:
        return
    if _import_error is not None:
        raise _import_error
    if not os.path.isdir(_JELLO_SRC):
        _import_error = ImportError(
            f"jello source not found at {_JELLO_SRC}. "
            "Clone codereport/jello into nd_table/jello/ first."
        )
        raise _import_error
    if _JELLO_SRC not in sys.path:
        sys.path.insert(0, _JELLO_SRC)
    try:
        _tokens = importlib.import_module("tokens")
        _utils = importlib.import_module("utils")
    except Exception as e:  # pragma: no cover - rare path
        _import_error = e
        raise


# ---------------------------------------------------------------------------
# Public lookup
# ---------------------------------------------------------------------------

def monadic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded()
    return dict(_tokens.monadic)


def dyadic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded()
    return dict(_tokens.dyadic)


def niladic_atoms() -> Dict[str, str]:
    _ensure_jello_loaded()
    return dict(_tokens.niladic)


def quick_atoms() -> Dict[str, str]:
    _ensure_jello_loaded()
    return dict(_tokens.quick)


def separator_atoms() -> Dict[str, str]:
    _ensure_jello_loaded()
    return dict(_tokens.separators)


def all_keywords() -> List[str]:
    """Sorted list of every keyword jello recognises (155+ atoms)."""
    _ensure_jello_loaded()
    return sorted(set(_tokens.monadic) | set(_tokens.dyadic)
                  | set(_tokens.niladic) | set(_tokens.quick)
                  | set(_tokens.separators))


# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------

_NILAD_ARRAY_RE = re.compile(r"^[-0-9,\[\]]+$")


def is_nilad_array(s: str) -> bool:
    """Same as jello.is_nilad_array: a literal array like ``[1,2,3]``."""
    return bool(s) and bool(_NILAD_ARRAY_RE.match(s))


def to_jelly_atom(token: str) -> str:
    """Translate a single keyword (or literal array) to its Jelly atom.
    Raises ``KeyError`` for unknown tokens."""
    _ensure_jello_loaded()
    for table in (_tokens.monadic, _tokens.dyadic, _tokens.niladic,
                  _tokens.quick, _tokens.separators):
        if token in table:
            return table[token]
    if is_nilad_array(token):
        return token
    raise KeyError(f"{token!r} is not a Jello keyword")


def translate(keyword_expr: str) -> str:
    """Translate a whitespace-separated Jello expression to a Jelly atom
    string. ``(`` and ``)`` are passed through unchanged (Jelly groups)."""
    parts = _tokenize(keyword_expr)
    return "".join(to_jelly_atom(p) if p not in ("(", ")") else p
                   for p in parts)


def _tokenize(keyword_expr: str) -> List[str]:
    # Split on whitespace and on the grouping parens; keep the parens as
    # standalone tokens. Mirrors jello.py's split_keep_multiple_delimiters.
    tokens_out: List[str] = []
    for chunk in re.split(r"(\s+|[()])", keyword_expr):
        if chunk and not chunk.isspace():
            tokens_out.append(chunk)
    return tokens_out


def keyword_arity(kw: str) -> int:
    """Return arity for a keyword: 0/1/2 (nilad/monad/dyad), -3 (quick),
    -10 (each), -50 (flip @), -20 (monadic separator µ), -21 (dyadic ð).
    Negative codes match jello.py's Quick/Separator enums."""
    _ensure_jello_loaded()
    if kw in _tokens.niladic:    return 0
    if kw in _tokens.monadic:    return 1
    if kw in _tokens.dyadic:     return 2
    if kw == "each":             return -10
    if kw == "c":                return -50
    if kw in _tokens.quick:      return -3
    if kw == ".":                return -20
    if kw == ":":                return -21
    if is_nilad_array(kw):       return 0
    raise KeyError(f"{kw!r} arity unknown")


# ---------------------------------------------------------------------------
# Execution — wraps the jelly executable
# ---------------------------------------------------------------------------

_JELLY_BIN: Optional[str] = None  # cached result of shutil.which


def jelly_path() -> Optional[str]:
    """Return absolute path to the ``jelly`` executable, or None if missing.
    Cached on first call."""
    global _JELLY_BIN
    if _JELLY_BIN is None:
        _JELLY_BIN = shutil.which("jelly") or ""
    return _JELLY_BIN or None


def is_jelly_available() -> bool:
    return jelly_path() is not None


def run_jelly(atom_expr: str, *args: Any, timeout: float = 30.0) -> str:
    """Pipe ``atom_expr`` (already in Jelly atoms) through the ``jelly``
    executable with the given arguments. Raises ``RuntimeError`` if jelly
    is not installed, ``subprocess.CalledProcessError`` if it exits non-zero.
    """
    binary = jelly_path()
    if binary is None:
        raise RuntimeError(
            "jelly executable not found on PATH. Install Jellyfish or set "
            "$PATH so `jelly --version` works, then call run_jelly() again."
        )
    cmd = [binary, "eun", atom_expr, *[str(a) for a in args]]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          check=True, timeout=timeout)
    return proc.stdout.strip()


def evaluate(keyword_expr: str, *args: Any, timeout: float = 30.0) -> str:
    """Translate a keyword expression and run it. Convenience wrapper."""
    return run_jelly(translate(keyword_expr), *args, timeout=timeout)


# ---------------------------------------------------------------------------
# JelloFormula — callable wrapper used by the nD Table formula evaluator
# ---------------------------------------------------------------------------

class JelloFormula:
    """Callable for use inside ``Table`` formulas.

    Two call styles:

      JelloFormula()("abs neg", 5)              -> str
      JelloFormula(translation_only=True)("abs neg", 5) -> ("A_N", 5)

    ``translation_only`` mode never calls the jelly executable — handy for
    testing or for environments where jelly isn't installed."""

    def __init__(self, *, translation_only: bool = False,
                 timeout: float = 30.0) -> None:
        self.translation_only = translation_only
        self.timeout = timeout

    def __call__(self, expr: str, *args: Any) -> Any:
        atoms = translate(expr)
        if self.translation_only or not is_jelly_available():
            return {"atoms": atoms, "args": list(args),
                    "executed": False,
                    "reason": "jelly not on PATH"
                              if not is_jelly_available() else
                              "translation_only=True"}
        return run_jelly(atoms, *args, timeout=self.timeout)


# ---------------------------------------------------------------------------
# nD Table wiring
# ---------------------------------------------------------------------------

_SIDE_NS: Dict[int, Dict[str, Any]] = {}


def formula_namespace_for(table: Any) -> Dict[str, Any]:
    """Return the per-table extra-formula-context dict, creating one if
    needed. Anything added here becomes visible to cell formula ``eval``
    after ``install_into_table`` (or any other call that wraps
    ``_get_formula_context``)."""
    ns = getattr(table, "_formula_namespace", None)
    if ns is None:
        ns = _SIDE_NS.get(id(table))
    if ns is None:
        ns = {}
        try:
            setattr(table, "_formula_namespace", ns)
        except AttributeError:
            _SIDE_NS[id(table)] = ns
    return ns


def _wrap_formula_context(table: Any) -> None:
    """Monkey-patch ``table._get_formula_context`` (idempotent) so that the
    returned dict is merged with ``formula_namespace_for(table)`` before
    being passed to ``eval``. Without this hook, JELLY would never be
    visible to the formula engine, since ``_get_formula_context`` builds
    its dict from scratch each call."""
    if getattr(table, "_jello_patched", False):
        return
    if not hasattr(table, "_get_formula_context"):
        # Table API mismatch — fail quietly; install_into_table still wrote
        # the namespace, the caller can read it directly.
        setattr(table, "_jello_patched", True)
        return

    original = table._get_formula_context

    def patched(*args, **kwargs):
        ctx = original(*args, **kwargs)
        extra = formula_namespace_for(table)
        if extra:
            ctx.update(extra)
        return ctx

    # Bind as a bound method on this instance only (not the class).
    try:
        table._get_formula_context = patched  # type: ignore[assignment]
    except AttributeError:
        # __slots__ or read-only attr — fall back to a class-level patch.
        cls = type(table)
        if not getattr(cls, "_jello_class_patched", False):
            cls_original = cls._get_formula_context
            def cls_patched(self_, *a, **kw):
                ctx = cls_original(self_, *a, **kw)
                extra = formula_namespace_for(self_)
                if extra:
                    ctx.update(extra)
                return ctx
            cls._get_formula_context = cls_patched  # type: ignore[assignment]
            cls._jello_class_patched = True  # type: ignore[attr-defined]
    setattr(table, "_jello_patched", True)


def install_into_table(table: Any, *, name: str = "JELLY",
                       translation_only: bool = False,
                       timeout: float = 30.0,
                       also: Sequence[str] = ("jello", "jelly")) -> "JelloFormula":
    """Make ``JELLY(expr, *args)`` callable from cell formulas on this
    table. Registers under ``name`` plus every alias in ``also``.

    Implementation:

    * Stash a per-table dict at ``table._formula_namespace`` (or on
      ``_SIDE_NS`` for slotted objects).
    * Wrap ``_get_formula_context`` so its returned dict is merged with
      the per-table namespace before each formula ``eval``.

    The result: cells can write ``=JELLY("abs neg", A1)`` and the lookup
    resolves through the regular formula evaluator with no other code
    changes.
    """
    formula = JelloFormula(translation_only=translation_only, timeout=timeout)
    ns = formula_namespace_for(table)
    for n in (name, *also):
        ns[n] = formula
    _wrap_formula_context(table)
    return formula


# ---------------------------------------------------------------------------
# CLI / smoke test
# ---------------------------------------------------------------------------

def _safe_print(s: str) -> None:
    """Print str robustly on Windows consoles that default to cp1252.
    Falls back to \\uXXXX escapes for characters the active codec can't
    encode."""
    enc = sys.stdout.encoding or "ascii"
    try:
        sys.stdout.write(s + "\n")
    except UnicodeEncodeError:
        sys.stdout.write(s.encode(enc, errors="backslashreplace").decode(enc) + "\n")


def _demo() -> None:
    _safe_print(f"jello source: {_JELLO_SRC}")
    _ensure_jello_loaded()
    _safe_print(f"  monadic:    {len(monadic_atoms())} atoms")
    _safe_print(f"  dyadic:     {len(dyadic_atoms())} atoms")
    _safe_print(f"  niladic:    {len(niladic_atoms())} atoms")
    _safe_print(f"  quick:      {len(quick_atoms())} atoms")
    _safe_print(f"  separators: {len(separator_atoms())} atoms")
    _safe_print(f"  total:      {len(all_keywords())} keywords")
    _safe_print("")

    samples = [
        "abs",
        "abs neg",
        "head rev",
        "+ * pow",
        "fold +",
        "( abs neg ) each",
    ]
    _safe_print("Translation samples:")
    for kw in samples:
        try:
            atoms = translate(kw)
            _safe_print(f"  {kw!r:32} -> {atoms!r}")
        except KeyError as e:
            _safe_print(f"  {kw!r:32} -> ERROR {e}")

    _safe_print("")
    _safe_print(
        f"jelly executable: "
        f"{'YES at ' + jelly_path() if is_jelly_available() else 'NO (translation-only mode)'}"
    )

    if is_jelly_available():
        try:
            out = evaluate("abs", -5)
            _safe_print(f"  evaluate('abs', -5) = {out!r}")
        except Exception as e:
            _safe_print(f"  evaluation error: {e}")


if __name__ == "__main__":
    _demo()
