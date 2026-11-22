"""Starcel: a Python-controlled 3D spreadsheet built on Unreal Engine 4.27.

This package is the Starcel launcher and installer. The Unreal build itself
(~1.5 GB) is too large for PyPI, so `starcel` downloads the newest build from
GitHub Releases into Documents\\Starcel the first time it runs.
"""
from pathlib import Path

from .config import VERSION as __version__

#: Copy of the Starcel Python scripts (Content/Scripts) bundled with the package.
SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"

__all__ = ["__version__", "SCRIPTS_DIR"]
