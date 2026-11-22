"""Donation banner — shown at the start and end of every install flow."""
from __future__ import annotations

from . import config


def _banner(title: str) -> str:
    width = 68
    urls = list(config.DONATION_URLS.items())
    inner_width = width - 2
    lines = [f"+{'-' * inner_width}+"]
    lines.append(f"| {title:<{inner_width - 2}} |")
    lines.append(f"|{' ' * inner_width}|")
    for name, url in urls:
        entry = f"  {name}: {url}"
        lines.append(f"| {entry:<{inner_width - 2}} |")
    lines.append(f"+{'-' * inner_width}+")
    return "\n".join(lines)


def print_start() -> None:
    print(_banner("Thanks for installing Starcel — consider supporting:"))


def print_end() -> None:
    print(_banner("Install complete! If Starcel is useful to you, support:"))


def print_line() -> None:
    urls = ", ".join(f"{name}: {url}" for name, url in config.DONATION_URLS.items())
    print(f"Support development — {urls}")
