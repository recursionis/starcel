"""Clone + build UE4.27.2 from the EpicGames GitHub repo.

The EpicGames/UnrealEngine repo is gated — access requires that the user's
Epic Games account be linked to GitHub (see UE_ON_GITHUB_DOC_URL). If the
user hasn't done this, `git clone` returns 404. We surface that early with a
clear message + link.

This is a multi-hour, ~150 GB operation. Opt out via
config.DEV_BUILD_UE_FROM_SOURCE = False if the user already has a built engine.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from . import config


class EpicAuthError(RuntimeError):
    """Raised when the EpicGames/UnrealEngine repo is inaccessible (unlinked account)."""


def check_epic_github_access() -> None:
    """Verify the current user can access EpicGames/UnrealEngine. Raises on failure."""
    result = subprocess.run(
        ["git", "ls-remote", config.UE_SOURCE_REPO, "HEAD"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        stderr = (result.stderr or "").lower()
        if "404" in stderr or "not found" in stderr or "authentication" in stderr:
            raise EpicAuthError(
                "Cannot access EpicGames/UnrealEngine — this repo is private and requires "
                "that your Epic Games account be linked to GitHub.\n\n"
                f"Follow the instructions at {config.UE_ON_GITHUB_DOC_URL} to link your "
                "accounts, then retry `starcel install-dev`."
            )
        raise RuntimeError(f"git ls-remote failed: {result.stderr or result.stdout}")


def clone(target_dir: Path) -> None:
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"{target_dir} already exists and is non-empty — skipping clone.")
        return
    print(f"Cloning {config.UE_SOURCE_REPO} (branch {config.UE_SOURCE_BRANCH}) into {target_dir}...")
    subprocess.run(
        [
            "git", "clone",
            "--branch", config.UE_SOURCE_BRANCH,
            "--single-branch",
            "--depth", "1",
            config.UE_SOURCE_REPO,
            str(target_dir),
        ],
        check=True,
    )


def run_setup(target_dir: Path) -> None:
    print("Running Setup.bat (downloads ~20 GB of engine binary dependencies)...")
    subprocess.run([str(target_dir / "Setup.bat")], check=True, cwd=str(target_dir))


def run_generate_project_files(target_dir: Path) -> None:
    print("Running GenerateProjectFiles.bat...")
    subprocess.run(
        [str(target_dir / "GenerateProjectFiles.bat")],
        check=True,
        cwd=str(target_dir),
    )


def build_engine(target_dir: Path) -> None:
    """Build the UE4 Development Editor target. Takes 1-3 hours on a fast machine."""
    msbuild = _find_msbuild()
    if not msbuild:
        raise RuntimeError(
            "MSBuild not found. Install Visual Studio 2019 with the NativeDesktop workload first "
            "via `starcel install-dev` (it calls vs_installer before this step)."
        )
    sln = target_dir / "UE4.sln"
    if not sln.exists():
        raise FileNotFoundError(f"UE4.sln not found at {sln}. Did GenerateProjectFiles.bat succeed?")

    print("Building UE4.sln (Development Editor | Win64). This takes 1-3 hours...")
    subprocess.run(
        [
            str(msbuild),
            str(sln),
            "/t:Build",
            "/p:Configuration=Development Editor",
            "/p:Platform=Win64",
            "/m",
            "/v:m",
        ],
        check=True,
    )


def _find_msbuild() -> Path | None:
    from .vs_installer import find_vswhere

    vswhere = find_vswhere()
    if not vswhere:
        return None
    result = subprocess.run(
        [
            str(vswhere),
            "-version", "[16.0,17.0)",
            "-requires", "Microsoft.Component.MSBuild",
            "-find", r"MSBuild\**\Bin\MSBuild.exe",
            "-latest",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    output = result.stdout.strip().splitlines()
    return Path(output[0]) if output else None


def install_ue_source(target_dir: Path | None = None) -> None:
    """Full flow: check auth → clone → Setup → GenerateProjectFiles → build."""
    if not config.DEV_BUILD_UE_FROM_SOURCE:
        print("DEV_BUILD_UE_FROM_SOURCE is False — skipping UE4 source build.")
        return

    target = target_dir or config.DEV_BUILD_UE_DEFAULT_DIR
    check_epic_github_access()
    clone(target)
    run_setup(target)
    run_generate_project_files(target)
    build_engine(target)
    print(f"UE4.27.2 built successfully at {target}")


def manual_instructions() -> str:
    return (
        f"Link your Epic account to GitHub: {config.UE_ON_GITHUB_DOC_URL}\n"
        "Then open a terminal and run:\n\n"
        f"  git clone --branch {config.UE_SOURCE_BRANCH} {config.UE_SOURCE_REPO} "
        f"\"{config.DEV_BUILD_UE_DEFAULT_DIR}\"\n"
        f"  cd \"{config.DEV_BUILD_UE_DEFAULT_DIR}\"\n"
        "  Setup.bat\n"
        "  GenerateProjectFiles.bat\n"
        "\nThen open UE4.sln in Visual Studio 2019 and build 'Development Editor' | 'Win64'."
    )
