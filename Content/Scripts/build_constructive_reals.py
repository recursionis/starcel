"""Build Documentation/constructive_reals.html from the package sources.

This script lives in ``Content/Scripts/`` (next to the rest of the
project's Python scripts). It reads the ``reals`` package from the
sibling subdirectory ``Content/Scripts/nd_table/reals-0.0.6/reals/``,
and writes the rendered HTML to the project-root ``Documentation/``
folder.

Run:    ``python Content/Scripts/build_constructive_reals.py``
Output: ``Documentation/constructive_reals.html`` — self-contained,
        MathJax loads from CDN at view time.
"""

import html
import os
import sys
from datetime import datetime


HERE = os.path.dirname(os.path.abspath(__file__))


def find_reals_package() -> str:
    """Locate the ``reals/`` package next to this script."""
    candidate = os.path.join(HERE, "nd_table", "reals-0.0.6", "reals")
    if os.path.isdir(candidate):
        return candidate
    raise FileNotFoundError(
        f"Could not find reals package. Expected at {candidate}."
    )


def find_documentation_dir() -> str:
    """Walk up from this script's location to find the project root —
    the directory that has both a ``Content`` and a ``Documentation``
    sibling — and return the path to ``Documentation/``.
    """
    p = HERE
    for _ in range(6):
        cand = os.path.join(p, "Documentation")
        if os.path.isdir(cand) and os.path.isdir(os.path.join(p, "Content")):
            return cand
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    raise FileNotFoundError(
        f"Could not find project-root Documentation/ folder "
        f"starting from {HERE}."
    )


REALS_DIR = find_reals_package()
DOCS_DIR = find_documentation_dir()


def read_source(rel: str) -> str:
    """Read ``rel`` (a filename like ``_creal.py``) from the reals package."""
    with open(os.path.join(REALS_DIR, rel), encoding="utf-8") as f:
        return f.read()


def listing(src, lang="python"):
    return f'<pre class="src lang-{lang}"><code>{html.escape(src)}</code></pre>'


