#!/usr/bin/env python3
"""
jello_ccs_probe.py -- Combinator Chain Sequence (CCS) probe & trace tool.

A self-contained CLI for reproducing the BBBB investigation on any Jello chain.
The BBBB investigation studies why certain chain expressions resolve to the
combinator sequence "BBBB" (and friends) under both monadic and dyadic
interpretations, what arity structure produces them, and how the per-level
combinator tree is constructed by `draw.combinator_tree`.

This script:
  - tokenizes a chain expression (using the Jello token tables),
  - computes the arity vector and the chain_arity_to_string,
  - runs `draw.combinator_chain_sequence` for both Chain.MONADIC and
    Chain.DYADIC, dumping the resulting CCS strings,
  - optionally monkey-patches `grid.Grid.add_subtree` to instrument a full
    level/start/end/label trace of the combinator tree,
  - optionally runs the canonical P1-P7 probe suite or compares two chains
    side-by-side.

Brief: C:/Users/nicho/Documents/Unreal Projects/Starcel9/Content/Scripts/nd_table/jello/bbbb_research_brief.html
Part of the Starcel9 nd_table/jello investigation; see Documentation/jello_ccs_analysis.html.
"""

# -- stdout/stderr utf-8 reconfigure (Windows defaults to cp1252) ---------
import sys
import io

def _force_utf8(stream_name: str):
    stream = getattr(sys, stream_name, None)
    if stream is None:
        return
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        try:
            reconfigure(encoding="utf-8")
            return
        except Exception:
            pass
    # Fallback: wrap the underlying buffer in a TextIOWrapper.
    buf = getattr(stream, "buffer", None)
    if buf is not None:
        try:
            setattr(sys, stream_name, io.TextIOWrapper(buf, encoding="utf-8", line_buffering=True))
        except Exception:
            pass

_force_utf8("stdout")
_force_utf8("stderr")

# -- path setup -----------------------------------------------------------
import os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_JELLO_SRC = os.path.join(_THIS_DIR, "nd_table", "jello", "src")
if _JELLO_SRC not in sys.path:
    sys.path.insert(0, _JELLO_SRC)

# -- jello imports (must come AFTER sys.path patch) -----------------------
import argparse
import json
import re

import tokens          # noqa: E402  jello token tables
import draw            # noqa: E402  jello combinator drawer
import grid            # noqa: E402  jello grid module (we monkey-patch this)
from utils import Chain, Quick, Separator  # noqa: E402


# -- ANSI colors ----------------------------------------------------------
class _C:
    RESET   = "\x1b[0m"
    BOLD    = "\x1b[1m"
    DIM     = "\x1b[2m"
    RED     = "\x1b[31m"
    GREEN   = "\x1b[32m"
    YELLOW  = "\x1b[33m"
    BLUE    = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN    = "\x1b[36m"

    @classmethod
    def disable(cls):
        for name in ("RESET", "BOLD", "DIM", "RED", "GREEN",
                     "YELLOW", "BLUE", "MAGENTA", "CYAN"):
            setattr(cls, name, "")


# -- canonical BBBB-investigation probe suite -----------------------------
# The 7 canonical P1-P7 chains from brief Section 9. Each chain is paired
# with a one-line `falsifies` note describing what its CCS outcome shows
# about the BBBB structure. See bbbb_research_brief.html for full context.
CANONICAL_PROBES = [
    {
        "id": "P1",
        "chain": "< prior : + * r . scan maxr add1",
        "falsifies": "Base case (no leading monads). Establishes that the post-separator structure alone yields BB.",
    },
    {
        "id": "P2",
        "chain": "iota flat < prior : + * r . scan maxr add1",
        "falsifies": "The expression of interest. +2 leading monads = +2 Bs.",
    },
    {
        "id": "P3",
        "chain": "flat < prior : + * r . scan maxr add1",
        "falsifies": "-1 leading monad = -1 B. Confirms linearity.",
    },
    {
        "id": "P4",
        "chain": "iota flat < prior : + * r . scan add1",
        "falsifies": "Drop maxr. CCS unchanged => 'maxr add1 contributes 2 Bs' is false.",
    },
    {
        "id": "P5",
        "chain": "iota flat < prior : + * r . scan add1 add1",
        "falsifies": "Swap maxr->add1. CCS unchanged => B#4 is structural, not token-identity.",
    },
    {
        "id": "P6",
        "chain": "iota flat < prior : + * r . scan",
        "falsifies": "Drop the .-subchain's tail entirely => -1 B. Some monadic terminator is required for B#4.",
    },
    {
        "id": "P7",
        "chain": "rev iota flat < prior : + * r . scan maxr add1",
        "falsifies": "+1 leading monad = +1 B. Extends linearity beyond two leading monads.",
    },
]


