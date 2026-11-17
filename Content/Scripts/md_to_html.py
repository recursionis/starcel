"""Convert Markdown files in Documentation/ to standalone HTML.

Wraps the generated body in CSS / typography that matches
``constructive_reals.html`` so the converted docs sit naturally next to
the long-form HTML in the same folder.

Usage from anywhere on the project:

    # Convert one file
    python Content/Scripts/md_to_html.py Documentation/ND_TABLE_REALS_UPGRADE.md

    # Convert all .md files under Documentation/ (skipping anything
    # whose .html sibling is newer than the .md source)
    python Content/Scripts/md_to_html.py --all

    # Force re-render even when the sibling .html is up to date
    python Content/Scripts/md_to_html.py --all --force

Output goes to the same directory as the input, with extension
``.html``. The script does NOT touch any pre-existing hand-authored HTML
in ``Documentation/`` — it only writes files whose base name matches a
``.md`` source.

Pure Python; depends on ``markdown >= 3.4`` (auto-installed in the same
``pip install markdown`` line you used for the rest of this project).
The HTML is self-contained except for MathJax, which loads from a CDN
at view time (matching the convention in ``constructive_reals.html``).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from html import escape
from pathlib import Path

try:
    import markdown
except ImportError as e:
    print(
        "ERROR: python-markdown is not installed.\n"
        "  pip install markdown\n",
        file=sys.stderr,
    )
    raise SystemExit(1) from e


HERE = Path(__file__).resolve().parent


def find_documentation_dir() -> Path:
    """Walk up from this script's location to find the project root —
    the directory that has both a ``Content`` and a ``Documentation``
    sibling — and return the path to ``Documentation/``.
    """
    p = HERE
    for _ in range(6):
        cand = p / "Documentation"
        if cand.is_dir() and (p / "Content").is_dir():
            return cand
        if p.parent == p:
            break
        p = p.parent
    raise FileNotFoundError(
        f"Could not find project-root Documentation/ folder "
        f"starting from {HERE}."
    )


DOCS_DIR = find_documentation_dir()


# ---- HTML chrome -------------------------------------------------------
# CSS palette copied verbatim from constructive_reals.html so the
# converted docs sit alongside it visually.

CSS = r"""
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
  .layout { max-width: 1100px; margin: 0 auto; padding: 32px 50px 80px 50px; }
  h1 { font-size: 2.0em; margin: 0 0 0.2em 0; color: var(--accent); letter-spacing: -0.01em; }
  h2 { margin-top: 2.0em; padding-bottom: 0.2em; border-bottom: 2px solid var(--accent); color: var(--accent); font-size: 1.45em; }
  h3 { margin-top: 1.6em; color: var(--accent2); font-size: 1.15em; }
  h4 { margin-top: 1.3em; font-size: 1.02em; }
  p, ul, ol { margin: 0.65em 0; }
  a { color: var(--accent); text-decoration: none; }
  a:hover { color: var(--accent2); text-decoration: underline; }
  code {
    font-family: "JetBrains Mono", "Fira Code", Menlo, Consolas, monospace;
    font-size: 0.88em;
    background: var(--code-bg);
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid var(--code-border);
  }
  pre {
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 4px;
    padding: 16px 18px;
    overflow-x: auto;
    font-size: 0.86em;
    line-height: 1.4;
    margin: 1em 0;
  }
  pre code { background: none; border: none; padding: 0; font-size: 1em; }
  blockquote {
    border-left: 3px solid var(--accent2);
    padding-left: 16px;
    color: var(--muted);
    margin: 1em 0;
    font-style: italic;
  }
  table { border-collapse: collapse; margin: 1em 0; font-size: 0.93em; }
  th, td { border: 1px solid var(--rule); padding: 6px 12px; text-align: left; }
  th { background: var(--side); }
  td.num { text-align: right; font-variant-numeric: tabular-nums; font-family: "JetBrains Mono", Menlo, monospace; }
  hr { border: none; border-top: 1px solid var(--rule); margin: 2.5em 0; }
  .meta { color: var(--muted); font-size: 0.92em; margin: 0.3em 0 1.5em 0; }
  .toc { background: var(--side); border: 1px solid var(--rule); border-radius: 4px; padding: 14px 20px; margin: 1em 0 2em 0; font-size: 0.94em; }
  .toc > ul { padding-left: 20px; margin: 0; }
  .toc > ul ul { padding-left: 20px; }
  .toc a { color: var(--fg); }
  .toc a:hover { color: var(--accent2); }
  footer { margin-top: 4em; padding-top: 1.5em; border-top: 1px solid var(--rule); color: var(--muted); font-size: 0.85em; }
  @media (max-width: 760px) { .layout { padding: 20px; } }