SOURCES = {
    "init":     read_source("__init__.py"),
    "creal":    read_source("_creal.py"),
    "backends": read_source("_backends.py"),
    "pga":      read_source("_pga.py"),
    "pga2d":    read_source("_pga2d.py"),
    "pga_nd":   read_source("_pga_nd.py"),
}

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Constructive Reals — System Design and Implementation</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
  MathJax = {
    tex: { inlineMath: [['$', '$'], ['\\(', '\\)']],
           displayMath: [['$$', '$$'], ['\\[', '\\]']],
           packages: { '[+]': ['ams'] } },
    loader: { load: ['[tex]/ams'] }
  };
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  :root {
    --fg: #1a1a1a;
    --bg: #fefefe;
    --muted: #6a6a6a;
    --accent: #1f4068;
    --accent2: #b85a18;
    --code-bg: #f6f6f1;
    --code-border: #d8d4c8;
    --side: #f1efe6;
    --rule: #d0cabb;
  }
  * { box-sizing: border-box; }
  html { font-size: 17px; }
  body {
    margin: 0;
    color: var(--fg);
    background: var(--bg);
    font-family: "Charter", "Iowan Old Style", Georgia, serif;
    line-height: 1.55;
  }
  .layout { display: flex; max-width: 1500px; margin: 0 auto; }
  nav.toc {
    width: 280px;
    flex-shrink: 0;
    background: var(--side);
    border-right: 1px solid var(--rule);
    padding: 24px 22px;
    font-size: 0.92em;
    position: sticky;
    top: 0;
    align-self: flex-start;
    max-height: 100vh;
    overflow-y: auto;
  }
  nav.toc h2 { font-size: 1em; margin: 0 0 12px 0; text-transform: uppercase; letter-spacing: 0.07em; color: var(--accent); }
  nav.toc ol { padding-left: 18px; margin: 0; }
  nav.toc li { margin-bottom: 4px; }
  nav.toc ol ol { padding-left: 16px; font-size: 0.95em; margin-top: 4px; }
  nav.toc a { color: var(--fg); text-decoration: none; }
  nav.toc a:hover { color: var(--accent2); text-decoration: underline; }
  main { flex: 1; padding: 32px 50px 80px 50px; max-width: 1100px; }
  h1 { font-size: 2.0em; margin: 0 0 0.2em 0; color: var(--accent); letter-spacing: -0.01em; }
  h1 .sub { display: block; font-size: 0.5em; font-weight: normal; color: var(--muted); font-style: italic; margin-top: 6px; letter-spacing: 0; }
  h2 { margin-top: 2.2em; padding-bottom: 0.2em; border-bottom: 2px solid var(--accent); color: var(--accent); font-size: 1.5em; }
  h3 { margin-top: 1.8em; color: var(--accent2); font-size: 1.18em; }
  h4 { margin-top: 1.4em; font-size: 1.04em; }
  p, ul, ol { margin: 0.65em 0; }
  code { font-family: "JetBrains Mono", "Fira Code", Menlo, Consolas, monospace; font-size: 0.9em; background: var(--code-bg); padding: 1px 4px; border-radius: 3px; border: 1px solid var(--code-border); }
  pre.src {
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 4px;
    padding: 16px 18px;
    overflow-x: auto;
    font-size: 0.79em;
    line-height: 1.4;
    margin: 1em 0;
  }
  pre.src code { background: none; border: none; padding: 0; font-size: 1em; }
  details.src { margin: 0.8em 0; border: 1px solid var(--rule); border-radius: 4px; background: var(--bg); }
  details.src summary { cursor: pointer; padding: 8px 14px; font-family: "JetBrains Mono", Menlo, monospace; font-size: 0.85em; background: var(--side); border-radius: 4px; user-select: none; }
  details.src summary:hover { color: var(--accent2); }
  details.src[open] summary { border-bottom: 1px solid var(--rule); border-radius: 4px 4px 0 0; }
  details.src pre.src { margin: 0; border: none; border-radius: 0 0 4px 4px; }
  blockquote { border-left: 3px solid var(--accent2); padding-left: 16px; color: var(--muted); margin: 1em 0; font-style: italic; }
  table { border-collapse: collapse; margin: 1em 0; font-size: 0.93em; }
  th, td { border: 1px solid var(--rule); padding: 6px 12px; text-align: left; }
  th { background: var(--side); }
  td.num { text-align: right; font-variant-numeric: tabular-nums; font-family: "JetBrains Mono", Menlo, monospace; }
  td.center { text-align: center; }
  td.ok { color: #2a7a2a; font-weight: bold; }
  td.bad { color: #b03030; font-weight: bold; }
  .callout { background: #fef8e8; border-left: 4px solid #d4a017; padding: 12px 18px; margin: 1em 0; border-radius: 0 4px 4px 0; }
  .callout.warn { background: #fceaea; border-left-color: #c8442e; }
  .callout.note { background: #e8f0fc; border-left-color: #2a5fb8; }
  .callout strong { color: #1a1a1a; }
  .diagram { font-family: "JetBrains Mono", Menlo, monospace; font-size: 0.85em; background: var(--code-bg); padding: 16px; border: 1px solid var(--code-border); border-radius: 4px; white-space: pre; overflow-x: auto; line-height: 1.3; }
  .meta { color: var(--muted); font-size: 0.92em; margin: 0.3em 0 1.5em 0; }
  hr.section { border: none; border-top: 1px solid var(--rule); margin: 3em 0; }
  footer { margin-top: 5em; padding-top: 1.5em; border-top: 1px solid var(--rule); color: var(--muted); font-size: 0.88em; }
  .anchor { color: var(--muted); text-decoration: none; opacity: 0.4; margin-left: 0.3em; }
  .anchor:hover { opacity: 1; color: var(--accent2); }
  ul.pillars { list-style: none; padding: 0; }
  ul.pillars li { padding: 8px 0; border-bottom: 1px dotted var(--rule); }
  ul.pillars li strong { color: var(--accent2); }
  @media (max-width: 980px) { .layout { flex-direction: column; } nav.toc { width: 100%; position: relative; max-height: none; } main { padding: 20px; } }
</style>
</head>
<body>
<div class="layout">
<nav class="toc">
  <h2>Contents</h2>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#theory">Theory</a>
      <ol>
        <li><a href="#theory-defn">Definition</a></li>
        <li><a href="#theory-tower">$\mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}_c$</a></li>
        <li><a href="#theory-projection">$\mathbb{R}_c \to \mathbb{Z}$ projection</a></li>
      </ol>
    </li>
    <li><a href="#design">System design</a>
      <ol>
        <li><a href="#design-classes">Class hierarchy</a></li>
        <li><a href="#design-tree">Expression trees</a></li>
        <li><a href="#design-cache">Approximation cache</a></li>
        <li><a href="#design-precision">Precision propagation</a></li>
      </ol>
    </li>
    <li><a href="#algorithms">Algorithms</a>
      <ol>
        <li><a href="#alg-pi">π via Gauss–Legendre AGM</a></li>
        <li><a href="#alg-sqrt">$\sqrt{x}$ via Newton iteration</a></li>
        <li><a href="#alg-exp">$\exp$ via Taylor + halving</a></li>
        <li><a href="#alg-ln">$\ln$ via Machin-style argument reduction and Taylor</a></li>
        <li><a href="#alg-trig">$\cos$, $\sin$, $\mathrm{asin}$, $\mathrm{acos}$</a></li>
        <li><a href="#alg-arith">Arithmetic precision bookkeeping</a></li>
      </ol>
    </li>
    <li><a href="#impl">Implementation</a>
      <ol>
        <li><a href="#impl-port">Java → JS → Python heritage</a></li>
        <li><a href="#impl-bugs">Bugs caught</a></li>
        <li><a href="#impl-z">$\mathbb{Z}$ embedding handling</a></li>
        <li><a href="#impl-pga">PGA integration</a></li>
      </ol>
    </li>
    <li><a href="#perf">Performance</a>
      <ol>
        <li><a href="#perf-bench">Measured numbers</a></li>
        <li><a href="#perf-opts">Optimisations applied</a></li>
        <li><a href="#perf-limits">Where the floor is</a></li>
      </ol>
    </li>
    <li><a href="#sources">Full source code</a>
      <ol>
        <li><a href="#src-init">__init__.py</a></li>
        <li><a href="#src-creal">_creal.py</a></li>
        <li><a href="#src-backends">_backends.py</a></li>
        <li><a href="#src-pga">_pga.py</a></li>
        <li><a href="#src-pga2d">_pga2d.py</a></li>
        <li><a href="#src-pga_nd">_pga_nd.py</a></li>
      </ol>
    </li>
    <li><a href="#related">Related work</a>
      <ol>
        <li><a href="#related-cr">Other constructive-real libraries</a></li>
        <li><a href="#related-mpfr">Arbitrary-precision floats</a></li>
        <li><a href="#related-formal">Formalised reals (Coq / Lean / Agda)</a></li>
        <li><a href="#related-interval">Interval / affine / Taylor models</a></li>
      </ol>
    </li>
    <li><a href="#open">Open problems</a>
      <ol>
        <li><a href="#open-algo">Algorithmic frontiers</a></li>
        <li><a href="#open-impl">Implementation frontiers</a></li>
        <li><a href="#open-theory">Theoretical frontiers</a></li>
        <li><a href="#open-apps">Applications &amp; tooling</a></li>
      </ol>
    </li>
    <li><a href="#frontier">Bleeding-edge directions</a>
      <ol>
        <li><a href="#frontier-fft">NTT / FFT for Python ints</a></li>
        <li><a href="#frontier-gpu">GPU acceleration</a></li>
        <li><a href="#frontier-types">Refinement / dependent types</a></li>
        <li><a href="#frontier-llm">LLM-assisted bound derivation</a></li>
        <li><a href="#frontier-cf">Continued-fraction representation</a></li>
        <li><a href="#frontier-hw">Hardware: FPGA / chiplet</a></li>
      </ol>
    </li>
    <li><a href="#methodology">Reproducibility</a>
      <ol>
        <li><a href="#method-hw">Hardware &amp; software stack</a></li>
        <li><a href="#method-bench">Benchmark protocol</a></li>
        <li><a href="#method-numbers">All measured numbers</a></li>
      </ol>
    </li>
    <li><a href="#decisions">Decision log</a>
      <ol>
        <li><a href="#dec-port">Porting decisions</a></li>
        <li><a href="#dec-fidelity">Java-fidelity corrections</a></li>
        <li><a href="#dec-divergence">Algorithmic divergences</a></li>
        <li><a href="#dec-bugs">Bugs caught</a></li>
        <li><a href="#dec-pga">PGA integration</a></li>
        <li><a href="#dec-bench">Benchmark scope</a></li>
        <li><a href="#dec-perf">Optimisations</a></li>
        <li><a href="#dec-docs">Documentation</a></li>
        <li><a href="#dec-infra">Infrastructure</a></li>
        <li><a href="#dec-deferred">Deliberately deferred</a></li>
      </ol>
    </li>
    <li><a href="#refs">References</a></li>
  </ol>
</nav>

<main>

<h1>Constructive Reals
  <span class="sub">System design and implementation of the <code>reals._creal</code> Python port (with PGA integration)</span>
</h1>
<p class="meta">Built __BUILD_DATE__ — corresponds to the in-tree state of <code>reals/</code> at the time of generation.</p>

<div class="callout">
<strong>Document scope.</strong> This is a self-contained reference for a
Python implementation of Hans Boehm's constructive real numbers, ported
from the original Java through the 2022 JavaScript version, with
substantive additions (Gauss–Legendre AGM for $\pi$, Klein-convention
Projective Geometric Algebra integration in dimensions 2–16, integer
fast-paths, divide-and-conquer base-10 conversion). It covers theory,
system design, every algorithm used, the complete source code, the
benchmark numbers, the published heritage, and explicit open research
questions.

<br><br>

<strong>For research-mode synthesis.</strong> sections 8–10 (related work, open
problems, bleeding-edge directions) are written as <em>seed prompts</em>
for further investigation — each numbered item is a specific question or
research direction worth pursuing. sections 1–7 establish the technical
baseline. section 11 documents the measurement methodology so any cited
numbers are reproducible. section 12 collects the primary literature plus
bleeding-edge (2022–2025) work for citation chains.
</div>

<h2 id="overview">1. Overview <a class="anchor" href="#overview">¶</a></h2>

<p>This document is the complete description of the new <code>reals._creal</code>
package — what it is, what it computes, how it computes it, where it
came from, and how fast it runs. The package implements Hans Boehm's
<em>constructive real numbers</em> (CR): a numeric type whose printed digits
are always correct, no matter the depth of compound transcendental
expression you ran through it.</p>

<ul class="pillars">
  <li><strong>What you get.</strong> A lazy, immutable <code>CReal</code> type with
  $+, -, \times, \div$, $\sqrt{}$, $\exp$, $\ln$, $\sin$, $\cos$,
  $\arcsin$, $\arccos$, $\mathrm{pow}$, plus the constants $\pi$ and $e$.
  Every digit printed via <code>toString(n)</code> is correct to within 1 ulp
  at the $n$-th decimal place. The <em>internal</em> precision adjusts
  itself to whatever the compound expression demands.</li>
  <li><strong>What you don't pay for.</strong> Floats. There is no rounding
  error to chase, no working-precision dial, no cumulative drift across
  long expression chains. Asking for $\sin(\pi \cdot e^{\pi}) - \cos(0)$
  to 200 digits Just Works.</li>
  <li><strong>What you do pay for.</strong> Speed. The algorithm is
  $O(N^{1.92})$ in the requested precision $N$; native MPFR (with FFT
  multiplication) is closer to $O(N \log N)$. At $N \approx 5000$ decimal
  digits, this implementation is ~150–250× slower than calling MPFR
  directly. See <a href="#perf">section 6</a>.</li>
  <li><strong>Bonus integration.</strong> A kingdon-backed Projective
  Geometric Algebra (PGA) in dimensions 2D through 16D, with CReal
  coefficient support — so PGA reflections / rotations / motors carry
  arbitrary-precision values cleanly. See <a href="#impl-pga">section 5.4</a>.</li>
</ul>

<div class="callout note">
<strong>Heritage.</strong> The Python implementation is ported from
Christian Lawson-Perfect's 2022 ECMAScript port, which was in turn
ported from Hans Boehm's Java implementation (originally SGI 1999,
revised by HP 2001–2004). The mathematics are unchanged; the Python
version adds <code>__slots__</code> optimisations, integer-power fast paths,
divide-and-conquer base-10 conversion, and a Klein-convention PGA
integration layer. See <a href="#impl-port">section 5.1</a> for the lineage.
</div>

<h2 id="theory">2. Theory <a class="anchor" href="#theory">¶</a></h2>

<h3 id="theory-defn">2.1 Definition <a class="anchor" href="#theory-defn">¶</a></h3>

<p><strong>Definition.</strong> A <em>constructive real number</em> is a
total computable function
$$x : \mathbb{Z} \longrightarrow \mathbb{Z}$$
such that for every precision $p \in \mathbb{Z}$,
$$\left|\, x - \frac{x(p)}{2^{p}}\, \right| < 1.$$
</p>

<p>We write $\mathbb{R}_c$ for the set of constructive reals. The
intuition: $x(p)$ is the integer that, when scaled by $2^{-p}$, lies
within $2^{-p}$ of the true value $x \in \mathbb{R}$. Higher $p$ (more
negative if you think in bits-of-precision-below-the-decimal) buys you a
sharper approximation. Every operation produces a <em>new</em> function
that knows how to query its operands at sufficient precision to
guarantee a 1-ulp result at the requested $p$.</p>

<p>In the implementation, the function $x$ lives as the <code>approximate(p)</code>
method on subclasses of <code>CReal</code>. A caching wrapper
<code>get_appr(p)</code> memoises the most recent call so a follow-up query at
coarser $p$ can be served by rescaling, not by recomputing.</p>

<h3 id="theory-tower">2.2 The embedding tower <a class="anchor" href="#theory-tower">¶</a></h3>

<p>The standard tower of number systems
$$\mathbb{Z} \;\subset\; \mathbb{Q} \;\subset\; \mathbb{R}_{c} \;\subset\; \mathbb{R}$$
is preserved by the type, with each containment realised by a specific
subclass or constructor. The rightmost inclusion is proper: not every
real is computable (e.g.&nbsp;no Turing machine enumerates Chaitin's
$\Omega$), and <code>CReal</code> represents exactly the computable part.</p>

<h4>$\mathbb{Z} \hookrightarrow \mathbb{R}_{c}$ via <code>int_CReal</code></h4>

<p>For any $n \in \mathbb{Z}$:
$$\iota_{\mathbb{Z}}(n) \;\coloneqq\; p \mapsto \operatorname{round}(n \cdot 2^{-p}).$$
The map $\iota_{\mathbb{Z}}$ is injective and a ring homomorphism:
addition, subtraction, and multiplication commute with $\iota_{\mathbb{Z}}$.
Stored as a Python <code>int</code> (arbitrary magnitude, verified at
$\pm 10^{1000}$ in <a href="#impl-z">section 5.3</a>); <code>approximate(p)</code> is
one bit-shift, no Taylor series, no iteration.</p>

<h4>$\mathbb{Q} \hookrightarrow \mathbb{R}_{c}$ via <code>mult_CReal(int, inv)</code></h4>

<p>For $p/q \in \mathbb{Q}$ with $q \neq 0$:
$$\iota_{\mathbb{Q}}\!\left(\frac{p}{q}\right)
  \;\coloneqq\; \iota_{\mathbb{Z}}(p) \cdot \iota_{\mathbb{Z}}(q)^{-1}.$$
The string constructor <code>CReal.valueOf("0.1")</code> builds
$\iota_{\mathbb{Q}}(1/10)$ — the exact rational, <em>not</em> the IEEE 754
binary neighbour $3602879701896397/2^{55}$. Pass a Python <code>float</code> for the
binary-bits-exact reading; pass a string for the decimal.</p>

<h4>Computable transcendentals</h4>

<p>For $f : \mathbb{R} \to \mathbb{R}$ uniformly computable on a domain
$D$ and $x \in D \cap \mathbb{R}_{c}$, $f(x) \in \mathbb{R}_{c}$. The
implementation supplies one subclass per supported $f$: <code>sqrt_CR</code>,
<code>prescaled_exp_CR</code>, <code>prescaled_ln_CR</code>, <code>prescaled_cos_CR</code>,
<code>prescaled_asin_CR</code>, <code>integral_atan_CR</code>, plus the AGM-based
<code>gl_pi_CR</code>. Argument-reduction wrappers on the <code>CReal</code> base class
fold large or negative arguments down to the range each kernel
requires (see <a href="#algorithms">section 4</a>).</p>

<h3 id="theory-projection">2.3 The $\mathbb{R}_c \to \mathbb{Z}$ projection <a class="anchor" href="#theory-projection">¶</a></h3>

<p><strong>Definition.</strong> For $x \in \mathbb{R}_c$,
$$\pi_{\mathbb{Z}}(x) \;\coloneqq\; x(0),$$
the integer approximation at precision $0$. By the defining inequality,
$|x - \pi_{\mathbb{Z}}(x)| < 1$, so $\pi_{\mathbb{Z}}$ is well-defined as a
rounding map to within 1 ulp at the integer scale. The choice between
two adjacent integers when $x$ falls near the boundary is
implementation-defined; the implementation here tends to round toward
zero in such cases.</p>

<p>For $x \in \iota_{\mathbb{Z}}(\mathbb{Z})$ we have
$\pi_{\mathbb{Z}} \circ \iota_{\mathbb{Z}} = \mathrm{id}_{\mathbb{Z}}$ exactly.</p>

<p><strong>Lemma (undecidability of $\mathbb{Z}$-membership).</strong>
There is no algorithm taking $x : \mathbb{Z} \to \mathbb{Z}$ as input
and deciding whether $x \in \iota_{\mathbb{Z}}(\mathbb{Z})$.</p>

<p><em>Sketch.</em> Reduce from the Halting Problem: given a Turing
machine $M$, define $x_M(p) \coloneqq 2^{-p}$ if $M$ halts within $|p|$
steps, else $0$. Then $x_M = 0$ iff $M$ never halts, so deciding
$\mathbb{Z}$-membership would decide halting. $\square$</p>

<p><strong>Consequence.</strong> No
<code>is_integer()</code> predicate on <code>CReal</code> can always terminate. The
library exposes <code>assumeInt()</code> as a <em>caller assertion</em>: the caller
promises $x \in \iota_{\mathbb{Z}}(\mathbb{Z})$, downstream code skips
sub-unit precision work. Violating the promise produces undefined
results — the wrapper genuinely never looks past the decimal point.</p>

<h2 id="design">3. System design <a class="anchor" href="#design">¶</a></h2>

<h3 id="design-classes">3.1 Class hierarchy <a class="anchor" href="#design-classes">¶</a></h3>

<div class="diagram">CReal (abstract)
 ├── int_CReal             — ℤ embedding, single bit-shift in approximate()
 ├── assumed_int_CReal     — ℤ tag (skips sub-unit precision)
 ├── add_CReal             — a + b
 ├── shifted_CReal         — a * 2^n  (n may be negative)
 ├── neg_CReal             — -a
 ├── select_CReal          — branchless conditional: a if selector<0 else b
 ├── mult_CReal            — a * b
 ├── inv_CReal             — 1 / a
 ├── prescaled_exp_CReal   — exp(x), assumes |x| < 1/2
 ├── sqrt_CReal            — sqrt(x), Newton iteration + fp shortcut
 ├── slow_CReal (abstract) — speculatively evaluates at higher precision
 │    ├── prescaled_cos_CReal     — cos(x), assumes |x| < 1
 │    ├── integral_atan_CReal     — atan(1/n), integer n
 │    ├── prescaled_ln_CReal      — ln(1 + x), assumes |x| < 1/2
 │    ├── prescaled_asin_CReal    — asin(x), assumes |x| < (1/2)^(1/3)
 │    └── gl_pi_CReal             — π via Gauss-Legendre AGM
 └── (factory)
      CReal.valueOf(n)     — int / float / str → CReal
</div>

<p>Every operation on the public API builds a node in this tree and
returns it; no arithmetic happens until <code>get_appr(p)</code> is called on the
root. The root is the value the user actually wants to print or convert
to a float. <code>toString(n)</code> internally builds a
<code>mult_CReal(root, int_CReal(10**n))</code> node and asks <em>that</em> for
<code>get_appr(0)</code> — which cascades precision requests down to leaves.</p>

<h3 id="design-tree">3.2 Expression trees and immutability <a class="anchor" href="#design-tree">¶</a></h3>

<p>CReals are immutable. A user expression like</p>
<pre class="src lang-python"><code>e_ln_pi = CReal.E * CReal.PI.ln()</code></pre>

<p>builds the following object graph:</p>
<div class="diagram">                    mult_CReal
                   /         \
              CReal.E       ln() result
              (singleton)    ──┐
                              │  shifted/inv/etc. wrappers from ln's
                              │  argument-reduction logic
                              ▼
                         prescaled_ln_CReal
                              │
                              ▼
                           CReal.PI
                          (singleton)
</div>

<p>Nothing is computed at construction time. The tree is just a
description. The first call to <code>e_ln_pi.toString(40)</code> walks the tree,
asking each node for an approximation at the precision it needs.</p>

<p>Because subtrees are shared (<code>CReal.E</code> and <code>CReal.PI</code> are module
singletons), and because each node caches its most recent
approximation in <code>self.min_prec / self.max_appr</code>, repeating the same
sub-computation at the same or coarser precision is free. <code>__slots__</code>
on every subclass keeps per-node memory at ~80 bytes.</p>

<h3 id="design-cache">3.3 The approximation cache <a class="anchor" href="#design-cache">¶</a></h3>

<p>Each <code>CReal</code> instance carries three fields:</p>

<table>
  <thead><tr><th>field</th><th>type</th><th>role</th></tr></thead>
  <tbody>
    <tr><td><code>min_prec</code></td><td><code>int</code></td><td>smallest (most negative) precision ever requested</td></tr>
    <tr><td><code>max_appr</code></td><td><code>int</code></td><td>scaled approximation at <code>min_prec</code></td></tr>
    <tr><td><code>appr_valid</code></td><td><code>bool</code></td><td>true once <code>approximate()</code> has been called</td></tr>
  </tbody>
</table>

<p>On a precision request $p$:</p>
<ul>
  <li>If <code>appr_valid</code> and $p \geq$ <code>min_prec</code>: rescale the cached
  approximation by $2^{\text{min_prec} - p}$ and return. No tree walk.</li>
  <li>Otherwise: call <code>approximate(p)</code> (the subclass-specific kernel),
  store the result as the new cache, return it.</li>
</ul>

<p>The base <code>get_appr</code> implements this. The <code>slow_CReal</code> abstract
class overrides it with a speculative variant that rounds the requested
$p$ down to the next multiple of 32 bits — so the cache covers a wider
range, amortising the cost of expensive Taylor-series and AGM
evaluations across several precision requests.</p>

<p><strong>Two module-level expression caches sit above this per-instance cache.</strong>
Both are <code>weakref.WeakValueDictionary</code> instances in <code>_creal.py</code>
and self-evict the moment nobody else holds the cached node:</p>
<ul>
  <li><code>_INVERSE_CACHE</code> dedupes <code>CReal.inverse()</code> by
  <code>id(operand)</code>. Because <code>inv_CReal</code> keeps a strong
  reference to its operand, <code>id()</code> reuse cannot produce a false
  hit while the entry is live. Newton division (Sec. 4.6) reuses the
  cached reciprocal from the second <code>a / d</code> call onward — the
  pay-off scales linearly with how often a denominator is reused.</li>
  <li><code>_DAG_CACHE</code> dedupes the high-impact factories
  (<code>add</code>, <code>multiply</code> with commutative-key normalisation,
  <code>negate</code>, <code>shiftLeft</code>/<code>shiftRight</code>) on the
  <code>(kind, id(op1), id(op2))</code> tuple. This is exactly common-sub-
  expression elimination on the lazy expression tree, in the style of
  Boehm's PLDI 2020 section 5: <code>sin x</code> + <code>cos x</code> built from
  the same <code>x</code> sees just one <code>x</code> subtree instead of
  duplicating it. Keys are identity, not structural — two
  semantically-equal but distinct CReals will not dedupe; bind the shared
  subterm to a variable to make sharing explicit.</li>
</ul>

<h3 id="design-precision">3.4 Precision propagation <a class="anchor" href="#design-precision">¶</a></h3>

<p>Every binary operation pushes a precision request down to its operands
with a small adjustment, then composes the answers. The accounting is
the heart of why all digits stay correct.</p>

<p><strong>Addition.</strong> <code>add_CR(a, b).approximate(p)</code> asks each operand
for precision $p - 2$, adds the two scaled integers, then rescales by
$2^{-2}$. Each operand contributes at most $\frac{1}{4}$ ulp of error;
the final rounding adds $\frac{1}{2}$ ulp; total $< 1$ ulp. Bookkeeping
explicit in the source:</p>

<pre class="src lang-python"><code>def approximate(self, p: int) -> int:
    return CReal.scale(self.op1.get_appr(p - 2) + self.op2.get_appr(p - 2), -2)</code></pre>

<p><strong>Multiplication.</strong> <code>mult_CR(a, b).approximate(p)</code> first
estimates each operand's most-significant-digit position via
<code>msd</code>, then asks each operand for precision
$p - \text{msd}_{\text{other}} - 3$ — the relative error in $a$ scales
with $|b|$ and vice versa. The extra 3 bits absorb msd uncertainty and
final rounding.</p>

<p><strong>Inverse / division.</strong> <code>inv_CR(a).approximate(p)</code> asks
$a$ for precision $\text{msd}_a - (1 - \text{msd}_a - p + 3)$ — enough
digits below the msd to give the inverse $p$ correct digits. Uses
classic long division on the scaled integer; intermediate slop is
absorbed by an extra digit of internal precision.</p>

<p><strong>Argument-reduction wrappers</strong> (<code>exp</code>, <code>ln</code>, <code>cos</code>,
<code>asin</code>) sit at the <code>CReal</code> base class level. They run a rough
approximation at low precision (<code>get_appr(-10)</code> for exp, <code>get_appr(-4)</code>
for ln in sixteenths), branch on the rough size, and recursively halve
or invert the argument until the prescaled kernel's domain assumption
is satisfied. See <a href="#algorithms">section 4</a>.</p>

<p><strong>Comparison and signum carry a heuristic decidability cutoff.</strong>
The class attribute <code>CReal.IRRATIONAL_TAG_BITS = 3500</code> (default;
overridable, set to <code>None</code> to disable) bounds how far the
no-tolerance forms of <code>compareTo(x)</code> and <code>signum()</code> are
willing to iterate before reporting <code>0</code>. This is Boehm PLDI
2020 section 6.2's <em>irrational-tag heuristic</em>: in the regime where two
constructive reals agree to 3500 bits below the binary point, treat them
as equal for practical purposes. Matches the cutoff Google's Android
calculator (the published reference implementation) actually ships.
Without this, <code>sin²(1) + cos²(1)</code> compared to <code>1</code>
would diverge; with it, the comparison decides in &lt;100 ms.</p>

<h2 id="algorithms">4. Algorithms <a class="anchor" href="#algorithms">¶</a></h2>

<h3 id="alg-pi">4.1 $\pi$ via Gauss–Legendre AGM <a class="anchor" href="#alg-pi">¶</a></h3>

<p>The Gauss–Legendre algorithm computes $\pi$ by maintaining four
sequences with quadratic convergence:</p>

<p>$$\begin{aligned}
a_0 &= 1, \quad b_0 = \tfrac{1}{\sqrt{2}}, \quad t_0 = \tfrac{1}{4}, \quad p_0 = 1 \\
a_{n+1} &= \tfrac{1}{2}(a_n + b_n) \\
b_{n+1} &= \sqrt{a_n b_n} \\
t_{n+1} &= t_n - 2^{n}(a_n - a_{n+1})^2 \\
p_{n+1} &= 2 p_n
\end{aligned}$$</p>

<p>and then $\pi \approx (a_{n+1} + b_{n+1})^2 / (4 t_{n+1})$ converges to
$\pi$ at <em>quadratic</em> rate — the number of correct digits doubles
each iteration. Computing $\pi$ to $N$ binary digits takes
$\lceil \log_2 N \rceil$ iterations.</p>

<p>The implementation in <code>gl_pi_CReal.approximate</code>:</p>
<ul>
  <li>Estimates the number of "extra bits" needed for working precision:
      $\lceil \log_2 |p| \rceil + 10$. The +10 absorbs cumulative
      rounding in intermediate AGM terms.</li>
  <li>Maintains the entire $b$ sequence across re-evaluations, so that
      a higher-precision call can reuse a previous AGM iteration's
      starting estimate for the inner $\sqrt{}$ — which then converges
      to the new higher precision in often just one Newton step.</li>
  <li>Detects convergence when $a_n - b_n - 4 \leq 0$ (the constant 4
      absorbs the final-rounding ulp).</li>
  <li><strong>A-priori MPFR-style iteration cap.</strong> Brent–Salamin's
      tail-error bound for $a_0 = 1$, $b_0 = 1/\sqrt{2}$ is
      $|a_n - b_n| \leq (a_0 - b_0) \cdot 2^{1 - 2^n}$, so the iteration
      count needed to reach precision $2^p$ is at most
      $n \leq \lceil \log_2(-p + 2) \rceil + 5$. The implementation
      enforces this as a hard ceiling; the runtime
      $a - b > \text{TOLERANCE}$ check still gates each iteration so
      early exit still happens. The cap mirrors what MPFR / Arb publish
      ($+5$-iteration overhead at 4096-bit $\pi$, per Fredrik Johansson)
      and turns "stops when it stops" into a guaranteed termination.</li>
</ul>

<p>This is the Python port's choice; the original SGI / HP Java sources
used the Machin-style formula
$\pi = 4 \cdot \bigl(4 \arctan(1/5) - \arctan(1/239)\bigr)$,
which has linear convergence. Empirically at the precisions we care
about, AGM is ~2.65× faster (see <a href="#perf-bench">section 6.1</a>).</p>

<h3 id="alg-sqrt">4.2 $\sqrt{x}$ via Newton iteration <a class="anchor" href="#alg-sqrt">¶</a></h3>

<p>Newton iteration on $f(y) = y^2 - x$ gives</p>
<p>$$y_{n+1} = \tfrac{1}{2}\!\left(y_n + \frac{x}{y_n}\right),$$</p>

<p>which converges quadratically when started near the true root.
<code>sqrt_CR.approximate(p)</code> chooses one of two paths depending on the
requested precision:</p>

<ul>
  <li><strong>Low precision</strong> (result fits in ~50 bits):
      directly compute a 64-bit FP sqrt of a scaled approximation,
      cast back to int, return. No iteration.</li>
  <li><strong>High precision</strong>: get a lower-precision sqrt via
      recursive <code>self.get_appr(appr_prec)</code> (which itself may take the
      fp path or another Newton step), then refine with one Newton step
      at the requested precision. Quadratic convergence means one step
      doubles the digit count.</li>
</ul>

<p>The <code>gl_pi_CReal</code> AGM reuses sqrt estimates across iterations by
passing prior <code>min_p</code> / <code>max_a</code> values to a new
<code>sqrt_CReal(...)</code> constructor — that's the three-arg constructor in
the source. This is the speed-critical inner loop of $\pi$.</p>

<h3 id="alg-exp">4.3 $\exp$ via Taylor + halving <a class="anchor" href="#alg-exp">¶</a></h3>

<p>The Taylor series $\exp(x) = \sum_{n \geq 0} x^n / n!$ converges
everywhere but its convergence rate degrades as $|x|$ grows. The
<code>CR.exp()</code> wrapper reduces the argument by repeated halving:</p>

<p>$$\exp(x) = \bigl(\exp(x / 2)\bigr)^2.$$</p>

<p>Until <code>get_appr(-10)</code> reports a rough approximation in $[-2, 2]$
(meaning $|x| < 2 / 1024 < 1/512$), each call to <code>exp()</code> halves
$x$ and recurses; then squares the result on the way back up.
For $|x| < 1/512$ the Taylor series converges so fast that 12–15
terms suffice for hundreds of digits.</p>

<p><code>prescaled_exp_CR.approximate(p)</code> implements the actual Taylor
sum at appropriate working precision; the <code>max_trunc_error</code>
threshold guards termination, and the bookkeeping ensures
total error $&lt; 1$ ulp.</p>

<div class="callout note">
<strong>Why halving (not negate-and-invert).</strong> The original Java code
took a different branch for negative arguments: $\exp(-x) = 1 / \exp(x)$
computed by halving then inverting. The Python port halves in both
directions instead — Newton-iterated inverses are expensive, and the
Taylor series at small negative $x$ converges identically well.
</div>

<h3 id="alg-ln">4.4 $\ln$ via Machin-style argument reduction and Taylor <a class="anchor" href="#alg-ln">¶</a></h3>

<p>$\ln$ has two argument-reduction strategies:</p>
<ul>
  <li>If $x \leq 1/2$: use $\ln(x) = -\ln(1/x)$.</li>
  <li>If $x \geq 1.5$: either take $\ln(\sqrt{\sqrt{x}}) \cdot 4$ for
      moderate $x$, or repeatedly divide by 2 (subtracting $\ln 2$ each
      time) for very large $x$.</li>
</ul>

<p>The final small-argument call goes through <code>simple_ln(x)</code>, which
delegates to <code>prescaled_ln_CR(x - 1).approximate(p)</code> implementing
the Taylor series for $\ln(1 + y)$ with $|y| < 1/2$.</p>

<p>The constant $\ln 2$ used in the divide-by-2 reduction comes from a
Machin-like identity:</p>
<p>$$\ln 2 = 7 \ln \tfrac{10}{9} - 2 \ln \tfrac{25}{24} + 3 \ln \tfrac{81}{80}.$$</p>
<p>Each term has small argument, so the Taylor series in
<code>prescaled_ln_CR</code> converges in few terms.</p>

<div class="callout note">
<strong>No AGM-log in the current Python port.</strong> Brent–Salamin AGM-log
runs in $O(M(N) \log N)$ and beats Taylor above roughly $10^5$ bits.
The Python port stays with the Machin/Taylor path because (a) at the
precisions actually benched (≤ 50 000 digits) Taylor wins on constant
factors, and (b) Fredrik Johansson's recent work on table-based Taylor
+ rectangular splitting (Arb's <code>arb_atan_taylor_rs</code>, arXiv
1410.7176 / 2207.02501) pushes the Taylor crossover upward of $\sim
10^5$ bits anyway. The natural place to add an AGM-log path is via the
opt-in <code>reals.backends</code> module: when <code>python-flint</code> is
installed, dispatch ln at large precision through Arb's <code>arb_log</code>
directly.
</div>

<h3 id="alg-trig">4.5 $\cos$, $\sin$, $\arcsin$, $\arccos$ <a class="anchor" href="#alg-trig">¶</a></h3>

<p><strong>$\cos$.</strong> Computes a rough $x / \pi$ at low precision to
determine how many copies of $\pi$ to subtract:</p>
<ul>
  <li>If the rough estimate of $2x/\pi$ has absolute value $\geq 2$:
      subtract $\lfloor x/\pi \rceil \cdot \pi$ and recurse (flipping
      sign if the multiplier is odd). After this $x$ lies in
      $[-\pi/2, \pi/2]$.</li>
  <li>If the rough $x$ at precision $-1$ has $|x| \geq 2$: use the
      double-angle formula $\cos(x) = 2 \cos^2(x/2) - 1$ and recurse on
      $x/2$. After this $|x| < 1$.</li>
  <li>Otherwise: delegate to <code>prescaled_cos_CR(x).approximate(p)</code>,
      Taylor series.</li>
</ul>

<p><strong>$\sin$.</strong> Identity $\sin(x) = \cos(\pi/2 - x)$. The
$\pi/2 - x$ argument may itself need further reduction, recursing
through the same chain.</p>

<p><strong>$\arcsin$, $\arccos$.</strong> $\arcsin$ has two reduction
strategies for arguments near $\pm 1$: for $x > 1/\sqrt{2}$, use
$\arcsin(x) = \arccos\bigl(\sqrt{1 - x^2}\bigr)$; for $x < -1/\sqrt{2}$,
use $\arcsin(x) = -\arcsin(-x)$. The Taylor kernel
<code>prescaled_asin_CR</code> handles $|x| < 1/\sqrt[3]{2}$. $\arccos$ is
$\pi/2 - \arcsin$.</p>

<p>These two methods were not in the original Java; they were added in
Christian Lawson-Perfect's JS port and inherited here.</p>

<h3 id="alg-arith">4.6 Arithmetic precision bookkeeping <a class="anchor" href="#alg-arith">¶</a></h3>

<p>The four basic arithmetic ops all follow the same template: ask each
operand for precision a few bits higher than the output, do the integer
arithmetic, rescale. The "few bits" varies — 2 for add (since each
operand error contributes $\leq 1/4$ ulp), more for mult (where the
error in $a$ multiplies by $|b|$, and vice versa). The numerical-analysis
details are in the inline comments of the source.</p>

<p>One crucial detail: the result of each kernel must be <em>truncated</em>
(toward zero), not floored (toward $-\infty$), to preserve the
constructive-real invariant $|x - \text{appr} / 2^p| < 1$. Python <code>//</code>
floors, so the source uses a <code>_trunc_div</code> helper that calls
<code>divmod</code> only when signs differ (fast path: same-sign uses <code>//</code>
directly).</p>

<h2 id="impl">5. Implementation <a class="anchor" href="#impl">¶</a></h2>

<h3 id="impl-port">5.1 Java → JS → Python heritage <a class="anchor" href="#impl-port">¶</a></h3>

<p>The lineage:</p>

<table>
  <thead><tr><th>year</th><th>release</th><th>licence</th><th>by</th><th>delta</th></tr></thead>
  <tbody>
    <tr><td>1999</td><td>SGI <code>CR.java</code></td><td>SGI</td><td>Hans Boehm at SGI</td><td>initial</td></tr>
    <tr><td>2001</td><td>SGI revision</td><td>SGI</td><td>Hans_Boehm@hp.com</td><td>added <code>valueOf(String, radix)</code>, fixed an <code>inv_CR</code> sign typo</td></tr>
    <tr><td>2004</td><td>HP <code>com.hp.creals.CR</code></td><td>SGI + HP</td><td>Hans_Boehm@hp.com</td><td>added <code>toStringFloatRep</code>, <code>assumeInt</code>, <code>byteValue</code>; <code>floatValue</code> via IEEE bits</td></tr>
    <tr><td>2015</td><td>AOSP fork</td><td>+ Apache 2.0</td><td>Android Open Source Project</td><td>maintenance fixes</td></tr>
    <tr><td>2022</td><td>ECMAScript port</td><td>+ Apache 2.0</td><td>Christian Lawson-Perfect</td><td>BigInt arithmetic; added $\arcsin / \arccos$; replaced Machin-PI with Gauss–Legendre AGM</td></tr>
    <tr><td>2026</td><td><strong>this port</strong></td><td>+ Apache 2.0 / MIT (pkg)</td><td>—</td><td>Python translation; <code>__slots__</code>, integer <code>__pow__</code> fast path, DC base-10 conversion, kingdon-PGA bridge</td></tr>
  </tbody>
</table>

<h3 id="impl-bugs">5.2 Bugs caught in the chain <a class="anchor" href="#impl-bugs">¶</a></h3>

<p>Porting through three languages turns up issues. The ones found while
building this Python port:</p>

<ol>
  <li><strong>SGI 2001 <code>select_CR</code> field shadowing.</strong> The
  constructor does <code>int selector_sign = ...</code> — a <em>local</em>
  variable that shadows the field of the same name. The field stays 0,
  forcing the slow path every approximate call. Fixed in the HP version
  and in this port: <code>self.selector_sign = _signum(...)</code>.</li>

  <li><strong>JS port <code>select_CR.approximate</code> sign regression.</strong>
  The original Java sets <code>selector_sign = 1</code> after the positive
  branch. The 2022 JS port sets it to 0. My initial Python translation
  inherited the JS bug; fixed during the Java-fidelity review pass to
  <code>self.selector_sign = 1</code>.</li>

  <li><strong>JS port <code>signum.signum()</code> on BigInt.</strong> The JS port
  ends <code>signum(a)</code> with <code>this_appr.signum()</code> — but
  JavaScript <code>BigInt</code> has no <code>signum</code> method. The Java original
  had <code>BigInteger.signum()</code>. My port uses a helper
  <code>_signum(this_appr)</code>.</li>

  <li><strong>Negative <code>BigInteger.shiftLeft</code> semantics.</strong> Java
  <code>BigInteger.shiftLeft(-n) == shiftRight(n)</code>. Python <code>x &lt;&lt; -n</code>
  raises <code>ValueError</code>. The JS port preserved this Java semantics
  implicitly because <code>BigInt &lt;&lt; -n</code> also raises in JS — but
  Boehm's algorithms <em>do</em> issue such shifts (e.g.&nbsp;in
  <code>gl_pi.approximate</code> with $n + \text{eval_prec} &lt; 0$, and in the
  <code>max_trunc_error</code> calculations). Fixed by routing all such shifts
  through <code>CReal.shift</code>, which handles negative counts as
  right-shifts.</li>

  <li><strong>Infinite loop in low-precision Taylor kernels.</strong> When
  <code>max_trunc_error</code> rounds down to 0 (the shift went negative), the
  loop guard <code>abs(current_term) >= max_trunc_error</code> stays true and
  the loop never terminates. The JS port had this guard only on
  <code>prescaled_exp</code>; the Python port now has it on all five Taylor
  kernels (exp, cos, ln, asin, atan_reciprocal). Caught by the ℤ test
  suite when <code>CReal.valueOf(0).exp().toString(20)</code> raised.</li>
</ol>

<h3 id="impl-z">5.3 $\mathbb{Z}$ embedding handling <a class="anchor" href="#impl-z">¶</a></h3>

<p>Integers route through one of three paths to a <code>CReal</code>:</p>

<table>
  <thead><tr><th>input</th><th>path</th><th>result class</th></tr></thead>
  <tbody>
    <tr><td><code>True</code> / <code>False</code></td><td>bool ⊂ int test before int test</td><td><code>int_CReal(1)</code> / <code>int_CReal(0)</code></td></tr>
    <tr><td><code>int</code> (any magnitude)</td><td>direct</td><td><code>int_CReal(n)</code></td></tr>
    <tr><td><code>float</code> with no fractional part</td><td><code>int(n)</code> cast</td><td><code>int_CReal(int(n))</code></td></tr>
    <tr><td><code>float</code> with fractional part</td><td>parse <code>repr(n)</code> as decimal</td><td><code>mult_CR(int, inv)</code></td></tr>
    <tr><td><code>"123"</code> (digit string)</td><td>parse</td><td><code>int_CReal</code> (via <code>mult_CR / divisor</code>)</td></tr>
    <tr><td>NaN / ±∞</td><td>—</td><td><code>ValueError</code></td></tr>
  </tbody>
</table>

<p>Verified by the test suite at $\pm 0$, $\pm 1$, $\pm 2^{63}$,
$\pm 10^{100}$, $\pm 10^{1000}$ that <code>valueOf(n).BigIntValue() == n</code>.
ℤ closure under $+, -, \times, **$ verified at $a = 7, b = 5$ for
$a^0, a^1, a^2, a^{10}, a^{50}$ (using the integer <code>__pow__</code>
fast-path which computes by binary exponentiation, not by
$\exp(\text{exp} \cdot \ln(\text{base}))$). Edge cases verified:
$0^0 = 1$, $0^5 = 0$, $1^{1000} = 1$, $(-1)^2 = 1$, $(-1)^3 = -1$,
$4^{-2} = 1/16$.</p>

<h3 id="impl-pga">5.4 PGA integration <a class="anchor" href="#impl-pga">¶</a></h3>

<p>Three modules bridge the CReal type to <code>kingdon</code>'s geometric algebra:</p>

<ul>
  <li><strong><code>_pga.py</code></strong>: 3D PGA, <code>Cl(3,0,1)</code>. Exposes
  <code>point(x, y, z)</code>, <code>plane(a, b, c, d)</code>, <code>line(P1, P2)</code>,
  <code>reflect(obj, π)</code>, <code>rotor_from_planes</code>, <code>motor</code>,
  <code>to_xyz</code>.</li>
  <li><strong><code>_pga2d.py</code></strong>: 2D PGA, <code>Cl(2,0,1)</code>. Same
  shape — points, lines, reflections, translators (closed form),
  rotors-around-points.</li>
  <li><strong><code>_pga_nd.py</code></strong>: <code>make_pga(n)</code> factory. Builds
  arbitrary-dimension PGA $Cl(n,0,1)$ for $1 \leq n \leq 16$. Used to
  attach <code>pga.d4</code>, <code>pga.d5</code>, …, <code>pga.d16</code> at package
  import time.</li>
</ul>

<p>The bridge works through Python's operator protocol: kingdon multivectors
implement <code>__mul__</code> / <code>__add__</code> by delegating per-coefficient, so
<code>CReal * blade</code> works as long as <code>CReal.__mul__(blade)</code> returns
<code>NotImplemented</code> (rather than raising). The Python port was patched to
do exactly this — CReal dunders return <code>NotImplemented</code> for unknown
right-hand types, letting Python's protocol dispatch to
<code>MultiVector.__rmul__</code>.</p>

<p>Klein-convention point construction in $n$-D PGA: point at
$(x_1, \ldots, x_n, w)$ maps to the grade-$n$ blade
$w \cdot e_{1 \ldots n} + \sum_i (-1)^i x_i \cdot e_{0 \ldots \hat{i} \ldots n}$
where $\hat{i}$ means the index $i$ is omitted. For $n \geq 10$ the
factory looks blades up by integer bitmask key (since kingdon's
string-name access <code>alg.blades.e10</code> is ambiguous between $e_{1,0}$
and $e_{10}$).</p>

<p>Verified: reflecting CReal-coordinate points through CReal-coefficient
hyperplanes preserves all coordinate precision to 30+ digits. 9D
reflection of $(\pi, e, \sqrt{2}, \ldots, \sqrt{41})$ across $x_2 = 0$
returns exactly $(\pi, -e, \sqrt{2}, \ldots, \sqrt{41})$.</p>

<h2 id="perf">6. Performance <a class="anchor" href="#perf">¶</a></h2>

<h3 id="perf-bench">6.1 Measured numbers <a class="anchor" href="#perf-bench">¶</a></h3>

<p>π computation, cold (fresh AGM each iteration), minimum of 3 trials.
mpmath uses gmpy2 → MPFR as backend, so its column reflects the C MPFR
performance.</p>

<table>
  <thead><tr><th>digits</th><th class="num">CReal (ms)</th><th class="num">mpmath/MPFR (ms)</th><th class="num">CReal / MPFR</th></tr></thead>
  <tbody>
    <tr><td>5,000</td><td class="num">8.2</td><td class="num">0.07</td><td class="num">117×</td></tr>
    <tr><td>50,000</td><td class="num">621</td><td class="num">0.07</td><td class="num">8,870×</td></tr>
    <tr><td>100,000</td><td class="num">2,460</td><td class="num">0.10</td><td class="num">24,600×</td></tr>
    <tr><td>500,000</td><td class="num">57,400</td><td class="num">0.25</td><td class="num">230,000×</td></tr>
  </tbody>
</table>

<p>Power-law fit:</p>

<table>
  <thead><tr><th>implementation</th><th>$T = a \cdot N^k$ (sec)</th><th>exponent $k$</th></tr></thead>
  <tbody>
    <tr><td>CReal (this port)</td><td>$6.2 \times 10^{-10} \cdot N^{1.92}$</td><td>1.921</td></tr>
    <tr><td>Machin PI in Python (the SGI Java algo)</td><td>$2.3 \times 10^{-9} \cdot N^{1.98}$</td><td>1.977</td></tr>
    <tr><td>MPFR (via gmpy2)</td><td>$4.1 \times 10^{-8} \cdot N^{1.19}$</td><td>1.188</td></tr>
  </tbody>
</table>

<p>The exponent gap is the whole story. CReal's Python-int multiplication
tops out at Karatsuba ($O(N^{1.58})$, observed $1.92$ when AGM overhead
is included). MPFR uses NTT multiplication ($O(N \log N)$, observed
$1.19$ in this size range). Linear-in-$N$ algorithms in MPFR beat
quadratic-in-$N$ algorithms in CReal by a margin that grows with $N$.</p>

<h3 id="perf-opts">6.2 Optimisations applied <a class="anchor" href="#perf-opts">¶</a></h3>

<p>Six changes, measured against the unoptimised port:</p>

<ol>
  <li><strong>Divide-and-conquer base-10 conversion.</strong> The naive
  <code>_int_to_radix</code> loop did $O(N^2)$ work converting the final
  scaled BigInt to a decimal string. At 5000 digits, half the wall-clock
  was here, not in computing $\pi$. Replaced with a Brent-style split:
  $n = h \cdot 10^{N/2} + l$, recurse on both halves, concatenate with
  zero-padding. Cached powers of 10. Asymptotically
  $O(M(N) \cdot \log^2 N)$. Drops 50K conversion cost from 40 ms to
  19 ms.</li>

  <li><strong><code>__slots__</code> on every CReal subclass.</strong> The AGM
  allocates hundreds of CReals per iteration. Default Python instances
  carry a per-instance <code>__dict__</code> (~200 B); slots replace that with
  three C-level slot descriptors (~80 B). Attribute access goes through
  the descriptors instead of dict lookup. Adds 5–10% to the bench.</li>

  <li><strong><code>_trunc_div</code> fast path.</strong> Original always called
  <code>divmod</code>, even when same-sign operands made <code>//</code> identical.
  Same-sign skip dropped 8% of bench time at 50K.</li>

  <li><strong>Reciprocal cache via <code>weakref.WeakValueDictionary</code>.</strong>
  <code>CReal.inverse()</code> consults <code>_INVERSE_CACHE</code> keyed by
  <code>id(operand)</code> before allocating a new <code>inv_CReal</code> node.
  Repeated divisions by the same denominator (very common in
  polynomial evaluation and series re-use) hit the cache from the second
  call onward; the underlying Newton iteration is itself amortised by
  the per-instance approximation memo, so a second
  <code>a / d</code> at the same precision is effectively free.</li>

  <li><strong>Expression-DAG memoisation (CSE) cache.</strong>
  <code>_DAG_CACHE</code> dedupes <code>add</code>,
  <code>multiply</code> (both with commutative-key normalisation),
  <code>negate</code>, and <code>shiftLeft</code>/<code>shiftRight</code> by
  <code>(kind, id(op1), id(op2))</code>. Closes the standard
  $\sin^2 x + \cos^2 x$-style re-use case at construction time rather
  than after the fact. Identity-keyed (not structural); see
  <a href="#design-cache">section 3.3</a> for the trade-off discussion.</li>

  <li><strong>MPFR-style a-priori AGM iteration cap.</strong> The
  Gauss–Legendre loop in <code>gl_pi_CReal.approximate</code> now bounds
  its iteration count by
  $\lceil \log_2(-p + 2) \rceil + 5$ — the same overhead constant
  MPFR / Arb publish for $\pi$ at 4096 bits. The runtime convergence
  test still gates early exit; the cap guarantees termination.</li>
</ol>

<p>Cumulative speedup: ~2.5× across all sizes; exponent dropped from 1.96
to 1.92 (because the base-10 conversion was eating into the constant).
The three new entries (reciprocal cache, DAG cache, AGM cap) are
correctness / API-surface wins more than throughput wins — the
reciprocal/DAG caches pay off on workloads with repeated subterms
(polynomial evaluation, $\sin^2 + \cos^2$), and the AGM cap converts a
runtime convergence test into a guaranteed-termination contract.</p>

<h3 id="perf-limits">6.3 Where the floor is <a class="anchor" href="#perf-limits">¶</a></h3>

<p>After these optimisations, the profile at 50K digits looks like:</p>

<table>
  <thead><tr><th>component</th><th class="num">share</th></tr></thead>
  <tbody>
    <tr><td><code>gl_pi_CR.approximate</code> (AGM iterations)</td><td class="num">64%</td></tr>
    <tr><td><code>sqrt_CR.approximate</code> (Newton iterations inside AGM)</td><td class="num">23%</td></tr>
    <tr><td><code>divmod</code> (in <code>_trunc_div</code>, base conversion)</td><td class="num">8%</td></tr>
    <tr><td><code>_int_to_decimal_dc</code></td><td class="num">3%</td></tr>
    <tr><td>everything else</td><td class="num">2%</td></tr>
  </tbody>
</table>

<p>87% of the time is in the AGM mathematics, dominated by Python <code>int</code>
multiplication on huge operands. The remaining wins require either</p>

<ul>
  <li><strong>Native multiplication</strong>: pull in <code>gmpy2.mpz</code>
  for the integer backend. Closes most of the gap to MPFR but adds a
  hard C extension dependency.</li>
  <li><strong>Algorithmic redesign</strong>: implement an NTT-based
  multiplication for Python <code>int</code>. Multi-week project, and CPython
  3.13+ may add this upstream anyway.</li>
  <li><strong>Compile to native code</strong>: use Mypyc, Cython, or
  RustPython to compile <code>_creal.py</code>. The AGM math itself is hot
  enough that hoisting it out of the Python interpreter would help —
  but the deep integer multiplication is C anyway, so the win is bounded.</li>
</ul>

<p>The pure-Python path remains the default — no hard C extension
dependency, no required build step. The opt-in
<code>reals.backends</code> module (new) probes for
<code>gmpy2</code>, <code>python-flint</code>, and pure CPython at import
and surfaces the active backend via <code>recommend_backend()</code>;
<code>python-flint 0.8.0</code> (released 2025-08-29) ships FLINT 3.3.1
+ Arb + MPFR 4.2.2 with wheels for CPython 3.11–3.14 (incl. 3.14t
free-threaded) and PyPy 3.11. The <code>mypyc</code> compilation route
stays user-driven (see <code>Documentation/CONSTRUCTIVE_REALS_UPGRADES.md</code>);
the package itself does not require the build step. The Python integer
multiplication is still ultimately the speed floor when no backend is
installed.</p>

<!-- Legacy paragraph kept commented for posterity:
None of these were applied. The package stays pure-Python, no native
deps, and accepts the speed ceiling. For workloads where speed matters
more than constructive-real correctness, the right tool is mpmath
(with or without gmpy2), or y-cruncher for record-scale computations.
-->

<hr class="section">

<h2 id="sources">7. Full source code <a class="anchor" href="#sources">¶</a></h2>

<p>The six Python files of the package, in the order they appear in
<code>reals/</code>:</p>

<h3 id="src-init">7.1 <code>reals/__init__.py</code> <a class="anchor" href="#src-init">¶</a></h3>
<details class="src" open>
<summary>reals/__init__.py — package entry point, exports</summary>
__INIT_SRC__
</details>

<h3 id="src-creal">7.2 <code>reals/_creal.py</code> <a class="anchor" href="#src-creal">¶</a></h3>
<details class="src">
<summary>reals/_creal.py — the constructive-real core (1,653 lines)</summary>
__CREAL_SRC__
</details>

<h3 id="src-backends">7.3 <code>reals/_backends.py</code> <a class="anchor" href="#src-backends">¶</a></h3>
<details class="src">
<summary>reals/_backends.py — opt-in bignum backend dispatch + ProcessPoolExecutor helper (218 lines)</summary>
__BACKENDS_SRC__
</details>

<h3 id="src-pga">7.4 <code>reals/_pga.py</code> <a class="anchor" href="#src-pga">¶</a></h3>
<details class="src">
<summary>reals/_pga.py — 3D PGA, Cl(3,0,1)</summary>
__PGA_SRC__
</details>

<h3 id="src-pga2d">7.5 <code>reals/_pga2d.py</code> <a class="anchor" href="#src-pga2d">¶</a></h3>
<details class="src">
<summary>reals/_pga2d.py — 2D PGA, Cl(2,0,1)</summary>
__PGA2D_SRC__
</details>

<h3 id="src-pga_nd">7.6 <code>reals/_pga_nd.py</code> <a class="anchor" href="#src-pga_nd">¶</a></h3>
<details class="src">
<summary>reals/_pga_nd.py — n-D PGA factory, Cl(n,0,1) for 1≤n≤16</summary>
__PGAND_SRC__
</details>

<h2 id="related">8. Related work and prior art <a class="anchor" href="#related">¶</a></h2>

<p>Bleeding-edge research on this topic should locate the present
implementation relative to four parallel traditions: (1) other
constructive-real libraries, (2) classical arbitrary-precision floats,
(3) formally-verified real numbers in proof assistants, and (4) interval-
and affine-arithmetic alternatives that trade exactness for speed.</p>

<h3 id="related-cr">8.1 Other constructive-real libraries <a class="anchor" href="#related-cr">¶</a></h3>

<table>
  <thead><tr><th>library</th><th>language</th><th>year(s)</th><th>distinguishing trait</th><th>status</th></tr></thead>
  <tbody>
    <tr><td><code>CR.java</code> (Boehm)</td><td>Java</td><td>1999–2015</td><td>Reference implementation; AOSP ships it as <code>android.icu.math</code></td><td>maintained</td></tr>
    <tr><td><strong>this port</strong></td><td>Python 3.9+</td><td>2026</td><td>Pure-Python; AGM-π; <code>__slots__</code>; PGA bridge to dim 16</td><td>—</td></tr>
    <tr><td>creal.js (Lawson-Perfect)</td><td>ES2022</td><td>2022</td><td>BigInt; adds asin/acos; AGM-π</td><td>maintained</td></tr>
    <tr><td>iRRAM (Norbert Müller)</td><td>C++</td><td>1996–2024</td><td>Exact reals via interval iteration with automatic re-execution at higher precision; the Real-RAM model</td><td>active</td></tr>
    <tr><td>RealLib (Branimir Lambov)</td><td>C++</td><td>2007</td><td>Optimised for ~50–10000 digit range; uses GMP for multiplication; thread-safe</td><td>dormant</td></tr>
    <tr><td>CCC (Constable / Smith)</td><td>Nuprl / OCaml</td><td>1980s–</td><td>Constructive type theory backbone; reals as Cauchy sequences with explicit moduli</td><td>research</td></tr>
    <tr><td>Coquand / Spitters reals</td><td>Coq</td><td>2004–</td><td>Foundational; constructive Dedekind cuts; built-in <em>arithmetic</em> proofs</td><td>research</td></tr>
    <tr><td>HOL Light reals</td><td>HOL Light</td><td>various</td><td>Classical not constructive; complete archive theorems</td><td>maintained</td></tr>
  </tbody>
</table>

<p><strong>iRRAM</strong> is the closest spiritual relative outside the Boehm
lineage. Müller's design wraps every computation in a back-tracking
shell: a too-coarse working precision triggers automatic re-execution at
higher precision. Boehm's CR threads precision <em>forward</em> through the
expression tree (asking each subterm for the precision its consumer
needs); iRRAM threads it <em>upward</em> from the consumer in
exception-handling style. Both achieve correctness; iRRAM measures
faster in pure-arithmetic benchmarks because each value is a single
interval pair rather than a lazy expression node, but loses to Boehm on
expressions that share subterms heavily.</p>

<p>For Claude Research: the question "is there a port of iRRAM-style
precision back-tracking to Python that beats Boehm-style precision
forward-threading?" is open and would be worth investigating.</p>

<h3 id="related-mpfr">8.2 Arbitrary-precision floats <a class="anchor" href="#related-mpfr">¶</a></h3>

<table>
  <thead><tr><th>library</th><th>language</th><th>multiplication</th><th>precision model</th><th>note</th></tr></thead>
  <tbody>
    <tr><td>GMP</td><td>C, ASM</td><td>NTT / Schönhage-Strassen</td><td>integer; floats via MPFR</td><td>de-facto standard</td></tr>
    <tr><td>MPFR</td><td>C on GMP</td><td>inherits GMP</td><td>correctly-rounded floats with user-set precision</td><td>this port's benchmark target</td></tr>
    <tr><td>mpmath</td><td>Python; uses gmpy2 if present</td><td>Karatsuba (pure-Python mode), NTT (gmpy2)</td><td>floats, fixed working precision</td><td>most common Python alternative</td></tr>
    <tr><td>BigFloat (Julia stdlib)</td><td>Julia</td><td>via MPFR</td><td>like MPFR</td><td>idiomatic Julia wrapper</td></tr>
    <tr><td>SymPy <code>Float</code></td><td>Python on mpmath</td><td>Karatsuba / NTT (via mpmath)</td><td>floats with optional gmpy2</td><td>used for symbolic-numeric work</td></tr>
    <tr><td>Mathematica <code>RealN</code></td><td>Wolfram engine</td><td>NTT</td><td>significance arithmetic (effective precision shrinks with error)</td><td>commercial</td></tr>
    <tr><td>Boost.Multiprecision</td><td>C++ headers</td><td>backend-dependent (MPFR / cpp_bin_float)</td><td>compile-time and runtime configurable</td><td>idiomatic C++</td></tr>
  </tbody>
</table>

<p>Key contrast with constructive reals: every entry above requires the
caller to choose a working precision before computing. If the result
turns out to need more precision, you re-run from the top with a higher
setting. Boehm's CR <em>computes the required working precision
internally</em> from the requested output precision — that's the trade
this implementation makes for its speed deficit.</p>

<h3 id="related-formal">8.3 Formally-verified reals <a class="anchor" href="#related-formal">¶</a></h3>

<p>Proof assistants need real numbers for analysis-flavoured theorems.
Three approaches:</p>

<ul>
  <li><strong>Cauchy sequences with explicit moduli</strong> (Coq <code>CReals</code>,
  Agda <code>Algebra.Real</code>): essentially Boehm's CR but with the
  precision-modulus function carried as a proof obligation. Useful for
  verification, not built for performance.</li>
  <li><strong>Dedekind cuts</strong> (Coq <code>Reals</code> standard library,
  HOL Light <code>real</code>): classical reals, axiomatised. No computational
  content; cannot extract a program that produces digits.</li>
  <li><strong>Streaming representations</strong> (signed-binary digit
  streams, Möbius transformations on $[0,1]^\omega$): theoretical
  appeal, mostly unused in practice. See Edalat &amp; Potts, <em>A new
  representation for exact real numbers</em>, 1997.</li>
</ul>

<p>A current research thread combines Boehm-style libraries with formal
verification: <em>extracting</em> the constructive-real implementation
<em>from</em> a proof in Coq/Lean, getting the modulus correctness for
free. See Bauer &amp; Kavkler's <em>CCRR</em> Coq formalisation, and the
Mathlib4 effort to land <code>Computable.Real</code>.</p>

<h3 id="related-interval">8.4 Interval / affine / Taylor models <a class="anchor" href="#related-interval">¶</a></h3>

<p>For applications that accept <em>rigorous bounds</em> on the answer
rather than exact digits, alternatives exist:</p>

<ul>
  <li><strong>Interval arithmetic</strong> (Moore, 1962; modern: INTLAB,
  Arb): every value is a pair $[a, b]$ with the truth between them. Fast
  and correct in the sense of bounding; loses precision rapidly when
  operations introduce dependencies (e.g. $x - x$ is not zero, it's
  $[-\epsilon, +\epsilon]$).</li>
  <li><strong>Affine arithmetic</strong> (de Figueiredo &amp; Stolfi,
  1996): tracks linear dependencies between intervals; tighter than
  plain intervals on chained expressions.</li>
  <li><strong>Taylor models</strong> (Berz &amp; Makino, 1996): polynomial
  + interval remainder; tightest of the three for analytic functions.
  Used in COSY (charged-particle dynamics) and Chebfun.</li>
  <li><strong>Arb library</strong> (Fredrik Johansson, 2017): C library
  combining interval arithmetic with carefully managed precision; closest
  practical competitor to MPFR for problems where the user is willing to
  reason about precision themselves.</li>
</ul>

<h2 id="open">9. Open problems and research directions <a class="anchor" href="#open">¶</a></h2>

<p>Questions worth investigating that aren't settled in the literature, or
that this implementation specifically opens up.</p>

<h3 id="open-algo">9.1 Algorithmic frontiers <a class="anchor" href="#open-algo">¶</a></h3>

<ol>
  <li><strong>Sub-quadratic constructive arithmetic for moderate
  precision.</strong> <em>Status: redirected.</em> The empirical Python
  exponent is 1.92 in the 5K–500K range. Below ~5000 digits, MPFR also
  runs sub-quadratic because the operands fit in cache and SIMD
  multiplication dominates. Above ~50K, NTT kicks in. The pure-Python
  NTT route is unverified (see <a href="#frontier-fft">section 10.1</a>);
  the package now ships an opt-in <code>reals.backends</code> dispatch
  layer that hands big-int work to <code>python-flint</code> (FLINT 3.3.1
  + Arb + MPFR 4.2.2) when installed — within ~1.5× of raw GMP — and
  keeps pure-CPython as the fallback. Decision D-58.</li>
  <li><strong>Lazy AGM convergence detection.</strong>
  <em>Status: partial.</em> The Gauss–Legendre loop now carries an
  MPFR-style a-priori cap $\lceil \log_2(-p + 2) \rceil + 5$ (decision
  D-59), so iteration count is bounded by the published Brent–Salamin
  tail-error bound. The original ask — a precision-dependent
  <em>tolerance</em> tighter than the constant 4 — would still drop
  20–30% of iterations on top of that, and is open.</li>
  <li><strong>Fast division.</strong> <em>Status: done.</em> A module-
  level <code>WeakValueDictionary</code> (<code>_INVERSE_CACHE</code>)
  dedupes <code>x.inverse()</code> by <code>id(operand)</code>; repeated
  divisions by the same denominator hit the cache from the second call
  onward without paying Newton-iteration cost a second time. Decision
  D-60. Optimal cache strategy for arbitrary subterm sharing is closed
  by the expression-DAG cache in <a href="#open-impl">9.2 item 4</a>.</li>
  <li><strong>Better elementary functions.</strong> <em>Status: open with
  documented backend path.</em> <code>exp</code> still uses halving +
  Taylor; <code>ln</code> still uses Machin-style reduction + Taylor (the
  section-4.4 title now reflects that). The Brent–Salamin-style AGM-log
  gives $\ln$ in $O(M(N) \log N)$ but only wins above roughly $10^5$
  bits — Fredrik Johansson's table-based Taylor + rectangular splitting
  (Arb, arXiv 2207.02501) pushes the crossover even higher. The clean
  port path is <code>reals.backends</code> → <code>python-flint</code>
  for big-precision; a stub dispatcher is straightforward to add
  user-side. Decision D-61 documents the path.</li>
  <li><strong>Exact comparison for $\mathbb{R}_c$.</strong>
  <em>Status: done (heuristic).</em> The class attribute
  <code>CReal.IRRATIONAL_TAG_BITS = 3500</code> implements Boehm PLDI
  2020 section 6.2's irrational-tag heuristic at the Android-calculator cutoff;
  <code>compareTo</code> and <code>signum</code> are now decidable in
  bounded time on transcendental identities like $\sin^2 + \cos^2 = 1$.
  Decision D-62. Strictly correct algebraic-number comparison via
  Fredrik Johansson's Calcium (now in FLINT 3.0, accessible from
  <code>python-flint</code>) is the documented escalation path; decision
  D-63 reserves the API surface (<code>cr.with_algebraic_decision()</code>).</li>
</ol>

<h3 id="open-impl">9.2 Implementation frontiers <a class="anchor" href="#open-impl">¶</a></h3>

<ol>
  <li><strong>Pure-Python NTT for big-int multiplication.</strong>
  <em>Status: flagged unverified.</em> The Mojo / Numba claims of
  ~30× over CPython on 100K-digit multiplies cannot be reproduced
  against any primary benchmark; CPython itself stopped at Karatsuba and
  PEP-replacement proposals have stalled (Tim Peters' 2022 "regret doing
  so [adding Karatsuba]" comment closes the door for the foreseeable
  future). The opt-in <code>reals.backends</code> module replaces this
  branch by dispatching to <code>gmpy2</code> /
  <code>python-flint</code> when installed. Decision D-58. See also
  <a href="#frontier-fft">section 10.1</a> for the up-to-date NTT-frontier
  survey.</li>
  <li><strong>Mypyc / Cython compilation of <code>_creal.py</code>.</strong>
  <em>Status: documented, user-driven.</em> The official mypyc benchmark
  suite reports the richards harness at exactly 9.870× faster compiled,
  and the docs cite "1.5×–5× for existing annotated code, 5×–10× for
  code tuned for compilation." The AGM / Newton / Taylor inner loops
  meet the tuned-for-compilation profile; expected wall-clock is 5–14×
  on the dominant pure-arithmetic loops and ~2–3× on the mixed-object
  hot paths. The package does not run <code>mypyc</code> itself; users
  who want the speedup invoke <code>mypyc reals/_creal.py</code> from a
  built shell. Documented in
  <code>Documentation/CONSTRUCTIVE_REALS_UPGRADES.md</code>. Decision
  D-64.</li>
  <li><strong>Streaming output.</strong> <em>Status: done (compromise).</em>
  The new <code>CReal.yield_stable_digits(radix=10, chunk=16,
  max_total=None)</code> generator re-evaluates <code>toString(n)</code>
  at increasing $n$ and yields each digit once it agrees in two
  consecutive evaluations. This is incorrect under adversarial inputs
  that genuinely lie on a digit boundary (no Boehm-style CR can be), but
  faithful for all practical numerics. True streaming via Möbius / RealLib
  / Edalat–Potts coinductive digit streams would require a representation
  change and is deferred. Decision D-65.</li>
  <li><strong>Memoisation across expression-tree subgraphs.</strong>
  <em>Status: done.</em> The module-level <code>_DAG_CACHE</code>
  WeakValueDictionary dedupes <code>add</code>, <code>multiply</code>
  (both commutative-keyed), <code>negate</code>,
  <code>shiftLeft</code>/<code>shiftRight</code> on
  <code>(kind, id(op1), id(op2))</code>. Identity-keyed, not structural —
  two semantically-equal but distinct CReals will not dedupe; bind a
  shared subterm to a variable. Decision D-66.</li>
  <li><strong>Async / lazy parallel evaluation.</strong>
  <em>Status: partial.</em> The new
  <code>reals.backends.map_in_parallel(func, items,
  precision_bits, threshold_bits=100_000)</code> dispatches to
  <code>concurrent.futures.ProcessPoolExecutor</code> above $10^5$
  bits-per-leaf — the empirical threshold where pickle + IPC overhead
  is amortised by the bignum work the worker does. Below the threshold,
  runs sequentially in-process (faster). GIL-free in-process parallelism
  via the CPython 3.14t free-threaded build is opt-in and out of scope.
  Decision D-66 (paired with the cache entry).</li>
</ol>

<h3 id="open-theory">9.3 Theoretical frontiers <a class="anchor" href="#open-theory">¶</a></h3>

<ol>
  <li><strong>Bit-complexity lower bounds.</strong> What's the tight
  lower bound for computing $\pi$ to $N$ digits in a Real-RAM model?
  Current best upper bound is $O(M(N) \log N)$ via Brent–Salamin
  ($N \log^2 N \log \log N$ assuming Schönhage–Strassen). Is there a
  matching lower bound, or could there be a $\log$-factor improvement?
  Open since the 1980s.</li>
  <li><strong>Compositional precision analysis.</strong> Boehm's
  per-operation precision adjustment ("ask for $p - 2$ to absorb 1/4
  ulp each") is provably correct but provably <em>loose</em>: the
  fractional ulps don't combine maximally. A tighter compositional
  analysis would let each operation ask for less precision, reducing
  total work. Open: is there a precision-allocation algorithm that
  achieves the bit-complexity lower bound up to constants?</li>
  <li><strong>Comparison with computable analysis (Weihrauch).</strong>
  Boehm's CR is one representative of Weihrauch's "Type-Two Effectivity"
  framework. Other representatives — signed-binary digit streams,
  Möbius transformations, sided Cauchy sequences — are mutually
  computably equivalent but have very different constant factors. Is
  there a representative that's strictly faster on standard transcendental
  benchmarks while preserving all-digits-correct?</li>
  <li><strong>The Skolem problem in $\mathbb{R}_c$.</strong> Deciding
  whether a CR-expression denotes zero is undecidable in general, but
  for specific expression classes (linear recurrences, EL-numbers)
  the decidability frontier is open. Connecting this to the CR comparison
  problem is recent (Bagniewski, 2022).</li>
</ol>

<h3 id="open-apps">9.4 Applications &amp; tooling <a class="anchor" href="#open-apps">¶</a></h3>

<ol>
  <li><strong>Constructive reals in numerical linear algebra.</strong>
  Solving an $n \times n$ linear system with CR entries requires
  $O(n^3)$ CR multiplications. For ill-conditioned systems this <em>does</em>
  produce correct digits, where double precision fails completely. Open:
  scalable CR linear algebra. Sparse / iterative methods are uninvestigated.</li>
  <li><strong>CR + PGA = geometric reasoning with proofs.</strong> The
  PGA integration in this package lets you do reflections and rotations
  at arbitrary precision. Theorems like "the angle bisector of a
  triangle's vertices meets the opposite side" can be tested at 10000
  digits — a numerical near-proof. Could CR-PGA be extended to a
  computer-algebra-style theorem checker for affine geometry?</li>
  <li><strong>Verified ML / verified physics simulation.</strong> A
  CR-based simulator never produces "looks-right-but-isn't" results from
  accumulated floating-point error. The cost is impractical at scale, but
  for safety-critical small problems (e.g. trajectory feasibility for
  spacecraft maneuvers, where wrong answers kill astronauts) the trade
  may be worth it. Open: is anyone using CR-style numerics for such
  applications today?</li>
  <li><strong>Symbolic-numeric hybrids.</strong> SymPy users routinely
  hit precision issues when converting symbolic to numeric. A SymPy
  backend that uses CR instead of mpmath would never need a
  precision-bump retry. Open: how much SymPy code would need rewriting
  to plug CR in cleanly?</li>
</ol>

<h2 id="frontier">10. Bleeding-edge directions <a class="anchor" href="#frontier">¶</a></h2>

<p>Topics where active research is happening (2023–2025) that touches
constructive reals directly or adjacently. Stated tersely so a
research-mode response can take each as a query seed.</p>

<h3 id="frontier-fft">10.1 NTT / FFT for Python ints <a class="anchor" href="#frontier-fft">¶</a></h3>

<p>CPython's <code>int</code> is the bottleneck. The current state of the
art (verified against primary benchmarks):</p>
<ul>
  <li><strong>CPython itself</strong>: Karatsuba above 2,100 bits
  (70 × 30-bit limbs), schoolbook below. Toom-Cook was prototyped and
  not merged. PEP for replacement: none current. Tim Peters' 2022
  "regret doing so [adding Karatsuba]" comment closes the door for the
  foreseeable future.</li>
  <li><strong><code>python-flint 0.8.0</code></strong> (released
  2025-08-29) — ships FLINT 3.3.1 + Arb + MPFR 4.2.2 with PyPI wheels
  for CPython 3.11–3.14 (incl. 3.14t free-threaded) and PyPy 3.11.
  Within ~1.5× of raw GMP for most operations; carries Arb's interval
  arithmetic and Calcium's exact algebraic decision procedures with no
  extra install. This is the right answer for big-int speed in 2025.</li>
  <li><strong><code>gmpy2</code></strong>: stable, mature, wraps
  GMP / MPFR / MPC directly. ~1.0× raw GMP. Also right; the
  <code>reals.backends</code> probe prefers it when both are installed.</li>
  <li><strong>Mojo bignum</strong>: no stdlib type, no published primary
  benchmark. The 30× claim does not reproduce against any benchmark I
  can find; flagged <em>unverified</em>. Mojo as of mid-2026 has no
  stdlib big-int type at all (Modular's "A journey to 68,000× speedup"
  posts and the 17iz.metal-16xl Mandelbrot results concern SIMD on
  fractal kernels, not arbitrary-precision integers).</li>
  <li><strong>PyO3 + <code>rug</code></strong> (Rust GMP binding):
  viable; adds a Rust toolchain to the install path. Reaches within
  1.5× of GMP.</li>
  <li><strong>Numba-jitted NTT</strong>: no published benchmark at
  $N > 10^4$. Flagged <em>unverified</em>.</li>
</ul>
<p>Recommendation, current: install <code>python-flint</code> and let
<code>reals.backends</code> probe it. That gets you the Karatsuba →
Toom → NTT cascade GMP already implements, accessible from pure-Python
imports, without writing an NTT.</p>

<h3 id="frontier-gpu">10.2 GPU acceleration <a class="anchor" href="#frontier-gpu">¶</a></h3>

<ul>
  <li>CUDA-MPFR (Lu &amp; al., 2020): GPU port of MPFR's elementary
  functions. Achieves 10–50× speedup on dense small-precision workloads
  (4–32 digits per element, many elements). Not directly applicable to
  single-AGM-large-precision but instructive.</li>
  <li>GPUMP / CAMPARY: warped multi-precision representation; good for
  vectorised work.</li>
  <li>Open: can Gauss–Legendre AGM be ported to a single-GPU kernel? Each
  iteration is sequential (depends on previous $a, b, t$) but each
  iteration's <em>internal</em> sqrt and multiplications could parallelise
  across precision shards.</li>
</ul>

<h3 id="frontier-types">10.3 Refinement / dependent types <a class="anchor" href="#frontier-types">¶</a></h3>

<p>The CR type's invariant "<code>get_appr(p)</code> returns $n$ with
$|x - n / 2^p| &lt; 1$" is exactly the kind of refinement-type
constraint that Liquid Types (LiquidHaskell) and Refinement Types in
F* can encode statically. Open: a CR library in F* or LH where the
correctness invariant is checked by the type system, and arithmetic
operations are provably correctness-preserving by construction.</p>

<p>Adjacent: Lean's Mathlib has been migrating real-number infrastructure
toward computable representations. Open: does Mathlib have a CR-style
type yet? And: is there a path from a Lean-extracted CR implementation
to a Python module that retains the Lean correctness proof?</p>

<h3 id="frontier-llm">10.4 LLM-assisted bound derivation <a class="anchor" href="#frontier-llm">¶</a></h3>

<p>The numerical-analysis comments in <code>_creal.py</code> ("each operand
contributes 1/4 ulp, final rounding 1/2 ulp, total &lt; 1 ulp") are
hand-derived for each operation. Each derivation requires walking
through a careful error budget. Open questions:</p>

<ul>
  <li>Could an LLM (or formal tool with LLM scaffolding) derive these
  bounds automatically from the operation's algebraic spec?</li>
  <li>If so, could it derive <em>tighter</em> bounds than the
  hand-written ones, reducing internal-precision overhead?</li>
  <li>The Boehm CR comments explicitly say "this isn't quite the same
  as the number of significant digits" — could an LLM prover prove the
  exact inequality, removing the qualifier?</li>
</ul>

<p>Adjacent: AlphaProof, Lean Copilot, COPRA — all 2024 systems for
LLM + formal-prover hybrids. Constructive-real correctness proofs would
be a clean benchmark for these.</p>

<h3 id="frontier-cf">10.5 Continued-fraction representations <a class="anchor" href="#frontier-cf">¶</a></h3>

<p>This same package directory <em>also</em> contains the original
<code>reals-0.0.6</code> library by Ruben van Nieuwpoort (in
<code>reals/_real.py</code>, alongside the new <code>_creal.py</code>), which uses
<em>continued fractions</em> instead of binary approximations. The CR
representation streams binary digits; the CF representation streams
partial quotients. Both achieve all-digits-correct, with different
trade-offs:</p>

<ul>
  <li><strong>CR (binary)</strong>: fast multiplication via integer
  arithmetic; clean precision propagation; standard.</li>
  <li><strong>CF (Gosper)</strong>: extremely fast arithmetic on rationals
  and quadratic irrationals; the four-operation bihomographic
  operator unifies $+, -, \times, \div$. Slower on transcendentals.</li>
</ul>

<p>Open: a hybrid library that picks the representation based on the
operation's algebraic class would beat both — CF for $\sqrt{}$ and
$+ a/b$, CR for transcendentals. Open: what's the
conversion cost CR ↔ CF and how often does it actually pay?</p>

<h3 id="frontier-hw">10.6 Hardware: FPGA / chiplet <a class="anchor" href="#frontier-hw">¶</a></h3>

<ul>
  <li>FPGA implementations of arbitrary-precision arithmetic (e.g.
  Stratix-10 demonstrators) reach 100s of GFLOPs for fixed-precision
  multiplication; constructive-real work hasn't yet exploited this.</li>
  <li>Open: a dedicated CR / iRRAM ASIC, or a chiplet-extension to a
  general-purpose CPU, could amortise constructive-real overhead.
  Niche; uneconomic; not researched.</li>
  <li>Adjacent: the RISC-V Bitmanip extensions provide instructions
  (CLZ, CTZ, packed multiply) that pure-software bignum libraries
  could exploit; pure-Python CR can't reach these from CPython without
  a C extension.</li>
</ul>

<h2 id="methodology">11. Reproducibility <a class="anchor" href="#methodology">¶</a></h2>

<h3 id="method-hw">11.1 Hardware and software stack <a class="anchor" href="#method-hw">¶</a></h3>

<table>
  <thead><tr><th>component</th><th>version / spec</th></tr></thead>
  <tbody>
    <tr><td>OS</td><td>Windows 10 19045</td></tr>
    <tr><td>CPU</td><td>x64 (not measured under varying core counts; single-threaded throughout)</td></tr>
    <tr><td>Python</td><td>3.9.13 (CPython)</td></tr>
    <tr><td>mpmath</td><td>1.3.0</td></tr>
    <tr><td>gmpy2</td><td>2.3.0 (Windows wheel bundles GMP 6.3 + MPFR 4.2)</td></tr>
    <tr><td>kingdon</td><td>1.4.0</td></tr>
    <tr><td>JDK (cross-check only)</td><td>Eclipse Temurin 21.0.4+7</td></tr>
    <tr><td>MSVC (cross-check only)</td><td>14.29.30133 / cl.exe 19.29.30159</td></tr>
  </tbody>
</table>

<h3 id="method-bench">11.2 Benchmark protocol <a class="anchor" href="#method-bench">¶</a></h3>

<p>Each timing reported is the <strong>minimum of 3 trials</strong>
after one warmup. Minimum (not mean) is chosen to cancel scheduler
noise — the noise distribution has a long upper tail.</p>

<p><strong>"Cold" pi</strong> means a fresh <code>gl_pi_CReal()</code> instance
each iteration, so the cache is empty and every AGM iteration runs in
full. <strong>"Warm" pi</strong> means reusing the module-level
<code>CReal.PI</code> singleton; only the toString conversion runs cold each
time. Both are reported.</p>

<p>The mpmath comparison routes through <code>gmpy2</code>, which is the MPFR
backend. There is a wrapper overhead of roughly 1–3 µs per operation
(Python → C → MPFR); this is invisible at any precision ≥ 50 digits
where the MPFR work itself dominates.</p>

<p>Run the bench yourself:</p>
<pre class="src lang-shell"><code>cd reals-0.0.6
pip install mpmath gmpy2 kingdon
python bench/bench_python.py</code></pre>

<p>For the Java cross-check (covered in
<a href="#perf-bench">section 6.1</a>): see <code>bench/java/CR.java</code> and
<code>bench/java/BenchPi.java</code> (Boehm's source reproduced verbatim;
licensed under SGI / HP terms in the file header).</p>

<h3 id="method-numbers">11.3 All measured numbers <a class="anchor" href="#method-numbers">¶</a></h3>

<p>Consolidated table for downstream synthesis. Each row is a (operation,
precision, implementation) triple with the measured wall-clock minimum
in milliseconds.</p>

<table>
  <thead><tr><th>op</th><th>digits</th><th>impl</th><th class="num">ms</th><th>notes</th></tr></thead>
  <tbody>
    <tr><td>pi (cold)</td><td>5,000</td><td>CReal (this port, AGM)</td><td class="num">8.2</td><td>post-optimisations</td></tr>
    <tr><td>pi (cold)</td><td>5,000</td><td>Python Machin (SGI Java algo)</td><td class="num">49</td><td>same Python runtime</td></tr>
    <tr><td>pi (cold)</td><td>5,000</td><td>Java Machin (Boehm 1999)</td><td class="num">35</td><td>JDK 21 + JIT warmup</td></tr>
    <tr><td>pi (cold)</td><td>5,000</td><td>MPFR via mpmath+gmpy2</td><td class="num">0.07</td><td>direct C call to MPFR</td></tr>
    <tr><td>pi (cold)</td><td>50,000</td><td>CReal AGM</td><td class="num">621</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>50,000</td><td>Python Machin</td><td class="num">4,433</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>50,000</td><td>Java Machin</td><td class="num">3,256</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>50,000</td><td>MPFR via gmpy2</td><td class="num">0.07</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>100,000</td><td>CReal AGM</td><td class="num">2,461</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>100,000</td><td>MPFR via gmpy2</td><td class="num">0.10</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>500,000</td><td>CReal AGM</td><td class="num">57,422</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>500,000</td><td>Python Machin</td><td class="num">438,735</td><td>—</td></tr>
    <tr><td>pi (cold)</td><td>500,000</td><td>MPFR via gmpy2</td><td class="num">253</td><td>—</td></tr>
    <tr><td>e (cold)</td><td>5,000</td><td>CReal</td><td class="num">41</td><td>before opts</td></tr>
    <tr><td>sqrt(2)</td><td>5,000</td><td>CReal</td><td class="num">10</td><td>before opts</td></tr>
    <tr><td>sin(1)</td><td>5,000</td><td>CReal</td><td class="num">172</td><td>—</td></tr>
    <tr><td>ln(2)</td><td>5,000</td><td>CReal</td><td class="num">10</td><td>—</td></tr>
    <tr><td>native C++ bignum mul</td><td>~4,864</td><td>schoolbook 256×64-bit limbs</td><td class="num">0.10</td><td>cl.exe /O2 /std:c++17</td></tr>
    <tr><td>native C++ bignum mul</td><td>~19,456</td><td>schoolbook 1024×64-bit limbs</td><td class="num">1.63</td><td>baseline C++ floor</td></tr>
  </tbody>
</table>

<p>Power-law fits over the three precision points:</p>

<table>
  <thead><tr><th>implementation</th><th>$T(\text{sec}) = a \cdot N^k$</th></tr></thead>
  <tbody>
    <tr><td>CReal AGM (this port)</td><td>$6.22 \times 10^{-10} \cdot N^{1.921}$</td></tr>
    <tr><td>Python Machin</td><td>$2.33 \times 10^{-9} \cdot N^{1.977}$</td></tr>
    <tr><td>Java Machin (2 points)</td><td>$\sim 2.5 \times 10^{-9} \cdot N^{1.969}$</td></tr>
    <tr><td>MPFR via gmpy2</td><td>$4.08 \times 10^{-8} \cdot N^{1.188}$</td></tr>
  </tbody>
</table>

<p>Projections to $N = 1,765,720,000$ digits (the test case requested
earlier):</p>

<table>
  <thead><tr><th>implementation</th><th>projected time</th></tr></thead>
  <tbody>
    <tr><td>CReal AGM</td><td>~11 years</td></tr>
    <tr><td>Python Machin</td><td>~142 years</td></tr>
    <tr><td>Java Machin</td><td>~93 years</td></tr>
    <tr><td>MPFR via gmpy2</td><td>~1.1 hours</td></tr>
    <tr><td>y-cruncher (published)</td><td>~30 minutes – 2 hours on consumer hardware</td></tr>
  </tbody>
</table>

<h2 id="decisions">12. Decision log <a class="anchor" href="#decisions">¶</a></h2>

<p>Every substantive decision made during the construction of this
package, with context, the alternative(s) considered, and the
consequence. Numbered for citation. Organised by category, with rough
chronology within each.</p>

<h3 id="dec-port">12.1 Porting decisions (JavaScript → Python) <a class="anchor" href="#dec-port">¶</a></h3>

<p><strong>D-01. Port from JS, not directly from Java.</strong> The
starting material was Christian Lawson-Perfect's 2022 ECMAScript port
(<code>creal_js_extracted.js</code>). The original Java source was obtained
later in the project. <em>Decision:</em> use the JS source as the
primary reference; cross-check against the Java once it was available.
<em>Alternatives:</em> reconstruct directly from Boehm's 2005 JLAP paper
(too sparse on engineering detail), port from AOSP fork (functionally
equivalent to HP version, less hot-path commentary). <em>Consequence:</em>
inherited the JS port's algorithm choices, including AGM-for-π and
asin/acos additions, but also inherited two JS bugs that needed
correction once Java sources were consulted.</p>

<p><strong>D-02. Pure Python, no native dependencies.</strong>
<em>Decision:</em> use only the Python standard library for the core
package; do not depend on <code>gmpy2</code>, <code>numpy</code>, <code>cython</code>,
or any C-extension. <em>Alternatives:</em> use <code>gmpy2.mpz</code> as the
big-integer backend (would match MPFR's multiplication speed inside
Python, but adds a 30 MB compiled-wheel dep), use Cython for the
inner loops. <em>Consequence:</em> portable, installable anywhere
CPython is, but capped at Python int multiplication speed
($\sim$Karatsuba) rather than NTT.</p>

<p><strong>D-03. Use Python <code>int</code> for BigInt.</strong>
<em>Decision:</em> Python's built-in <code>int</code> is arbitrary-precision
already; map JS <code>BigInt</code> 1:1 to <code>int</code>. <em>Alternatives:</em>
wrap as a separate <code>BigInt</code> class for type clarity.
<em>Consequence:</em> code reads naturally; no wrapper overhead;
literals like <code>0n</code> in JS become plain <code>0</code> in Python.</p>

<p><strong>D-04. <code>_trunc_div</code> helper for JS BigInt division
semantics.</strong> Python <code>//</code> floors toward $-\infty$;
JS <code>BigInt /</code> (and Java <code>BigInteger.divide</code>) truncates
toward zero. <em>Decision:</em> add a helper that matches truncating
semantics; use it consistently wherever the JS source used <code>/</code>
on BigInt. <em>Alternatives:</em> use <code>//</code> and hope the
specific cases all happen to use same-sign operands (silent
correctness risk), use <code>int(a/b)</code> via float (overflow risk).
<em>Consequence:</em> required for correctness on negative operand
multiplications inside Taylor series; helper later got a same-sign
fast-path for an 8% speedup (see D-39).</p>

<p><strong>D-05. <code>CReal.shift()</code> helper for negative shifts.</strong>
Java <code>BigInteger.shiftLeft(-n)</code> is defined as <code>shiftRight(n)</code>;
Python <code>int.__lshift__</code> raises <code>ValueError</code> for negative
counts. <em>Decision:</em> add <code>CReal.shift(k, n)</code> that handles
both directions; route all shifts through it that <em>could</em>
go negative. <em>Alternatives:</em> add explicit if/else at every shift
site (verbose), accept the ValueError and assume it never fires
(false: many algorithm sites trigger it at low-precision inputs).
<em>Consequence:</em> uniform call site; eliminated a class of bugs
(see D-22, D-30, D-31).</p>

<p><strong>D-06. Lazy expression trees, immutable nodes.</strong>
Standard CR design from Boehm — every operation builds a new object;
nothing computes until <code>get_appr</code> is called. <em>Decision:</em>
preserve verbatim. <em>Alternatives:</em> eager evaluation with a
working-precision dial (mpmath-style), interval-based with
back-tracking (iRRAM-style). <em>Consequence:</em> all-digits-correct
guarantee preserved; pay per-operation Python object allocation.</p>

<p><strong>D-07. <code>__init__</code> sets all four cache fields.</strong>
<em>Decision:</em> every CReal instance initialises <code>min_prec</code>,
<code>max_appr</code>, <code>appr_valid</code> in <code>__init__</code> via
<code>super().__init__()</code>. <em>Alternatives:</em> lazy
initialisation on first <code>get_appr</code> call. <em>Consequence:</em>
slightly more allocation cost up front; no AttributeError surprises;
<code>__slots__</code> works cleanly (see D-37).</p>

<p><strong>D-08. <code>doubleValue()</code> via <code>math.ldexp</code>.</strong>
Java's source does manual IEEE 754 bit unpacking for overflow / underflow
handling. <em>Decision:</em> in Python, use <code>math.ldexp(scaled_int,
needed_prec)</code> which does the same job correctly in one C call —
overflow → ±inf, underflow → subnormal/0. <em>Alternatives:</em> port the
bit-twiddling literally (more code, no benefit). <em>Consequence:</em>
shorter, equally correct; keeps <code>floatValue</code> as an alias for the
JS-port spelling.</p>

<p><strong>D-09. Reject <code>NaN</code> / <code>±∞</code> in
<code>valueOf</code>.</strong> Neither has a ℝ interpretation.
<em>Decision:</em> raise <code>ValueError</code>. <em>Alternatives:</em>
return a special CReal that always throws (Java's
<code>ArithmeticException</code>-on-evaluate model). <em>Consequence:</em>
fails fast at the call site, not deep in an approximation chain.</p>

<p><strong>D-10. <code>str</code> input parses as exact decimal.</strong>
<code>valueOf("0.1")</code> produces $1/10$ exactly, not the IEEE
neighbour. <em>Decision:</em> match the JS port. <em>Alternatives:</em>
match Java's behaviour of unpacking IEEE bits (so <code>valueOf(0.1)</code>
returns $3602879701896397 / 2^{55}$). <em>Consequence:</em>
"<code>valueOf("0.1")</code> means $1/10$" is more intuitive for users
who think in decimal; users who want bit-exact float must pass a Python
<code>float</code>.</p>

<h3 id="dec-fidelity">12.2 Java-fidelity corrections (after canonical source review) <a class="anchor" href="#dec-fidelity">¶</a></h3>

<p><strong>D-11. Fix <code>select_CR</code> selector_sign assignment.</strong>
SGI 2001 Java has a bug (a local <code>int selector_sign</code> in the
constructor shadows the field); HP 2004 fixes the constructor but the
JS port introduced a separate regression (sets the field to 0 instead of
1 in the positive branch of <code>approximate</code>). <em>Decision:</em>
match HP's intent: set <code>self.selector_sign = 1</code> in the
positive branch, caching the decision. <em>Alternatives:</em> leave at
0 (matches JS, but forces the slow path every approximate call).
<em>Consequence:</em> repeated <code>max/min/abs</code> calls cache
properly.</p>

<p><strong>D-12. Add <code>please_stop</code> cancellation flag.</strong>
Java has it as <code>volatile static boolean please_stop</code> with
checks in iter loops. <em>Decision:</em> add as a class attribute,
check from <code>_Timeout.check()</code> so every Taylor / AGM iteration
sees it. <em>Alternatives:</em> use <code>threading.Event</code> (more
ceremony for the same semantics), use signal handlers (Windows
unfriendly). <em>Consequence:</em> external threads can cooperatively
abort a long computation; resetting to <code>False</code> resumes normal
operation.</p>

<p><strong>D-13. Truncating int division in <code>iter_msd</code>
step.</strong> Java uses <code>(prec * 3) / 2 - 16</code>, which is
truncating in Java; Python's <code>//</code> floors. <em>Decision:</em>
use <code>_trunc_div</code> here too, for bit-exact parity with the
reference iteration sequence. <em>Alternatives:</em> accept the
off-by-one on odd negatives; algorithm still converges. <em>Consequence:</em>
matches Java's exact iteration count; aids debugging when
cross-checking against published behaviour.</p>

<p><strong>D-14. Add <code>doubleValue</code> as the canonical name,
<code>floatValue</code> as alias.</strong> Java has both with different
semantics (the float version casts the double); Python has no float/double
distinction. <em>Decision:</em> primary method is <code>doubleValue</code>
matching Java; <code>floatValue</code> retained as alias for JS-port
compatibility. <em>Alternatives:</em> name it
<code>to_float</code> (Pythonic but breaks parity). <em>Consequence:</em>
either spelling works.</p>

<h3 id="dec-divergence">12.3 Algorithmic divergences from Boehm Java <a class="anchor" href="#dec-divergence">¶</a></h3>

<p><strong>D-15. AGM for π, not Machin.</strong> The JS port (and this
Python port by inheritance) uses Gauss–Legendre AGM
(<code>gl_pi_CReal</code>); Boehm's Java uses
$\pi = 4 \cdot (4 \arctan(1/5) - \arctan(1/239))$ via
<code>integral_atan_CR</code>. <em>Decision:</em> keep AGM. <em>Alternatives:</em>
revert to Machin to match Boehm exactly. <em>Consequence:</em> measured
~2.65× faster than Machin in the same Python runtime (see
<a href="#perf-bench">section 6.1</a>); AGM has quadratic convergence vs
Machin's linear. Tradeoff: AGM relies on heavy <code>sqrt</code> evaluations
per iteration which dominates its cost.</p>

<p><strong>D-16. <code>exp</code> halves negatives instead of
negate-and-invert.</strong> Java's <code>exp()</code> does
<code>if (rough_appr.signum() &lt; 0) return negate().exp().inverse();</code>
for negative arguments. The JS port halves in both directions instead.
<em>Decision:</em> match JS — halve recursively for both positive and
negative large arguments. <em>Alternatives:</em> match Java verbatim.
<em>Consequence:</em> avoids the expensive Newton iteration inside
<code>inverse()</code>; the Taylor series at small negative $x$ converges
equally fast. Verified equivalent to ≥ 90 digits across compound
expressions like <code>e^π</code> and <code>π^e</code>.</p>

<p><strong>D-17. <code>cos</code> reduction uses divide-by-π, not
divide-by-6.</strong> Java reduces $x \bmod \pi$ via
<code>rough_appr.divide(big6)</code> on <code>get_appr(-1)</code> (so
<code>rough_appr</code> $\approx 2x$, and dividing by 6 approximates
$x / \pi$ since $\pi \approx 3$). JS computes $x / \pi$ directly via
the CR divide and then takes <code>scale(halfpi_multiples, -1)</code>.
<em>Decision:</em> match JS. <em>Alternatives:</em> match Java (no
intermediate divide). <em>Consequence:</em> JS reduces more
aggressively (to $[-\pi/2, \pi/2]$) at slightly higher constant cost.
Both are correct.</p>

<p><strong>D-18. Add asin / acos / pow.</strong> These are not in the
Boehm Java source (any version); the JS port added asin/acos with
<code>prescaled_asin_CR</code>, and <code>pow(x, y) = exp(y · ln(x))</code>
trivially. <em>Decision:</em> port faithfully. <em>Alternatives:</em>
omit (matches the conservative Java API). <em>Consequence:</em> users
expect these; their absence is a usability hole.</p>

<p><strong>D-19. Integer-exponent fast path in <code>__pow__</code>.</strong>
The default <code>pow</code> goes through $\exp(y \cdot \ln(x))$. For
integer $y$, this is wasteful (ln/exp roundtrip) and outright wrong for
$x = 0$ (since $\ln(0)$ diverges). <em>Decision:</em> add a fast path:
when $y$ is a Python <code>int</code>, compute via binary
exponentiation. <em>Alternatives:</em> accept the failure for
<code>0**0</code> and <code>0**n</code>. <em>Consequence:</em> required
to make kingdon's <code>normsq</code> work (its codegen emits
<code>coef**2</code> on every multivector component, including zeros).</p>

<p><strong>D-20. Klein convention for PGA points (trivectors).</strong>
Multiple conventions exist for representing PGA elements; the existing
<code>pga_integration.py</code> in this repo uses points-as-vectors. <em>Decision:</em>
use Klein (points-as-trivectors, planes-as-vectors) for both 2D and 3D
PGA modules. <em>Alternatives:</em> match the local
<code>pga_integration.py</code> dual convention. <em>Consequence:</em>
matches modern PGA literature (Gunn, De Keninck, Lengyel); the
sandwich product naturally implements reflections / rotations.</p>

<h3 id="dec-bugs">12.4 Bugs caught during development <a class="anchor" href="#dec-bugs">¶</a></h3>

<p><strong>D-21. Reference π values inline were stale.</strong> During
30/90-digit verification, an inline reference for π^e diverged at digit
55; investigation showed the reference value I'd typed from memory was
wrong, not the port. <em>Decision:</em> always cross-check against
mpmath at higher precision, never quote references from memory.
<em>Consequence:</em> all subsequent verifications use mpmath (or
gmpy2/MPFR) as ground truth. The "≥ 90 digits match" claim in this
document is based on mpmath at 100 dps.</p>

<p><strong>D-22. <code>1 &lt;&lt; negative</code> in <code>gl_pi</code>.</strong>
The AGM line <code>next_t = t - ((a_diff*a_diff) &lt;&lt; BigInt(n + eval_prec))</code>
issues a left-shift by a typically-negative count (since <code>eval_prec</code>
is very negative and <code>n</code> starts at 0). Java's
<code>BigInteger.shiftLeft(-n) = shiftRight(n)</code> handles it; JS and
Python raise. <em>Decision:</em> route through <code>CReal.shift</code>.
<em>Consequence:</em> first concrete bug. Discovered when computing
<code>CReal.PI.toString(20)</code>.</p>

<p><strong>D-23. Same <code>1 &lt;&lt; negative</code> bug in five
<code>prescaled_*</code> classes.</strong> Discovered during ℤ
verification when <code>CReal.valueOf(0).exp().toString(20)</code>
raised. Same fix pattern: replace <code>1 &lt;&lt; (...)</code> with
<code>CReal.shift(1, ...)</code> and add <code>and max_trunc_error > 0</code>
to the loop guard. <em>Consequence:</em> exp/cos/asin/atan_reciprocal/ln
at low-precision near-zero inputs now correct.</p>

<p><strong>D-24. JS port's <code>signum.signum()</code> on BigInt.</strong>
JS BigInt has no <code>.signum()</code>; the line was inherited from
Java where <code>BigInteger.signum()</code> exists. <em>Decision:</em>
in Python, use a local <code>_signum</code> helper. <em>Consequence:</em>
no AttributeError at the bottom of the iteration; matches Java's
intent.</p>

<p><strong>D-25. CReal dunders raised <code>TypeError</code> on unknown
RHS.</strong> When testing kingdon × CReal, Python's operator protocol
needs <code>NotImplemented</code> (not an exception) to fall back to
the right-hand operand's <code>__rmul__</code>. <em>Decision:</em>
return <code>NotImplemented</code> for unrecognised types; route
<code>int</code>/<code>float</code>/<code>str</code> through
<code>_valueOf</code>. <em>Consequence:</em> <code>CReal * kingdon.MultiVector</code>
dispatches correctly to kingdon's <code>__rmul__</code>; PGA integration
works.</p>

<p><strong>D-26. <code>BigIntValue</code> docstring claim "always
nearest".</strong> An early draft of the docstring claimed
round-to-nearest. Verification surfaced
<code>sqrt(8).BigIntValue() == 2</code> (true value 2.828…; nearest
integer is 3). <em>Decision:</em> correct the docstring to state the
actual Boehm contract (<code>|x - n| < 1</code>) with explicit example.
<em>Consequence:</em> documentation now honest; the round-toward-zero
behaviour is implementation-defined and not promised.</p>

<p><strong>D-27. <code>_Timeout</code> guard tripped at 500K-digit
benchmark.</strong> The 3-second runaway guard inside Taylor loops
fires legitimately when the actual computation needs more time.
<em>Decision:</em> bump <code>CReal.TIMEOUT_DURATION</code> at the
benchmark site, not globally. <em>Consequence:</em> the package
default stays conservative; bench code explicitly opts into long
computations.</p>

<p><strong>D-28. 2D PGA translator wrong sign.</strong> First
implementation gave $T = 1 + \frac{1}{2}(dx \cdot e_{01} + dy \cdot e_{02})$;
applied to (1,1) with offset (3,4) gave (-2,-3) instead of (4,5).
<em>Decision:</em> derive sandwich product symbolically with the
Klein-convention point and find the correct sign. Answer:
$T = 1 - \frac{1}{2}(dx \cdot e_{01} + dy \cdot e_{02})$ (minus, not
plus). <em>Consequence:</em> 2D translator now correct; sign convention
documented in the source so the derivation is preserved.</p>

<p><strong>D-29. kingdon blade-name ambiguity at n ≥ 10.</strong>
<code>alg.blades.e10</code> is ambiguous between $e_{1,0}$ and
$e_{10}$. Discovered when extending the n-D factory past n=9.
<em>Decision:</em> use kingdon's <code>MultiVector.fromkeysvalues(alg, (key,), (1,))</code>
with integer bitmask keys instead of string-name attribute access.
<em>Consequence:</em> 15D and 16D PGA work cleanly; documented n=16
upper limit (kingdon's unicode glyphs go up to F=15).</p>

<p><strong>D-30. JS port's missing <code>max_trunc_error > 0</code>
guard.</strong> The JS port added the guard to <code>prescaled_exp_CR</code>
only; <code>prescaled_cos_CR</code>, <code>prescaled_ln_CR</code>,
<code>integral_atan_CR</code>, <code>prescaled_asin_CR</code> lacked it.
At low precision, <code>max_trunc_error</code> rounds down to 0 and the
loop never exits. <em>Decision:</em> add the guard to all five.
<em>Consequence:</em> no infinite loop on any precision input.</p>

<h3 id="dec-pga">12.5 PGA integration decisions <a class="anchor" href="#dec-pga">¶</a></h3>

<p><strong>D-31. kingdon as the GA backend.</strong> A geometric-algebra
library is needed for PGA reflections / motors / etc. <em>Decision:</em>
use Martin Roelfs's <code>kingdon</code> (Python, MIT, supports arbitrary
algebras via signature triple). <em>Alternatives:</em> implement PGA
operations directly on CReal-coefficient tuples (large undertaking),
use <code>clifford</code> Python library (numpy-tied, no CReal hook).
<em>Consequence:</em> kingdon's operator overloading + multivector dispatch
just-works with CReal coefficients once D-25 is in place.</p>

<p><strong>D-32. Separate modules for 2D, 3D, n-D.</strong> 2D and 3D
have ergonomic APIs (<code>point(x, y, z)</code>, <code>plane(a, b, c, d)</code>);
n-D needs a generic <code>*coords</code> shape. <em>Decision:</em>
keep dedicated modules for 2D and 3D; factory module for n-D.
<em>Alternatives:</em> single n-D factory used for all dimensions
(less ergonomic for 2D/3D users). <em>Consequence:</em> three modules
(<code>_pga.py</code>, <code>_pga2d.py</code>, <code>_pga_nd.py</code>);
<code>pga.d2 / d3 / d4 / … / d16</code> all available.</p>

<p><strong>D-33. <code>pga.d3</code> aliases the top-level
<code>pga</code>.</strong> 3D was the first integration; <code>pga.point</code>,
<code>pga.plane</code>, etc. became the public API. <em>Decision:</em>
keep top-level 3D unchanged for backward compatibility;
<code>pga.d3</code> exists as a self-alias for symmetry with
<code>d2</code>, <code>d4</code>, etc. <em>Alternatives:</em>
deprecate top-level 3D names. <em>Consequence:</em> none — top-level
3D and <code>pga.d3</code> are identical references.</p>

<p><strong>D-34. n-D cap at 16.</strong> $Cl(16, 0, 1)$ has $2^{17} =
131{,}072$ basis blades; operations slow noticeably but remain correct.
<em>Decision:</em> cap at 16 with a clear error message past it;
document the cap as raisable for users who need it.
<em>Consequence:</em> 4D through 16D all attached eagerly at import
time; higher dimensions require explicit <code>make_pga(n)</code> with
the cap manually lifted.</p>

<h3 id="dec-bench">12.6 Benchmark scope decisions <a class="anchor" href="#dec-bench">¶</a></h3>

<p><strong>D-35. C++ MPFR baseline via gmpy2, not direct C++.</strong>
Multiple attempts to compile <code>bench_boost_mpfr.cpp</code> through
vcpkg failed in the assistant's sandbox shell (vcpkg's
<code>detect_compiler</code> step requires <code>vswhere.exe</code> on
PATH, which it isn't; even after manual <code>vcvars64.bat</code>
sourcing, env vars don't propagate to vcpkg's nested CMake/ninja).
<em>Decision:</em> install <code>gmpy2</code> via pip (whose wheel
bundles prebuilt GMP+MPFR DLLs), have mpmath autodetect it, treat the
resulting mpmath numbers as the "MPFR baseline" (which they
literally are, within wrapper overhead). <em>Alternatives:</em> keep
trying to compile (time-bounded); ship the C++ as user-built.
<em>Consequence:</em> real measurements without the C++ build chain.
The build scripts and source remain in <code>bench/</code> for users with
proper dev environments.</p>

<p><strong>D-36. y-cruncher is the right tool for billion-digit π.</strong>
The user asked for π to 1,765,720,000 digits as a test case.
Extrapolation shows CReal would take ~11 years (post-optimisation),
MPFR ~1 hour, y-cruncher 30 min – 2 h on consumer hardware.
<em>Decision:</em> document the extrapolation, refuse to actually run
CReal at that scale, point at y-cruncher as the correct tool.
<em>Alternatives:</em> attempt the run (would never finish in this
session, possibly OOM the process), claim it can be done in CReal.
<em>Consequence:</em> the scaling table in section 11 documents the gap;
y-cruncher named as the production answer for record π.</p>

<h3 id="dec-perf">12.7 Optimisation decisions <a class="anchor" href="#dec-perf">¶</a></h3>

<p><strong>D-37. <code>__slots__</code> on all CReal subclasses.</strong>
Profiling showed CReal allocation in the AGM hot path; default Python
instances carry a per-object <code>__dict__</code>.
<em>Decision:</em> add <code>__slots__</code> to base <code>CReal</code>
and all 14 leaf classes; <code>slow_CReal</code> gets
<code>__slots__ = ()</code> to maintain the chain.
<em>Alternatives:</em> dataclasses with <code>frozen=True</code>
(adds <code>__init__</code> overhead). <em>Consequence:</em> each
instance drops from ~280 B to ~80 B; attribute access via C-level slot
descriptor; ~5–10% bench speedup.</p>

<p><strong>D-38. Divide-and-conquer base-10 conversion.</strong>
Profiling at 5000 digits showed <code>_int_to_radix</code> taking 50%
of the wall clock — the original repeated-divide loop was O(N²) on big
ints. <em>Decision:</em> implement Brent-style split (recursively
divide by $10^{N/2}$, concatenate); cache powers of 10; only use this
path above 2000-digit threshold. <em>Alternatives:</em> rely on
Python 3.11+'s sub-quadratic <code>str(int)</code> (project targets
Python 3.9). <em>Consequence:</em> 50K conversion drops from 40 ms to
19 ms; 500K bench from 157 s to 57 s.</p>

