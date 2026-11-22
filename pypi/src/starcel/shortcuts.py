"""Create Desktop + Start Menu shortcuts for the four launch profiles.

Attempts all-users Start Menu first (requires admin). Falls back to per-user
on PermissionError.

Targets point at the pip-generated wrapper exes in the Starcel install folder
(starcelw.exe for client, starcel-server.exe, starcel-editor.exe) so flag logic
stays in starcel.cli / starcel.launcher rather than being baked into each
shortcut's Arguments field.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import config, paths


@dataclass(frozen=True)
class _Shortcut:
    filename: str
    target_exe: str
    arguments: str
    description: str


_SHORTCUTS: tuple[_Shortcut, ...] = (
    _Shortcut(
        filename="Starcel (Play).lnk",
        target_exe="starcelw.exe",
        arguments="",
        description="Launch Starcel (server from settings.ini, if set)",
    ),
    _Shortcut(
        filename="Starcel (Standalone).lnk",
        target_exe="starcelw.exe",
        arguments="--standalone",
        description="Launch Starcel without connecting to a server",
    ),
    _Shortcut(
        filename="Starcel (Host Server).lnk",
        target_exe="starcel-server.exe",
        arguments="",
        description="Start the Starcel dedicated server",
    ),
    _Shortcut(
        filename="Starcel (Editor).lnk",
        target_exe="starcel-editor.exe",
        arguments="",
        description="Open Starcel9.uproject in the UE4.27 editor",
    ),
)


def _create_one(lnk_path: Path, target: Path, arguments: str, description: str, icon: Path) -> None:
    """Write a .lnk file via the Windows Shell COM object."""
    from win32com.client import Dispatch

    lnk_path.parent.mkdir(parents=True, exist_ok=True)
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(lnk_path))
    shortcut.Targetpath = str(target)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = str(target.parent)
    shortcut.Description = description
    shortcut.IconLocation = f"{icon},0"
    shortcut.Save()


def _install_dir_exe(exe_name: str) -> Path:
    """Path to a wrapper exe in <install_root>\\bin\\ (copied there by post_install).

    Falls back to the Python Scripts folder if the copy hasn't happened yet.
    """
    install_exe = config.BIN_DIR / exe_name
    if install_exe.exists():
        return install_exe
    scripts_exe = paths.python_scripts_dir() / exe_name
    if scripts_exe.exists():
        return scripts_exe
    return install_exe


def create_all() -> list[Path]:
    """Create all four shortcuts on Desktop + Start Menu. Returns list of paths created."""
    try:
        icon = paths.client_exe()
    except FileNotFoundError:
        icon = _install_dir_exe("starcelw.exe")

    start_menu_dir = _resolve_start_menu_dir()
    desktop_dir = config.SHORTCUT_DESKTOP_DIR

    created: list[Path] = []
    for entry in _SHORTCUTS:
        target = _install_dir_exe(entry.target_exe)
        for directory in (desktop_dir, start_menu_dir):
            lnk = directory / entry.filename
            _create_one(lnk, target, entry.arguments, entry.description, icon)
            created.append(lnk)
    return created


def _resolve_start_menu_dir() -> Path:
    """All-users first (admin), per-user on PermissionError."""
    allusers = config.SHORTCUT_START_MENU_ALLUSERS_DIR
    try:
        allusers.mkdir(parents=True, exist_ok=True)
        probe = allusers / ".starcel-write-test"
        probe.write_text("", encoding="utf-8")
        probe.unlink()
        return allusers
    except (PermissionError, OSError):
        user_dir = config.SHORTCUT_START_MENU_USER_DIR
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir


def remove_all() -> list[Path]:
    """Delete every shortcut this module may have created. Returns list of paths removed."""
    removed: list[Path] = []
    for directory in (
        config.SHORTCUT_DESKTOP_DIR,
        config.SHORTCUT_START_MENU_ALLUSERS_DIR,
        config.SHORTCUT_START_MENU_USER_DIR,
    ):
        for entry in _SHORTCUTS:
            lnk = directory / entry.filename
            if lnk.exists():
                try:
                    lnk.unlink()
                    removed.append(lnk)
                except OSError:
                    pass
        if directory.exists() and directory.name == "Starcel" and not any(directory.iterdir()):
            try:
                directory.rmdir()
            except OSError:
                pass
    return removed


def manual_instructions() -> str:
    return (
        "Create a Desktop shortcut by right-clicking 'starcelw.exe' in "
        f"{config.BIN_DIR} and selecting 'Send to → Desktop (create shortcut)'. "
        "Repeat for starcel-server.exe and starcel-editor.exe."
    )
