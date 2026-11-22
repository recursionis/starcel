"""Post-install entry point: download build, copy wrappers, dispatch to auto/manual."""
from __future__ import annotations

import importlib.resources
import shutil
from pathlib import Path

from . import config, downloader, install_modes, paths


_WRAPPER_EXES = [
    "starcel.exe",
    "starcel-run.exe",
    "starcel-server.exe",
    "starcel-editor.exe",
    "starcelw.exe",
]


def copy_wrapper_exes() -> list[Path]:
    """Copy starcel*.exe from the Python Scripts folder into <install_root>\\bin.

    pip-generated wrappers embed an absolute path to python.exe, so copies keep
    working. bin\\ is added to the user PATH, so `starcel` works in any new
    terminal even when pip put the originals in a folder that isn't on PATH.
    """
    if not config.COPY_SCRIPTS_TO_INSTALL_ROOT:
        return []

    scripts = paths.python_scripts_dir()
    dest = config.BIN_DIR
    dest.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for name in _WRAPPER_EXES:
        src = scripts / name
        if not src.exists():
            print(f"  skip: {src} does not exist (pip may not have generated it yet)")
            continue
        target = dest / name
        shutil.copy2(src, target)
        copied.append(target)
        print(f"  copied: {src.name} -> {target}")
    return copied


def write_user_settings_if_missing() -> None:
    """Seed <install_root>\\settings.ini with the template on first install."""
    if config.USER_SETTINGS_FILE.exists():
        return
    config.USER_SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    template = importlib.resources.files(__package__).joinpath("templates", "settings.ini").read_text(encoding="utf-8")
    config.USER_SETTINGS_FILE.write_text(template, encoding="utf-8")
    print(f"Wrote default settings to {config.USER_SETTINGS_FILE}")


def install(*, manual: bool = False, offline: bool = False, force: bool = False) -> None:
    """Main entry point for `starcel install`."""
    downloader.ensure_build(offline=offline, force=force)
    copy_wrapper_exes()
    write_user_settings_if_missing()

    if manual:
        install_modes.manual_install()
    else:
        install_modes.auto_install()

    print(f"\nStarcel is installed at {paths.build_root()}")
    try:
        print(f"Python scripts: {paths.scripts_dir()}")
    except FileNotFoundError:
        pass
    print("Launch with: starcel  (or double-click the Desktop shortcut)")


def install_dev(*, manual: bool = False, ue_target_dir: Path | None = None) -> None:
    """Dev flow for `starcel install-dev`."""
    write_user_settings_if_missing()
    if manual:
        install_modes.manual_install()
    else:
        install_modes.auto_install_dev(ue_target_dir)


def uninstall(*, delete_files: bool | None = None) -> None:
    """Remove shortcuts, env vars, firewall rule; optionally the install folder.

    delete_files=None asks interactively, because the install folder holds the
    user's edited Content/Scripts and their backups.
    """
    from . import env, firewall, shortcuts

    print("Removing shortcuts...")
    shortcuts.remove_all()
    print("Removing firewall rule...")
    firewall.remove_rule()
    print("Removing STARCEL_HOME + PATH entry...")
    env.uninstall_all()
    if config.BIN_DIR.exists():
        shutil.rmtree(config.BIN_DIR, ignore_errors=True)

    root = paths.install_root()
    if root.exists():
        if delete_files is None:
            answer = input(f"Also delete {root}, including your Content/Scripts edits and backups? [y/N] ")
            delete_files = answer.strip().lower() in ("y", "yes")
        if delete_files:
            print(f"Deleting {root}...")
            shutil.rmtree(root, ignore_errors=True)
        else:
            print(f"Kept {root}.")
    print("Uninstall complete. Remove the Python package with: pip uninstall starcel")
