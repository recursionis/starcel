"""Resolve install locations and exe/uproject paths.

Layout (default install root is Documents\\Starcel):

    <install_root>/
        WindowsNoEditor/            <- build_root(): the extracted GitHub release zip
            Starcel9.exe
            Starcel9/Content/Scripts/
        bin/                        <- starcel*.exe wrappers (on user PATH)
        backups/                    <- Content/Scripts copies saved before updates
        release.json, settings.ini

Two resolution mechanisms inside build_root():

1. Release manifest: if <build_root>/starcel_manifest.json exists, read the
   explicit names from it.
2. Candidate pattern matching: walk CLIENT_EXE_CANDIDATES (etc.) from config.py
   in order, exact names first, then globs. Shallowest match wins.
"""
from __future__ import annotations

import json
import os
import sys
import sysconfig
from pathlib import Path

from . import config

_BUILD_DIR_NAMES = ("WindowsNoEditor", "WindowsClient")


def install_root() -> Path:
    return config.INSTALL_ROOT


def build_root() -> Path:
    """Folder holding the extracted packaged build (contains Engine/ and Starcel9/)."""
    root = install_root()
    for name in _BUILD_DIR_NAMES:
        candidate = root / name
        if candidate.is_dir():
            return candidate
    if (root / "Engine").is_dir():  # zip without a top-level folder
        return root
    return root / _BUILD_DIR_NAMES[0]


def is_installed() -> bool:
    try:
        return client_exe().is_file()
    except FileNotFoundError:
        return False


def _load_manifest() -> dict | None:
    manifest_path = build_root() / config.MANIFEST_FILENAME
    if not manifest_path.exists():
        return None
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _resolve(candidates: list[str], manifest_key: str) -> Path:
    root = build_root()
    manifest = _load_manifest()
    if manifest and manifest.get(manifest_key):
        return root / manifest[manifest_key]

    if root.is_dir():
        # Prefer shallow matches: for UE4 packaged builds, the top-level
        # <ProjectName>.exe is the user-facing launcher; the deeper one under
        # <ProjectName>/Binaries/Win64/ is what the top-level forwards to.
        for exact_pass in (True, False):
            for name in candidates:
                if ("*" not in name) != exact_pass:
                    continue
                hits = sorted(root.rglob(name), key=lambda p: (len(p.parts), str(p)))
                if hits:
                    return hits[0]

    raise FileNotFoundError(
        f"No file matched any of {candidates} under {root}. Run `starcel update` to download "
        f"the build, or if the project was renamed, add the new name to config.{manifest_key.upper()}_CANDIDATES."
    )


def client_exe() -> Path:
    return _resolve(config.CLIENT_EXE_CANDIDATES, "client_exe")


def server_exe() -> Path:
    return _resolve(config.SERVER_EXE_CANDIDATES, "server_exe")


def uproject() -> Path:
    return _resolve(config.UPROJECT_CANDIDATES, "uproject")


def project_folder() -> Path:
    """The `Starcel9/` style subfolder inside the packaged tree."""
    root = build_root()
    manifest = _load_manifest()
    if manifest and manifest.get("project_name"):
        return root / manifest["project_name"]
    for exact_pass in (True, False):
        for name in config.PROJECT_FOLDER_CANDIDATES:
            if ("*" not in name) != exact_pass:
                continue
            hits = sorted(p for p in root.glob(name) if p.is_dir()) if root.is_dir() else []
            if hits:
                return hits[0]
    raise FileNotFoundError(
        f"No project folder matched any of {config.PROJECT_FOLDER_CANDIDATES} under {root}."
    )


def scripts_dir() -> Path:
    """The installed build's Content/Scripts folder (what the game actually runs)."""
    return project_folder() / config.SCRIPTS_SUBPATH


def prereq_installer() -> Path:
    """Bundled UE4PrereqSetup_x64.exe — path is stable across UE4.27 versions."""
    return build_root() / "Engine" / "Extras" / "Redist" / "en-us" / "UE4PrereqSetup_x64.exe"


def manifest_path() -> Path:
    return build_root() / config.MANIFEST_FILENAME


def ue4_editor_exe() -> Path:
    """Locate UE4Editor.exe for UE4.27.

    Tries in order:
      1. HKLM\\SOFTWARE\\EpicGames\\Unreal Engine\\4.27\\InstalledDirectory
      2. HKCU\\SOFTWARE\\Epic Games\\Unreal Engine\\4.27\\InstalledDirectory
      3. Default Epic install path: C:\\Program Files\\Epic Games\\UE_4.27
      4. From-source build at DEV_BUILD_UE_DEFAULT_DIR
    """
    import winreg

    candidates: list[Path] = []
    for hive, key in [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\EpicGames\Unreal Engine\4.27"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Epic Games\Unreal Engine\4.27"),
    ]:
        try:
            with winreg.OpenKey(hive, key) as k:
                install_dir = Path(winreg.QueryValueEx(k, "InstalledDirectory")[0])
                candidates.append(install_dir / "Engine" / "Binaries" / "Win64" / "UE4Editor.exe")
        except OSError:
            pass

    candidates.append(Path(r"C:\Program Files\Epic Games\UE_4.27\Engine\Binaries\Win64\UE4Editor.exe"))
    candidates.append(config.DEV_BUILD_UE_DEFAULT_DIR / "Engine" / "Binaries" / "Win64" / "UE4Editor.exe")

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find UE4.27 editor. Install UE4.27 via the Epic Launcher, or "
        "build from source and set config.DEV_BUILD_UE_DEFAULT_DIR. Checked: "
        + ", ".join(str(c) for c in candidates)
    )


def python_exe() -> Path:
    """Absolute path to the Python running this package."""
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe":
        exe = exe.with_name("python.exe")
    if exe.exists():
        return exe
    fallback = config.PYTHON_INSTALL_DIR / "python.exe"
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"Python not found at {exe} or {fallback}")


def python_scripts_dir() -> Path:
    """Folder where pip put the starcel*.exe wrappers (system or --user install)."""
    candidates = [Path(sysconfig.get_path("scripts"))]
    try:
        candidates.append(Path(sysconfig.get_path("scripts", f"{os.name}_user")))
    except KeyError:
        pass
    for c in candidates:
        if (c / "starcel.exe").exists():
            return c
    return candidates[0]