# -- token classification (mirrors jello.py logic) ------------------------
def _is_nilad_array(s: str) -> bool:
    return len(s) > 0 and set(s).issubset(set("-0123456789,[]"))


def keyword_arity(k: str):
    """Return the arity tag for a keyword (int or Quick/Separator enum)."""
    if k in tokens.niladic:   return 0
    if k in tokens.monadic:   return 1
    if k in tokens.dyadic:    return 2
    if k == "each":           return Quick.EACH
    if k == "c":              return Quick.FLIP
    if k in tokens.quick:     return Quick.QUICK
    if k == ".":              return Separator.MONADIC
    if k == ":":              return Separator.DYADIC
    if _is_nilad_array(k):    return 0
    raise ValueError(f"unknown token: {k!r}")


def to_jelly(token: str) -> str:
    if token in tokens.monadic:    return tokens.monadic[token]
    if token in tokens.dyadic:     return tokens.dyadic[token]
    if token in tokens.niladic:    return tokens.niladic[token]
    if token in tokens.quick:      return tokens.quick[token]
    if token in tokens.separators: return tokens.separators[token]
    if _is_nilad_array(token):     return token
    raise ValueError(f"{token!r} is not a valid Jello keyword.")


def arity_chain_repr(i) -> str:
    if i in (Quick.QUICK, Quick.EACH, Quick.FLIP):  return "q"
    if i in (Separator.MONADIC, Separator.DYADIC):  return "s"
    return str(i)


def chain_arity_to_string(chain_arity) -> str:
    return "-".join(arity_chain_repr(e) for e in chain_arity)


# -- tokenization ---------------------------------------------------------
def tokenize(expr: str):
    """Split a chain expression into tokens, stripping () groupers."""
    # Same regex split style as jello.py: keep delimiters, drop empty/space.
    parts = re.split(r"([ ()])", expr.strip())
    return [p for p in parts if p not in ("", " ", "(", ")")]


# -- trace instrumentation ------------------------------------------------
def _make_traced_add_subtree(original, sink: list):
    def traced(self, level, start, end, s):
        sink.append({"level": level, "start": start, "end": end, "label": s})
        return original(self, level, start, end, s)
    return traced


def compute_ccs(chain_arity, chain_type, trace: bool):
    """Return (ccs_string, trace_list). If trace is False, trace_list is []."""
    sink = []
    original = grid.Grid.add_subtree
    try:
        if trace:
            grid.Grid.add_subtree = _make_traced_add_subtree(original, sink)
        ccs = draw.combinator_chain_sequence(list(chain_arity), chain_type)
    finally:
        grid.Grid.add_subtree = original
    return ccs, sink


# -- analysis core --------------------------------------------------------
def analyze(expr: str, trace: bool = False) -> dict:
    """Run the full analysis for a single chain expression."""
    toks = tokenize(expr)
    arity = [keyword_arity(t) for t in toks]
    atoms = "".join(to_jelly(t) for t in toks)
    arity_str = chain_arity_to_string(arity)

    m_ccs, m_trace = compute_ccs(arity, Chain.MONADIC, trace)
    d_ccs, d_trace = compute_ccs(arity, Chain.DYADIC,  trace)

    return {
        "expression":   expr,
        "tokens":       toks,
        "arity_string": arity_str,
        "atoms":        atoms,
        "monadic_ccs":  m_ccs,
        "dyadic_ccs":   d_ccs,
        "monadic_trace": m_trace,
        "dyadic_trace":  d_trace,
    }


def analyze_probe(probe: dict, trace: bool = False) -> dict:
    """Run analyze() on a canonical probe dict and merge id/falsifies fields."""
    result = analyze(probe["chain"], trace=trace)
    result["id"]        = probe["id"]
    result["falsifies"] = probe["falsifies"]
    return result


