"""Visual Studio 2019 Community silent install with UE4.27-required workloads."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from . import config, downloader


VSWHERE_PATHS = [
    Path(r"C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"),
    Path(r"C:\Program Files\Microsoft Visual Studio\Installer\vswhere.exe"),
]


def find_vswhere() -> Path | None:
    for p in VSWHERE_PATHS:
        if p.exists():
            return p
    return None


def vs2019_installed_with_cpp() -> bool:
    """True if VS 2019 with the NativeDesktop workload is already present."""
    vswhere = find_vswhere()
    if not vswhere:
        return False
    result = subprocess.run(
        [
            str(vswhere),
            "-version", "[16.0,17.0)",
            "-requires", "Microsoft.VisualStudio.Workload.NativeDesktop",
            "-property", "installationPath",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def install_vs2019(*, force: bool = False) -> None:
    """Download and silently install VS 2019 Community with UE4.27 workloads."""
    if not force and vs2019_installed_with_cpp():
        print("Visual Studio 2019 with C++ workload already installed — skipping.")
        return

    with tempfile.TemporaryDirectory(prefix="starcel-vs-") as tmpdir:
        installer = Path(tmpdir) / "vs_community.exe"
        downloader.download_vs2019_installer(installer)

        cmd = [str(installer), "--quiet", "--wait", "--norestart", "--nocache"]
        for component in config.VS2019_COMPONENTS:
            cmd += ["--add", component]

        print("Installing Visual Studio 2019 Community — this can take 30-60 minutes...")
        result = subprocess.run(cmd, check=False)
        if result.returncode not in (0, 3010):
            raise RuntimeError(
                f"vs_community.exe failed with exit code {result.returncode}. "
                "See %TEMP%\\dd_bootstrapper_*.log and %TEMP%\\dd_setup_*.log for details."
            )
        if result.returncode == 3010:
            print("VS 2019 installed (reboot recommended before using it).")
        else:
            print("VS 2019 installed.")


def manual_instructions() -> str:
    components = "\n".join(f"  - {c}" for c in config.VS2019_COMPONENTS)
    return (
        f"Download Visual Studio 2019 Community: {config.VS2019_INSTALLER_URL}\n"
        "Run the installer, then in the Workloads tab select 'Desktop development with C++'. "
        "In the Individual Components tab, check the following:\n"
        f"{components}\n"
        "Click 'Install'. This will take 30-60 minutes and use ~10 GB of disk."
    )
