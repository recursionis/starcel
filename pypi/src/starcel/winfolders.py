"""Resolve Windows known folders (Documents, Desktop), following OneDrive redirection."""
from __future__ import annotations

import sys
from pathlib import Path

# KNOWNFOLDERID values
_DOCUMENTS = (0xFDD39AD0, 0x238F, 0x46AF, (0xAD, 0xB4, 0x6C, 0x85, 0x48, 0x03, 0x69, 0xC7))
_DESKTOP = (0xB4BFCC3A, 0xDB2C, 0x424C, (0xB0, 0x29, 0x7F, 0xE9, 0x9A, 0x87, 0xC6, 0x41))


def _known_folder(guid: tuple) -> Path | None:
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class GUID(ctypes.Structure):
            _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD),
                        ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8)]

        fid = GUID(guid[0], guid[1], guid[2], (ctypes.c_ubyte * 8)(*guid[3]))
        buf = ctypes.c_wchar_p()
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(fid), 0, None, ctypes.byref(buf)) != 0:
            return None
        try:
            return Path(buf.value)
        finally:
            ctypes.windll.ole32.CoTaskMemFree(buf)
    except Exception:
        return None


def documents() -> Path:
    return _known_folder(_DOCUMENTS) or Path.home() / "Documents"


def desktop() -> Path:
    return _known_folder(_DESKTOP) or Path.home() / "Desktop"