# -- pretty printing ------------------------------------------------------
def _fmt_label(label: str, key: str) -> str:
    return f"{_C.BOLD}{label:<14}{_C.RESET}{key}"


def print_single(result: dict, trace: bool):
    print()
    print(_fmt_label("Expression:",  result["expression"]))
    print(_fmt_label("Tokens:",      " ".join(result["tokens"])))
    print(_fmt_label("Arity:",       f"{_C.RED}{result['arity_string']}{_C.RESET}"))
    print(_fmt_label("Atoms:",       f"{_C.YELLOW}{result['atoms']}{_C.RESET}"))
    print(_fmt_label("Monadic CCS:", f"{_C.GREEN}{result['monadic_ccs']}{_C.RESET}"))
    print(_fmt_label("Dyadic CCS:",  f"{_C.BLUE}{result['dyadic_ccs']}{_C.RESET}"))

    if trace:
        for kind, key in (("Monadic", "monadic_trace"),
                          ("Dyadic",  "dyadic_trace")):
            print()
            print(f"{_C.BOLD}{kind} trace ({len(result[key])} entries){_C.RESET}")
            print(f"  {'idx':>3}  {'level':>5}  {'start':>5}  {'end':>5}  label")
            print(f"  {'-'*3}  {'-'*5}  {'-'*5}  {'-'*5}  {'-'*8}")
            for i, entry in enumerate(result[key]):
                print(f"  {i:>3}  {entry['level']:>5}  "
                      f"{entry['start']:>5}  {entry['end']:>5}  {entry['label']}")
    print()


def print_probes(results):
    """Render the canonical P1-P7 probe table.

    Each entry in `results` is expected to be the dict returned by
    `analyze_probe(probe_def)`, i.e. an `analyze()` result enriched with
    the canonical 'id' and 'falsifies' keys.
    """
    print()
    print(f"{_C.BOLD}Canonical P1-P7 probe suite{_C.RESET}")
    # Determine column widths.
    id_w     = max(max(len(r["id"]) for r in results), len("ID"))
    chain_w  = max(max(len(r["expression"]) for r in results), len("Chain"))
    arity_w  = max(max(len(r["arity_string"]) for r in results), len("Arity"))
    m_w      = max(max(len(r["monadic_ccs"]) for r in results), len("mCCS"))
    d_w      = max(max(len(r["dyadic_ccs"])  for r in results), len("dCCS"))
    fals_w   = max(max(len(r["falsifies"]) for r in results), len("Falsifies"))

    header = (f"  {'ID':<{id_w}}  {'Chain':<{chain_w}}  "
              f"{'Arity':<{arity_w}}  {'mCCS':<{m_w}}  "
              f"{'dCCS':<{d_w}}  {'Falsifies':<{fals_w}}")
    sep = (f"  {'-'*id_w}  {'-'*chain_w}  {'-'*arity_w}  "
           f"{'-'*m_w}  {'-'*d_w}  {'-'*fals_w}")
    print(header)
    print(sep)
    for r in results:
        print(f"  {_C.BOLD}{r['id']:<{id_w}}{_C.RESET}  "
              f"{r['expression']:<{chain_w}}  "
              f"{_C.RED}{r['arity_string']:<{arity_w}}{_C.RESET}  "
              f"{_C.GREEN}{r['monadic_ccs']:<{m_w}}{_C.RESET}  "
              f"{_C.BLUE}{r['dyadic_ccs']:<{d_w}}{_C.RESET}  "
              f"{_C.DIM}{r['falsifies']:<{fals_w}}{_C.RESET}")
    print()