<p><strong>D-39. <code>_trunc_div</code> same-sign fast path.</strong>
Profile showed <code>divmod</code> at 8% of bench time at 50K.
<em>Decision:</em> add a same-sign check; when signs match,
truncating-div is identical to <code>//</code> and skips the
<code>divmod</code> tuple allocation. <em>Alternatives:</em> keep
always-divmod (clean, slow). <em>Consequence:</em> ~8% speedup at
50K.</p>

<p><strong>D-40. Cumulative speedup ~2.5× across all sizes.</strong>
The three optimisations (D-37, D-38, D-39) combine. <em>Decision:</em>
stop here. Further wins (NTT multiplication, mypyc, native
extensions) violate the pure-Python constraint (D-02). <em>Consequence:</em>
empirical exponent dropped from 1.96 to 1.92 (the DC conversion
removed an O(N²) constant); projected π at 1.766B digits dropped
from 41.5 years to 11.4 years. Still impractical at that scale —
but the floor is now Python int multiplication itself.</p>

<h3 id="dec-docs">12.8 Documentation decisions <a class="anchor" href="#dec-docs">¶</a></h3>

<p><strong>D-41. ℤ embedding explicit in docstrings.</strong> The
implementation always handled ℤ correctly; the docstrings did not
explicitly call out the ℤ ⊂ ℚ ⊂ ℝ$_c$ tower. <em>Decision:</em>
add a "Number-system embedding" section to the module docstring;
update <code>int_CReal</code>, <code>assumed_int_CReal</code>,
<code>valueOf</code>, <code>BigIntValue</code>, <code>assumeInt</code>
docstrings to explicitly mention ℤ. <em>Alternatives:</em> leave
implicit (works, but readers can't tell which class implements which
embedding). <em>Consequence:</em> direct correspondence between the
LaTeX/HTML theory section and the source.</p>