"""


PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>
  MathJax = {{
    tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
           displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }}
  }};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>{css}</style>
</head>
<body>
<div class="layout">
{body}
<footer>
<p>Generated by <code>Content/Scripts/md_to_html.py</code> from
<code>{source_rel}</code> on {build_date}. Re-run after edits with
<code>python Content/Scripts/md_to_html.py {source_rel}</code>.</p>
</footer>
</div>
</body>
</html>
"""


# Markdown extensions to enable — chosen for the kinds of constructs the
# upgrade docs use (tables, fenced code, footnotes, sane lists, TOC).
MD_EXTENSIONS = [
    "extra",         # rolls in tables, fenced_code, footnotes, attr_list, def_list, abbr
    "sane_lists",    # don't merge ordered + unordered lists
    "toc",           # auto-generated table of contents via [TOC]
    "smarty",        # smart quotes / dashes
]

MD_EXT_CONFIGS = {
    "toc": {
        "title": "Contents",
        "anchorlink": False,
        "permalink": False,
        "toc_depth": "2-4",
    },
}


def derive_title(md_path: Path, body_html: str) -> str:
    """Pick the document title from the first ``# H1`` in the source."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    return md_path.stem


def convert_one(md_path: Path, out_path: Path, force: bool = False) -> bool:
    """Convert ``md_path`` to ``out_path``. Returns True if a file was written."""
    if (
        not force
        and out_path.exists()
        and out_path.stat().st_mtime >= md_path.stat().st_mtime
    ):
        return False
    md_src = md_path.read_text(encoding="utf-8")
    md = markdown.Markdown(
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXT_CONFIGS,
        output_format="html5",
    )
    body_html = md.convert(md_src)
    title = derive_title(md_path, body_html)
    page = PAGE_TEMPLATE.format(
        title=escape(title),
        css=CSS,
        body=body_html,
        source_rel=md_path.relative_to(DOCS_DIR.parent).as_posix(),
        build_date=datetime.utcnow().strftime("%Y-%m-%d"),
    )
    out_path.write_text(page, encoding="utf-8")
    return True


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "paths",
        nargs="*",
        help="Markdown files to convert. If omitted, use --all.",
    )
    p.add_argument(
        "--all",
        action="store_true",
        help=f"Convert every .md under {DOCS_DIR}.",
    )
    p.add_argument(
        "--force",
        action="store_true",
        help="Re-render even when the sibling .html is newer than the .md.",
    )
    args = p.parse_args(argv)

    if not args.paths and not args.all:
        p.error("Specify at least one .md path, or pass --all.")

    if args.all:
        md_paths = sorted(DOCS_DIR.glob("*.md"))
    else:
        md_paths = [Path(p).resolve() for p in args.paths]
        for path in md_paths:
            if not path.exists():
                print(f"ERROR: not found: {path}", file=sys.stderr)
                return 2

    if not md_paths:
        print(f"No .md files found under {DOCS_DIR}.", file=sys.stderr)
        return 1

    wrote = 0
    skipped = 0
    for md_path in md_paths:
        out_path = md_path.with_suffix(".html")
        if convert_one(md_path, out_path, force=args.force):
            print(f"  wrote {out_path}")
            wrote += 1
        else:
            print(f"  skipped {out_path} (up-to-date; pass --force to rebuild)")
            skipped += 1

    print(f"Done. {wrote} written, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