def print_compare(a: dict, b: dict):
    print()
    print(f"{_C.BOLD}Side-by-side comparison{_C.RESET}")
    rows = [
        ("expression",   a["expression"],   b["expression"]),
        ("arity",        a["arity_string"], b["arity_string"]),
        ("atoms",        a["atoms"],        b["atoms"]),
        ("monadic CCS",  a["monadic_ccs"],  b["monadic_ccs"]),
        ("dyadic CCS",   a["dyadic_ccs"],   b["dyadic_ccs"]),
    ]
    label_w = max(len(r[0]) for r in rows)
    left_w  = max(len(r[1]) for r in rows)
    right_w = max(len(r[2]) for r in rows)
    header = f"  {'field':<{label_w}}  {'A':<{left_w}}  {'B':<{right_w}}"
    print(header)
    print(f"  {'-'*label_w}  {'-'*left_w}  {'-'*right_w}")
    for label, va, vb in rows:
        marker = "  " if va == vb else f"{_C.MAGENTA}!={_C.RESET}"
        print(f"  {label:<{label_w}}  {va:<{left_w}}  {vb:<{right_w}}  {marker}")
    print()


# -- main / CLI -----------------------------------------------------------
def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="jello_ccs_probe",
        description=("Probe Jello combinator chain sequences (CCS). "
                     "Self-contained reproduction harness for the BBBB investigation."),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  jello_ccs_probe 'iota flat < prior : + * r . scan maxr add1' --trace\n"
            "  jello_ccs_probe --probes\n"
            "  jello_ccs_probe --compare 'iota flat <' 'iota flat'\n"
        ),
    )
    p.add_argument("chain", nargs="?",
                   help="chain expression as a single string "
                        "(optional if --probes or --compare is used)")
    p.add_argument("--trace", "-t", action="store_true",
                   help="dump the full instrumented combinator trace")
    p.add_argument("--probes", "-p", action="store_true",
                   help="run the canonical P1-P7 probe suite (no chain arg needed)")
    p.add_argument("--compare", nargs=2, metavar=("A", "B"),
                   help="run two chains side-by-side")
    p.add_argument("--json", action="store_true",
                   help="machine-readable output (default is pretty text)")
    p.add_argument("--no-color", action="store_true",
                   help="disable ANSI colors")
    return p


def _serialize_trace_entry(e: dict) -> dict:
    # Already plain ints/strings; this is defensive.
    return {
        "level": int(e["level"]),
        "start": int(e["start"]),
        "end":   int(e["end"]),
        "label": str(e["label"]),
    }


def _serialize_result(r: dict) -> dict:
    return {
        "expression":    r["expression"],
        "tokens":        r["tokens"],
        "arity_string":  r["arity_string"],
        "atoms":         r["atoms"],
        "monadic_ccs":   r["monadic_ccs"],
        "dyadic_ccs":    r["dyadic_ccs"],
        "monadic_trace": [_serialize_trace_entry(e) for e in r["monadic_trace"]],
        "dyadic_trace":  [_serialize_trace_entry(e) for e in r["dyadic_trace"]],
    }


def main(argv=None) -> int:
    args = build_argparser().parse_args(argv)

    if args.no_color or not sys.stdout.isatty():
        _C.disable()

    if not (args.chain or args.probes or args.compare):
        build_argparser().print_help()
        return 2

    # --compare A B
    if args.compare:
        a = analyze(args.compare[0], trace=args.trace)
        b = analyze(args.compare[1], trace=args.trace)
        if args.json:
            print(json.dumps({"mode": "compare",
                              "a": _serialize_result(a),
                              "b": _serialize_result(b)}, indent=2))
        else:
            print_compare(a, b)
            if args.trace:
                print_single(a, trace=True)
                print_single(b, trace=True)
        return 0

    # --probes (canonical P1-P7 suite)
    if args.probes:
        results = [analyze_probe(p, trace=args.trace) for p in CANONICAL_PROBES]
        if args.json:
            payload = [
                {
                    "id":          r["id"],
                    "chain":       r["expression"],
                    "arity":       r["arity_string"],
                    "monadic_ccs": r["monadic_ccs"],
                    "dyadic_ccs":  r["dyadic_ccs"],
                    "falsifies":   r["falsifies"],
                }
                for r in results
            ]
            print(json.dumps(payload, indent=2))
        else:
            print_probes(results)
            if args.trace:
                for r in results:
                    print_single(r, trace=True)
        return 0

    # Single chain
    result = analyze(args.chain, trace=args.trace)
    if args.json:
        print(json.dumps({"mode": "single",
                          "result": _serialize_result(result)}, indent=2))
    else:
        print_single(result, trace=args.trace)
    return 0


if __name__ == "__main__":
    sys.exit(main())