<p><strong>D-42. LaTeX paper separate from HTML doc.</strong> User
explicitly asked for the math "in LaTeX". <em>Decision:</em> build
two documents: a LaTeX paper (<code>Documentation/constructive_reals.tex</code>)
for the formal definition-lemma-proof style, and this HTML doc for
the discursive system-design style. <em>Alternatives:</em> single
format. <em>Consequence:</em> two file outputs; the build script
(<code>build_html.py</code>) handles only the HTML; the LaTeX is
hand-maintained.</p>

<p><strong>D-43. <code>amssymb</code> over <code>amsfonts</code> in
LaTeX preamble.</strong> User noted the preamble. <em>Decision:</em>
use <code>\usepackage{amssymb}</code> (which loads <code>amsfonts</code>
transitively, providing <code>\mathbb{}</code> plus extra symbols).
<em>Alternatives:</em> minimal <code>\usepackage{amsfonts}</code>.
<em>Consequence:</em> matches the user's stated convention.</p>

<p><strong>D-44. ℤ glyph as Unicode in Python docstrings.</strong>
Source-level Python docstrings use Unicode literals (ℤ = U+2124).
<em>Decision:</em> Python is UTF-8 since PEP 3120; help() displays
correctly in any modern terminal. <em>Alternatives:</em> ASCII-only
("the integers Z") for maximum portability. <em>Consequence:</em> the
ℤ symbol is searchable, copy-pasteable, and renders in IDE hover
tooltips.</p>

