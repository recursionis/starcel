"""Windows Firewall rule for the Starcel dedicated server (TCP/UDP 7827)."""
from __future__ import annotations

import subprocess

from . import config


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def rule_exists() -> bool:
    result = _run([
        "netsh", "advfirewall", "firewall", "show", "rule",
        f"name={config.FIREWALL_RULE_NAME}",
    ])
    return "No rules match" not in result.stdout and result.returncode == 0


def add_rule() -> None:
    if not config.INSTALL_FIREWALL_RULE:
        return
    if rule_exists():
        print(f"Firewall rule '{config.FIREWALL_RULE_NAME}' already exists — skipping.")
        return

    for protocol in ("TCP", "UDP"):
        result = _run([
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={config.FIREWALL_RULE_NAME}",
            "dir=in",
            "action=allow",
            f"protocol={protocol}",
            f"localport={config.FIREWALL_PORT}",
        ])
        if result.returncode != 0:
            print(
                f"Skipped firewall rule (needs an administrator terminal; only required to host "
                f"a dedicated server): {(result.stderr or result.stdout).strip()}"
            )
            return
    print(f"Firewall rule added for {config.FIREWALL_RULE_NAME} on port {config.FIREWALL_PORT} (TCP + UDP).")


def remove_rule() -> None:
    _run([
        "netsh", "advfirewall", "firewall", "delete", "rule",
        f"name={config.FIREWALL_RULE_NAME}",
    ])


def manual_instructions() -> str:
    return (
        f"Open 'Windows Defender Firewall with Advanced Security' → Inbound Rules → "
        f"New Rule → Port → TCP → Specific local ports: {config.FIREWALL_PORT} → Allow → "
        f"Name: {config.FIREWALL_RULE_NAME}. Repeat for UDP."
    )
