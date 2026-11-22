"""Silent install of the UE4.27 prerequisites.

UE4PrereqSetup_x64.exe ships bundled with every UE4.27 packaged game under
Engine/Extras/Redist/en-us/. It's an InstallShield wrapper that internally
installs VC++ Redistributable 2015-2022 + DirectX End-User Runtime. The
/install /quiet /norestart flags make it fully unattended.
"""
from __future__ import annotations

import subprocess
import winreg

from . import paths


def vc_redist_2015_2022_installed() -> bool:
    """True if VC++ 2015-2022 x64 runtime is already registered.

    Skipping the UE prereq installer when redist is already present saves ~30s
    on repeat installs.
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
        ) as k:
            installed, _ = winreg.QueryValueEx(k, "Installed")
            return bool(installed)
    except OSError:
        return False


def install_ue4_prereqs(*, force: bool = False) -> None:
    """Run UE4PrereqSetup_x64.exe silently. Skips if VC++ redist already installed."""
    if not force and vc_redist_2015_2022_installed():
        print("VC++ 2015-2022 redistributable already installed — skipping UE4 prereqs.")
        return

    installer = paths.prereq_installer()
    if not installer.exists():
        raise FileNotFoundError(
            f"UE4PrereqSetup_x64.exe not found at {installer}. The packaged build may not be "
            "installed yet — run `starcel install` first."
        )

    print(f"Running {installer.name} silently (Windows may ask for administrator permission)...")
    try:
        result = subprocess.run(
            [str(installer), "/install", "/quiet", "/norestart"],
            check=False,
        )
    except OSError as exc:
        if getattr(exc, "winerror", None) != 740:  # 740 = elevation required
            raise
        # Re-run through UAC and wait for it; exit code comes back via PowerShell.
        ps = (
            f"$p = Start-Process -FilePath '{installer}' -ArgumentList '/install','/quiet','/norestart' "
            "-Verb RunAs -Wait -PassThru; exit $p.ExitCode"
        )
        result = subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=False)
    # InstallShield returns 3010 when a reboot is required; treat as success.
    if result.returncode not in (0, 3010):
        raise RuntimeError(
            f"UE4PrereqSetup_x64.exe failed with exit code {result.returncode}. "
            "Try running it manually from the Starcel install folder."
        )
    if result.returncode == 3010:
        print("UE4 prerequisites installed (a reboot is recommended before first launch).")
    else:
        print("UE4 prerequisites installed.")


def manual_instructions() -> str:
    installer = paths.prereq_installer()
    return (
        f"Open {installer} and click through the dialogs. It installs "
        "Visual C++ Redistributable 2015-2022 and the DirectX End-User Runtime."
    )