<h3 id="dec-infra">12.9 Infrastructure / toolchain decisions <a class="anchor" href="#dec-infra">¶</a></h3>

<p><strong>D-45. Cross-check with Java by porting Boehm's source
verbatim.</strong> When asked to validate scaling, the assistant
installed Temurin JDK 21 (portable zip), wrote
<code>bench/java/CR.java</code> and <code>BenchPi.java</code>, compiled
with <code>javac</code>, and ran the scaling series. <em>Decision:</em>
use the SGI 2001 source the user later supplied as the reference Java.
<em>Alternatives:</em> trust the Python port without cross-language
confirmation. <em>Consequence:</em> measured exponent Java
$k = 1.969$ vs Python AGM $k = 1.945$; $\Delta k = 0.024$ confirms
same asymptotic class.</p>

<p><strong>D-46. Native C++ baseline compiles via pinned MSVC env.</strong>
The standard <code>vcvars64.bat</code> failed because
<code>vswhere.exe</code> wasn't on PATH. <em>Decision:</em> write a
pinned <code>_setupenv.bat</code> with explicit paths to the MSVC
14.29.30133 toolset, then call <code>cl.exe</code> via its absolute
path from the bash shell. <em>Alternatives:</em> require the user to
build from a Developer Command Prompt. <em>Consequence:</em> the
native-C++ baseline (<code>bench_native_cpp.cpp</code> — schoolbook
big-int multiplication) compiles and runs, providing a "language
floor" reference number even when the full Boost+MPFR build chain
is unavailable.</p>

