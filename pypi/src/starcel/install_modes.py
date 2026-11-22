"""Auto vs manual install orchestration.

Auto runs every step silently. Manual writes an HTML guide to the Desktop and
opens it in the default browser, listing every dependency URL and click-through
step. The user does the clicks; nothing is installed automatically.
"""
from __future__ import annotations

import importlib.resources
import os
import webbrowser
from pathlib import Path

from . import config, donations, env, firewall, prereqs, shortcuts
from . import vs_installer, ue_source


def _step(label: str, func) -> None:
    """Run one install step; report failures without aborting the remaining steps."""
    try:
        func()
    except Exception as exc:
        print(f"Warning: {label} failed: {exc}")
        print(f"  You can retry later; see `starcel install --manual` for the manual steps.")


def auto_install() -> None:
    """Run every enabled silent-install step in order."""
    donations.print_start()
    if config.INSTALL_PREREQS:
        _step("UE4 prerequisites", prereqs.install_ue4_prereqs)
    if config.INSTALL_SHORTCUTS:
        _step("shortcuts", shortcuts.create_all)
    if config.INSTALL_ENV_VARS:
        _step("environment variables", env.install_all)
    if config.INSTALL_FIREWALL_RULE:
        _step("firewall rule", firewall.add_rule)
    donations.print_end()


def auto_install_dev(ue_target_dir: Path | None = None) -> None:
    """Dev flow: VS 2019 + UE4.27-chaos from source."""
    donations.print_start()
    vs_installer.install_vs2019()
    ue_source.install_ue_source(ue_target_dir)
    print("\nReminder: to run the packaged game, also install the build:")
    print("  starcel install")
    donations.print_end()


def manual_install() -> None:
    """Write an HTML guide to the Desktop and open it in the browser."""
    guide_html = _render_manual_guide()
    output = config.SHORTCUT_DESKTOP_DIR / "Starcel-Install-Guide.html"
    output.write_text(guide_html, encoding="utf-8")
    print(f"Manual guide written to: {output}")
    try:
        webbrowser.open(output.as_uri())
    except Exception:
        os.startfile(str(output))


def _render_manual_guide() -> str:
    template_text = _read_template("manual_instructions.md")
    body_sections = [
        ("UE4 prerequisites (VC++ + DirectX)", prereqs.manual_instructions()),
        ("Desktop & Start Menu shortcuts", shortcuts.manual_instructions()),
        ("Environment variables & long paths", env.manual_instructions()),
        ("Firewall rule for dedicated server", firewall.manual_instructions()),
        ("Visual Studio 2019 (dev only)", vs_installer.manual_instructions()),
        ("UE4.27-chaos from source (dev only)", ue_source.manual_instructions()),
    ]

    sections_html = "\n".join(
        f'<section><h2>{title}</h2><pre>{_escape(body)}</pre></section>'
        for title, body in body_sections
    )

    donation_html = (
        "<div class='donate'>"
        + " &nbsp;|&nbsp; ".join(
            f'<a href="{url}">{name}</a>' for name, url in config.DONATION_URLS.items()
        )
        + "</div>"
    )

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Starcel Install Guide</title>
<style>
  body {{ font: 15px/1.5 system-ui, sans-serif; max-width: 820px; margin: 40px auto; padding: 0 20px; color: #222; }}
  h1 {{ border-bottom: 2px solid #333; padding-bottom: 8px; }}
  h2 {{ margin-top: 36px; color: #2a5a9a; }}
  pre {{ background: #f4f4f8; padding: 12px 16px; border-radius: 6px; white-space: pre-wrap; word-wrap: break-word; }}
  .donate {{ margin: 24px 0; padding: 16px; background: #fff8e1; border-left: 4px solid #f5b700; border-radius: 4px; }}
  .donate a {{ color: #2a5a9a; text-decoration: none; font-weight: 600; }}
  section {{ margin-bottom: 24px; }}
</style></head><body>
<h1>Starcel Install Guide</h1>
{donation_html}
<p>{_escape(template_text)}</p>
{sections_html}
{donation_html}
</body></html>"""


def _read_template(name: str) -> str:
    try:
        return importlib.resources.files(__package__).joinpath("templates", name).read_text(encoding="utf-8")
    except (FileNotFoundError, AttributeError):
        return ""


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )
