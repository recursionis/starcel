"""User environment variables, user PATH, and Windows long-path support.

STARCEL_HOME and PATH are set per-user (HKCU) so no admin rights are needed.
Long-path support is a machine setting and is skipped with a note when not
running elevated.
"""
from __future__ import annotations

import ctypes
import winreg

from . import config

_ENV_KEY = r"Environment"


def _broadcast_env_change() -> None:
    """Tell Explorer/new terminals that environment variables changed."""
    try:
        HWND_BROADCAST, WM_SETTINGCHANGE, SMTO_ABORTIFHUNG = 0xFFFF, 0x1A, 0x0002
        result = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 2000, ctypes.byref(result)
        )
    except Exception:
        pass


def _get_user_env(name: str) -> tuple[str | None, int]:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _ENV_KEY, 0, winreg.KEY_READ) as k:
        try:
            value, kind = winreg.QueryValueEx(k, name)
            return value, kind
        except FileNotFoundError:
            return None, winreg.REG_EXPAND_SZ


def _set_user_env(name: str, value: str, kind: int = winreg.REG_EXPAND_SZ) -> None:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _ENV_KEY, 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, name, 0, kind, value)


def _delete_user_env(name: str) -> None:
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _ENV_KEY, 0, winreg.KEY_SET_VALUE) as k:
            winreg.DeleteValue(k, name)
    except FileNotFoundError:
        pass


def _same_dir(a: str, b: str) -> bool:
    return a.rstrip("\\").lower() == b.rstrip("\\").lower()


def set_starcel_home() -> None:
    """Set user STARCEL_HOME to the install root."""
    _set_user_env(config.ENV_VAR_HOME, str(config.INSTALL_ROOT), winreg.REG_SZ)


def prepend_starcel_to_path() -> None:
    """Prepend <install_root>\\bin to the user PATH if not already present."""
    if not config.ADD_TO_PATH:
        return
    entry = str(config.BIN_DIR)
    current, kind = _get_user_env("Path")
    parts = [p for p in (current or "").split(";") if p]
    if any(_same_dir(p, entry) for p in parts):
        return
    _set_user_env("Path", ";".join([entry] + parts), kind)
    print(f"Added {entry} to your user PATH (open a new terminal to use `starcel`).")


def enable_long_paths() -> None:
    """Enable NTFS long-path support (paths > 260 chars). Needs admin."""
    if not config.ENABLE_LONG_PATHS:
        return
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\FileSystem",
            0,
            winreg.KEY_READ | winreg.KEY_SET_VALUE,
        ) as k:
            try:
                if winreg.QueryValueEx(k, "LongPathsEnabled")[0] == 1:
                    return
            except FileNotFoundError:
                pass
            winreg.SetValueEx(k, "LongPathsEnabled", 0, winreg.REG_DWORD, 1)
            print("Enabled Windows long-path support.")
    except PermissionError:
        print("Skipped enabling long paths (needs an administrator terminal; usually not required).")


def starcel_on_path() -> bool:
    current, _ = _get_user_env("Path")
    return any(_same_dir(p, str(config.BIN_DIR)) for p in (current or "").split(";") if p)


def remove_starcel_from_path() -> None:
    entry = str(config.BIN_DIR)
    current, kind = _get_user_env("Path")
    if not current:
        return
    parts = [p for p in current.split(";") if p]
    filtered = [p for p in parts if not _same_dir(p, entry)]
    if len(filtered) != len(parts):
        _set_user_env("Path", ";".join(filtered), kind)


def remove_starcel_home() -> None:
    _delete_user_env(config.ENV_VAR_HOME)


def install_all() -> None:
    if config.INSTALL_ENV_VARS:
        set_starcel_home()
        prepend_starcel_to_path()
    enable_long_paths()
    _broadcast_env_change()


def uninstall_all() -> None:
    remove_starcel_from_path()
    remove_starcel_home()
    _broadcast_env_change()


def manual_instructions() -> str:
    return (
        "Open Settings and search for 'Edit environment variables for your account'. "
        "Under 'User variables':\n"
        f"  1. New -> Name: {config.ENV_VAR_HOME}, Value: {config.INSTALL_ROOT}\n"
        f"  2. Edit 'Path' -> New -> paste: {config.BIN_DIR}\n"
        "Optionally enable long paths via an admin PowerShell:\n"
        '  New-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" '
        '-Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force'
    )