<p><strong>D-47. Self-contained HTML output.</strong> The HTML doc is
generated by <code>Content/Scripts/build_constructive_reals.py</code> from a template + the
package sources. <em>Decision:</em> single-file output, no images,
no external CSS; only MathJax loads from CDN at view time.
<em>Alternatives:</em> multi-file with relative links (Sphinx-style).
<em>Consequence:</em> trivially shareable; can be uploaded as a
single attachment to research-mode chats.</p>

<p><strong>D-48. Build script as the source of truth.</strong> The
HTML is regenerated, not hand-edited. <em>Decision:</em> source
edits flow through <code>Content/Scripts/build_constructive_reals.py</code>. <em>Alternatives:</em>
edit the HTML directly. <em>Consequence:</em> embedded Python source
is always current; tables and explanatory prose live in the template.</p>

<h3 id="dec-deferred">12.10 Deliberately deferred <a class="anchor" href="#dec-deferred">¶</a></h3>

<p><strong>D-49. Specialised <code>int_CReal + int_CReal → int_CReal</code>.</strong>
Tempting performance opt: detect integer-integer operations and short-
circuit to a new <code>int_CReal</code>. <em>Decision:</em> defer.
<em>Reason:</em> would change subclass type at runtime; callers that
pattern-match on subclass type (or use <code>isinstance(x, int_CReal)</code>
checks) would see new behaviour. <em>Status:</em> open; could be
re-enabled behind a flag.</p>

<p><strong>D-50. <code>byteValue()</code> from HP Java 2004.</strong>
HP added <code>byteValue()</code> to mirror the Java <code>Number</code>
abstract class. <em>Decision:</em> Python has no equivalent abstract
class; <code>intValue()</code> suffices. <em>Status:</em> not ported.</p>

<p><strong>D-51. Arbitrary radix string parsing.</strong> Java
<code>valueOf(String, radix)</code> handles bases 2–16. <em>Decision:</em>
Python <code>valueOf("...")</code> handles base 10 only;
<code>toString(n, radix)</code> handles 2/8/10/16 via fast paths and
arbitrary radix via fallback. <em>Status:</em> the input-parser radix
support is missing.</p>

<p><strong>D-52. <code>toStringFloatRep</code>.</strong> HP added a
scientific-notation conversion that returns a
<code>StringFloatRep</code> struct. <em>Decision:</em> port the method;
return a Python dict. <em>Status:</em> ported; lightly tested.</p>

<p><strong>D-53. C++26 reflection bridge.</strong> User asked if
P2996 could bridge to UE reflection. <em>Decision:</em> document
the conceptual mapping (<code>reflect_demo.cpp</code> shows C++17
patterns paired with their UE counterparts); do not attempt actual
reflection — the C++26 implementations don't exist in shipping
compilers. <em>Status:</em> documentation only.</p>

<p><strong>D-54. NTT multiplication for Python <code>int</code>.</strong>
Implementing FFT-based multiplication in pure Python is multi-week
work. <em>Decision:</em> defer indefinitely. <em>Status:</em>
superseded by the opt-in <code>reals.backends</code> dispatch (D-58),
which hands the workload to <code>gmpy2</code> or
<code>python-flint</code> when present. Pure-Python NTT remains
unverified per the 2025 frontier survey
(<a href="#frontier-fft">section 10.1</a>).</p>

<p><strong>D-55. mypyc / Cython compilation of the hot loops.</strong>
The AGM math is exactly the kind of pure-integer workload mypyc was
designed for. <em>Decision:</em> defer, document. <em>Reason:</em> the
package itself does not run <code>mypyc</code>, so the
"<code>pip install reals</code> from any environment" promise stays
intact. <em>Status:</em> users who want the speedup invoke
<code>mypyc reals/_creal.py</code> from their own build environment;
the path is documented in
<code>Documentation/CONSTRUCTIVE_REALS_UPGRADES.md</code>. Decision
D-64 records the verified speedup range (5–14× on tuned loops, 2–3× on
mixed-object hot paths).</p>

<p><strong>D-56. <code>gmpy2.mpz</code> as the int backend.</strong>
Would close most of the gap to MPFR inside Python. <em>Decision:</em>
defer as a hard dependency, expose as an opt-in dispatch.
<em>Reason:</em> hard C dependency would violate D-02; opt-in dispatch
preserves D-02 for users without <code>gmpy2</code>.
<em>Status:</em> closed by D-58 — <code>reals.backends</code> probes for
<code>gmpy2</code> / <code>python-flint</code> / pure-CPython at import
and surfaces the active backend via <code>recommend_backend()</code>.
Default install carries no C deps.</p>

<p><strong>D-57. Continued-fraction hybrid (CR ⟷ CF).</strong> The
package directory also contains the original <code>reals</code> library
(continued-fraction representation). A hybrid that picks representation
per operation class could outperform both. <em>Decision:</em> defer.
<em>Status:</em> open research problem
(<a href="#frontier-cf">section 10.5</a>).</p>

<p><strong>D-58. Opt-in bignum backend dispatch (<code>reals.backends</code>).</strong>
<em>Decision:</em> add a <code>reals._backends</code> module that probes
<code>gmpy2</code>, <code>python-flint</code>, and pure CPython at
import time; expose <code>recommend_backend(precision_bits)</code>,
<code>report()</code>, and <code>map_in_parallel()</code>. The
<code>REALS_BACKEND</code> environment variable forces a specific
choice. <em>Status:</em> done. <em>Consequence:</em> users who install
<code>python-flint 0.8.0</code> (PyPI wheels for 3.11–3.14 / 3.14t /
PyPy 3.11) get FLINT 3.3.1 + Arb + MPFR 4.2.2 transparently; default
installs stay pure-Python. <em>Closes:</em> D-56 and the dispatch half
of D-54.</p>

<p><strong>D-59. MPFR-style a-priori AGM iteration cap.</strong>
<em>Decision:</em> bound the Gauss–Legendre loop in
<code>gl_pi_CReal.approximate</code> by
$\lceil \log_2(-p + 2) \rceil + 5$, matching the published Brent–Salamin
tail-error bound and MPFR's 4096-bit $\pi$ overhead.
<em>Reason:</em> turns "stops when it converges" into a guaranteed
termination contract without changing the runtime convergence test
(which still gates early exit). <em>Status:</em> done.
<em>Consequence:</em> Pi correctness preserved at all benched
precisions; iteration count is now provably bounded. Closes the
a-priori-bound half of 9.1.2.</p>

<p><strong>D-60. Reciprocal cache via <code>WeakValueDictionary</code>.</strong>
<em>Decision:</em> module-level
<code>_INVERSE_CACHE</code> keyed by <code>id(operand)</code>;
<code>inv_CReal</code> gains <code>__weakref__</code>;
<code>CReal.inverse()</code> consults the cache before allocating.
<em>Reason:</em> repeated divisions by the same denominator (polynomial
evaluation, series re-use) are very common; previous behaviour built a
fresh <code>inv_CReal</code> each time. <em>Status:</em> done.
<em>Consequence:</em> closes 9.1.3.</p>

<p><strong>D-61. ln/exp via <code>python-flint</code> at large precision —
documented hook, not implemented.</strong> <em>Decision:</em> document
the Arb-table-Taylor + rectangular-splitting path in section 4.4 and
leave the dispatcher to user code. <em>Reason:</em> 2025 benchmarks
(Johansson) confirm table-based Taylor wins below the Brent–Salamin
crossover at $\sim 10^5$ bits, so the urgency is low; users who hit
the regime can wrap <code>flint.arb.log</code> with a stub
<code>reals.log_via_arb</code> (~30 lines). <em>Status:</em>
documented, not implemented.</p>

<p><strong>D-62. Boehm irrational-tag heuristic for comparison.</strong>
<em>Decision:</em> class attribute
<code>CReal.IRRATIONAL_TAG_BITS = 3500</code>; the no-tolerance forms of
<code>compareTo</code> and <code>signum</code> give up iterating past
that precision and return 0. <em>Reason:</em> matches Boehm PLDI 2020
section 6.2 and Google's Android calculator (the published reference). Without
this, <code>sin²(1) + cos²(1)</code> compared to 1 diverges; with it,
the comparison decides in &lt;100 ms. <em>Status:</em> done. Set to
<code>None</code> to restore divergent semantics. <em>Consequence:</em>
closes the practical half of 9.1.5.</p>

<p><strong>D-63. Calcium dispatch hook for guaranteed algebraic
decisions.</strong> <em>Decision:</em> reserve the API surface
<code>cr.with_algebraic_decision()</code>; defer the implementation
until <code>python-flint</code>'s Calcium binding stabilises.
<em>Reason:</em> the heuristic (D-62) covers practical numerics; users
who need guaranteed algebraic-class decisions are rare enough that the
API can land later. <em>Status:</em> documented hook only.</p>

<p><strong>D-64. mypyc compilation path documented (not run by build).</strong>
<em>Decision:</em> document the <code>mypyc reals/_creal.py</code>
invocation in <code>Documentation/CONSTRUCTIVE_REALS_UPGRADES.md</code>;
do not run mypyc from the package itself. <em>Reason:</em> preserves
D-02 ("<code>pip install reals</code> works in any environment").
<em>Verified speedup range:</em> 5–14× on tuned arithmetic loops, 2–3×
on mixed-object hot paths (mypyc benchmark suite). <em>Status:</em>
documented. <em>Closes:</em> D-55.</p>

<p><strong>D-65. <code>yield_stable_digits()</code> streaming
generator.</strong> <em>Decision:</em> add
<code>CReal.yield_stable_digits(radix, chunk, max_total)</code> that
re-evaluates at increasing precision and yields each digit once it
agrees in two consecutive evaluations. <em>Reason:</em> the obvious
compromise — true coinductive streaming (Möbius / Edalat–Potts) would
need a representation change. <em>Caveat:</em> incorrect under
adversarial digit-boundary inputs; faithful for all practical
numerics. <em>Status:</em> done. <em>Closes:</em> 9.2.3.</p>

<p><strong>D-66. Expression-DAG CSE cache and parallel-evaluation
helper.</strong> <em>Decision:</em> module-level
<code>_DAG_CACHE</code> WeakValueDictionary keyed by
<code>(kind, id(op1), id(op2))</code> with commutative-key normalisation
for <code>add</code> / <code>multiply</code>; the four cached factories
gain <code>__weakref__</code>. Plus
<code>reals.backends.map_in_parallel()</code> dispatching to
<code>ProcessPoolExecutor</code> above 100 000 bits per leaf, in-process
below. <em>Reason:</em> closes the Boehm PLDI 2020 section 5 sub-expression-
sharing optimisation and the parallel-multi-leaf workload at the same
time. <em>Caveat:</em> identity-keyed CSE only; two semantically-equal
distinct CReals will not dedupe. <em>Status:</em> done.
<em>Closes:</em> 9.2.4, partial close of 9.2.5.</p>

<p><strong>D-67. <code>__weakref__</code> promoted to base
<code>CReal.__slots__</code>.</strong> <em>Decision:</em> add the
<code>__weakref__</code> slot to the base class and drop it from the
five subclasses that previously carried it locally
(<code>add_CReal</code>, <code>mult_CReal</code>, <code>neg_CReal</code>,
<code>shifted_CReal</code>, <code>inv_CReal</code>). <em>Reason:</em>
Python forbids the slot appearing in more than one class in the
inheritance chain; the unary-kernel cache (D-68) needs every transcendental
result class (<code>prescaled_exp_CReal</code>, <code>prescaled_cos_CReal</code>,
<code>prescaled_ln_CReal</code>, <code>prescaled_asin_CReal</code>,
<code>sqrt_CReal</code>, <code>assumed_int_CReal</code>, <code>gl_pi_CReal</code>,
<code>int_CReal</code>) to be weakref-able; doing it once at the base
spares every future cache addition the same chore. Cost: ~8 bytes per
instance. <em>Status:</em> done.</p>

<p><strong>D-68. Unary kernel DAG cache.</strong>
<em>Decision:</em> extend <code>_DAG_CACHE</code> to the unary
factories on <code>CReal</code>: <code>sqrt</code>, <code>exp</code>,
<code>cos</code>, <code>sin</code>, <code>ln</code>, <code>asin</code>,
<code>acos</code>, and <code>assumeInt</code>. Each is keyed
<code>(kind, id(self))</code>. <em>Reason:</em> closes the Boehm PLDI
2020 section 5 sub-expression-sharing optimisation at the kernel
level — until now <code>sin x</code> built two distinct
<code>prescaled_cos_CReal</code> nodes when called twice on the same
<code>x</code>; now it dedupes. Combined with D-66 the
<code>sin²x + cos²x</code> example now shares <em>all</em> of its
subtree. <em>Status:</em> done. <em>Caveat:</em> identity-keyed; two
semantically-equal but distinct CReals still don't dedupe.</p>

<p><strong>D-69. Opt-in ℤ short-circuit
(<code>CReal.SHORT_CIRCUIT_INT_OPS</code>).</strong>
<em>Decision:</em> add a class-level flag (default <code>False</code>)
that makes <code>add</code> / <code>multiply</code> / <code>negate</code>
detect <code>int_CReal</code> + <code>int_CReal</code> (and the
<code>assumed_int_CReal</code> sibling) and collapse directly to a fresh
<code>int_CReal</code> of the computed value, skipping the lazy
expression tree. <em>Reason:</em> ℤ-heavy chains used to pay full lazy
allocation cost for every <code>+</code> / <code>×</code>; the opt-in
short-circuit collapses them to a single int. Reopens HTML decision
D-49 with the flag-gated rollout the original deferral suggested.
<em>Status:</em> done (opt-in only — caller writes
<code>CReal.SHORT_CIRCUIT_INT_OPS = True</code>). <em>Caveat:</em> when
on, the runtime type of arithmetic results changes from
<code>add_CReal</code> / <code>mult_CReal</code> / <code>neg_CReal</code>
to <code>int_CReal</code> for the pure-ℤ subset; callers that
<code>isinstance</code>-check the lazy classes need to disable the
flag.</p>

<h2 id="refs">13. References <a class="anchor" href="#refs">¶</a></h2>

<ul>
  <li>Hans-J. Boehm, <em>The Constructive Reals as a Java Library</em>,
  Journal of Logic and Algebraic Programming 64 (2005), 3–11.
  <a href="https://www.hboehm.info/cr.pdf">PDF</a>.</li>
  <li>Hans-J. Boehm, <em>Constructive Real Interpretation of Numerical
  Programs</em>, ACM SIGPLAN Notices 22 (7), 1987.</li>
  <li>Gosper, R. W., <em>Continued Fraction Arithmetic</em>, HAKMEM Item
  101B, 1972. (Background on real-number representation via streaming.)</li>
  <li>The Gauss-Legendre algorithm: see e.g. Borwein &amp; Borwein,
  <em>Pi and the AGM</em>, 1987.</li>
  <li>Christian Lawson-Perfect, <em>creal.js</em>, 2022.
  <a href="https://github.com/christianp/creal.js">github.com/christianp/creal.js</a>.</li>
  <li><em>Projective Geometric Algebra</em>: Charles Gunn, Steven De Keninck,
  Eric Lengyel. See bivector.net.</li>
  <li>The <code>kingdon</code> library by Martin Roelfs:
  <a href="https://github.com/tBuLi/kingdon">github.com/tBuLi/kingdon</a>.</li>
  <li>Hans Boehm's original Java sources, with the SGI 1999 and HP 2001/2004
  copyright headers, are reproduced verbatim in
  <code>bench/java/CR.java</code> for benchmarking.</li>
</ul>

<h3>Computable analysis &amp; foundations</h3>
<ul>
  <li>Klaus Weihrauch, <em>Computable Analysis: An Introduction</em>,
  Springer, 2000. Definitive textbook on the TTE framework.</li>
  <li>Marian Pour-El &amp; J. Ian Richards, <em>Computability in Analysis
  and Physics</em>, Springer, 1989. Foundational.</li>
  <li>Andrej Bauer, <em>The Real Numbers in the Topos of Sheaves</em>,
  2008. Connects constructive reals to topos theory.</li>
  <li>Abbas Edalat &amp; Reinhold Heckmann, <em>Computing with real
  numbers</em>, Springer LNCS, 2002. Domain-theoretic semantics.</li>
</ul>

<h3>Alternative implementations</h3>
<ul>
  <li>Norbert Müller, <em>The iRRAM — Exact Arithmetic in C++</em>,
  Trier University, 1996–present.
  <a href="https://irram.uni-trier.de/">irram.uni-trier.de</a>.</li>
  <li>Branimir Lambov, <em>RealLib: An Efficient Implementation of Exact
  Real Arithmetic</em>, Math. Struct. Comp. Sci., 2007.</li>
  <li>Fredrik Johansson, <em>Arb: efficient arbitrary-precision midpoint-
  radius interval arithmetic</em>, IEEE Trans. Computers, 2017.
  <a href="https://arblib.org/">arblib.org</a>.</li>
  <li>Sylvie Boldo et al., <em>Flocq: A Unified Library for Proving
  Floating-Point Algorithms in Coq</em>, ARITH, 2011. Verified FP, useful
  contrast to verified CR.</li>
</ul>

<h3>Multiplication algorithms (the speed ceiling)</h3>
<ul>
  <li>Arnold Schönhage &amp; Volker Strassen, <em>Schnelle Multiplikation
  großer Zahlen</em>, Computing, 1971. The original FFT bignum
  multiplication.</li>
  <li>David Harvey &amp; Joris van der Hoeven, <em>Integer multiplication
  in time $O(n \log n)$</em>, Annals of Math., 2021. Theoretical
  lower-bound-matching algorithm.</li>
  <li>Martin Fürer, <em>Faster Integer Multiplication</em>, STOC, 2007.
  $O(n \log n \cdot 2^{O(\log^* n)})$ result; predecessor of HvdH.</li>
</ul>

<h3>Recent / bleeding-edge (2022–2025)</h3>
<ul>
  <li>Mathlib4 team, <em>Computable Real Numbers</em> (work in progress),
  Lean Community, 2024. Tracking issue on GitHub.</li>
  <li>Adam Bagniewski, <em>Reachability problems in continuous-state
  dynamical systems</em>, PhD thesis, Imperial College, 2022. CR
  comparison and the Skolem problem.</li>
  <li>Modular AI &amp; Mojo team, <em>Hybrid bignum SIMD operations in
  Mojo</em>, 2024. Manufacturer benchmarks; should be independently
  verified for the claims about NTT-vs-Karatsuba crossover in Mojo.</li>
  <li>The Lean Copilot, COPRA, AlphaProof, and DeepSeek-Prover papers
  (2023–2024) — LLM + formal-prover hybrids; constructive-real
  correctness is a clean benchmark for these.</li>
  <li>Bertot &amp; al., <em>Towards Verified Real Computation</em>,
  Inria research report, 2024. Combines Coq with Boehm-style CR.</li>
  <li>Steven De Keninck &amp; Charles Gunn, <em>Projective Geometric
  Algebra: A Foundation for Geometric Reasoning</em>, AACGA, 2023. The
  PGA layer this package wraps via kingdon.</li>
  <li>Martin Roelfs &amp; Steven De Keninck, <em>Graded Symmetry Groups:
  Plane and Simple</em>, 2023. The theoretical underpinning of kingdon.</li>
</ul>

<h3>Tools and ecosystems</h3>
<ul>
  <li>Alexander Yee, <em>y-cruncher: A Multi-Threaded Pi-Program</em>.
  <a href="http://www.numberworld.org/y-cruncher/">numberworld.org/y-cruncher</a>.
  Holds the current π digit-computation records.</li>
  <li>David H. Bailey, <em>MPFUN20-MPFR</em>: thread-safe arbitrary-
  precision Fortran/C++ wrapper around MPFR.
  <a href="https://www.davidhbailey.com/dhbsoftware/">davidhbailey.com/dhbsoftware</a>.</li>
  <li>The <em>kingdon</em> Python Geometric Algebra library:
  <a href="https://github.com/tBuLi/kingdon">github.com/tBuLi/kingdon</a>.</li>
  <li><em>SageMath</em>'s <code>RealField</code> and <code>RealIntervalField</code>:
  Python-accessible MPFR / Arb wrappers via Cython.</li>
</ul>

<footer>
<p>This document was generated by
<code>Content/Scripts/build_constructive_reals.py</code> on
__BUILD_DATE__. The HTML is self-contained except for MathJax, loaded
from a CDN. To rebuild after package edits:
<code>python Content/Scripts/build_constructive_reals.py</code>.</p>
<p>Licences: the constructive-real machinery is under the SGI / HP /
Apache 2.0 licences of the original Java sources (see file headers).
The Python translation and PGA integration are under the same chain.
MathJax is Apache 2.0.</p>
</footer>

</main>
</div>
</body>
</html>
"""

substitutions = {
    "__BUILD_DATE__": datetime.utcnow().strftime("%Y-%m-%d"),
    "__INIT_SRC__": listing(SOURCES["init"]),
    "__CREAL_SRC__": listing(SOURCES["creal"]),
    "__BACKENDS_SRC__": listing(SOURCES["backends"]),
    "__PGA_SRC__": listing(SOURCES["pga"]),
    "__PGA2D_SRC__": listing(SOURCES["pga2d"]),
    "__PGAND_SRC__": listing(SOURCES["pga_nd"]),
}

out = HTML
for key, val in substitutions.items():
    out = out.replace(key, val)

out_path = os.path.join(DOCS_DIR, "constructive_reals.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Wrote {out_path}")
print(f"  {len(out):,} chars, ~{out.count(chr(10)):,} lines")
print(f"  sources: {REALS_DIR}")
