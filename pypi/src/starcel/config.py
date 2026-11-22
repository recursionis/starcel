"""Central static config for the starcel pip package.

All tunable paths, URLs, install toggles, and default launch flags live here.
Edit this file to change behavior project-wide; for per-user overrides of
launch flags, edit Documents\\Starcel\\settings.ini instead.
"""
from __future__ import annotations

import os
from pathlib import Path

from . import winfolders

VERSION = "0.2.0a2"

# --- Install locations ---
# Default is Documents\Starcel so users can find and edit
# WindowsNoEditor\Starcel9\Content\Scripts easily. To use another folder, pass
# `--dir PATH` to any starcel command; it is saved as the user environment
# variable STARCEL_HOME and used from then on.
ENV_VAR_HOME        = "STARCEL_HOME"
DEFAULT_INSTALL_ROOT = winfolders.documents() / "Starcel"


def _saved_install_root() -> str | None:
    """STARCEL_HOME from this process, else from the user's registry environment
    (so a location chosen with --dir applies even before a new terminal is opened)."""
    value = os.environ.get(ENV_VAR_HOME)
    if value:
        return value
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ENV_VAR_HOME)[0] or None
    except (ImportError, OSError):
        return None


def set_install_root(root: Path) -> None:
    """Point every install-location setting at `root` for this process."""
    global INSTALL_ROOT, BIN_DIR, BACKUPS_DIR, RELEASE_STATE_FILE, USER_SETTINGS_DIR, USER_SETTINGS_FILE
    INSTALL_ROOT        = Path(root)
    BIN_DIR             = INSTALL_ROOT / "bin"            # starcel*.exe wrappers (added to user PATH)
    BACKUPS_DIR         = INSTALL_ROOT / "backups"        # Content/Scripts copies saved before each update
    RELEASE_STATE_FILE  = INSTALL_ROOT / "release.json"   # which GitHub release is installed
    USER_SETTINGS_DIR   = INSTALL_ROOT
    USER_SETTINGS_FILE  = USER_SETTINGS_DIR / "settings.ini"


set_install_root(Path(_saved_install_root() or DEFAULT_INSTALL_ROOT))
PYTHON_INSTALL_DIR  = Path(r"C:\Program Files\Python39")

# Python PATH handling is decided interactively by the bootstrapper.
# None = prompt user. True/False = skip the dialog and force that choice.
PREPEND_PYTHON_TO_PATH: bool | None = None

# --- GitHub Releases (the packaged game build lives on the UE repo) ---
# The newest non-draft release (pre-releases included) is used. The first
# asset name in BUILD_ASSET_NAMES that the release has is downloaded; if the
# release also has "<asset>.sha256", the download is verified against it.
GAME_REPO             = "recursionis/starcel"
BUILD_ASSET_NAMES     = ["WindowsNoEditor.zip", "WindowsClient.zip"]
SCRIPTS_SUBPATH       = Path("Content") / "Scripts"   # inside the project folder (Starcel9/)
INSTALLER_ASSET_NAME  = "StarcelInstaller.exe"

# --- Third-party download URLs ---
PYTHON_INSTALLER_URL  = "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
VS2019_INSTALLER_URL  = "https://aka.ms/vs/16/release/vs_community.exe"
UE_SOURCE_REPO        = "https://github.com/EpicGames/UnrealEngine.git"
UE_SOURCE_BRANCH      = "4.27-chaos"
UE_ON_GITHUB_DOC_URL  = "https://www.unrealengine.com/en-US/ue-on-github"

# --- VS 2019 workload component IDs (needed to build UE4.27 from source) ---
VS2019_COMPONENTS = [
    "Microsoft.VisualStudio.Workload.NativeDesktop",
    "Microsoft.VisualStudio.Component.VC.v142.x86.x64",
    "Microsoft.VisualStudio.Component.Windows10SDK.19041",
    "Microsoft.VisualStudio.Component.VC.CMake.Project",
    "Microsoft.VisualStudio.Component.VC.ATL",
    "Microsoft.VisualStudio.Component.VC.ATLMFC",
    "Microsoft.VisualStudio.Component.VC.DiagnosticTools",
    "Microsoft.VisualStudio.Component.VC.CLI.Support",
    "Microsoft.VisualStudio.Component.Debugger.JustInTime",
    "Microsoft.VisualStudio.Component.VC.CoreIde",
    "Microsoft.VisualStudio.Component.Graphics",
    "Microsoft.Component.MSBuild",
]

# --- Version-independent exe/uproject resolution ---
# paths.py tries each candidate in order (exact names first, then globs).
# When you rename the UE module (Starcel9 → Starcel11 → StarcelClient → ...),
# prepend the new name to each list. Old entries stay below as fallbacks for
# older installs.
CLIENT_EXE_CANDIDATES = [
    "Starcel9.exe",
    "Starcel9Client.exe",
    "StarcelClient.exe",
    "Starcel*Client.exe",
    "Starcel*.exe",
]
SERVER_EXE_CANDIDATES = [
    "Starcel9Server.exe",
    "StarcelServer.exe",
    "Starcel*Server.exe",
]
UPROJECT_CANDIDATES = [
    "Starcel9.uproject",
    "Starcel*.uproject",
]
PROJECT_FOLDER_CANDIDATES = [
    "Starcel9",
    "Starcel*",
]

# --- Shortcut targets ---
SHORTCUT_DESKTOP_DIR             = winfolders.desktop()
SHORTCUT_START_MENU_ALLUSERS_DIR = Path(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Starcel")
SHORTCUT_START_MENU_USER_DIR     = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Starcel"

# --- Launch defaults ---
# Every _StartClient.bat / _StartServer.bat flag has a key here. User overrides
# go in settings.ini; per-run overrides come from the CLI. Precedence:
# CLI args > settings.ini > these defaults.
CLIENT_DEFAULTS = {
    "server_host":     "",  # standalone by default; set in settings.ini or pass --server

    "res_x":           1600,
    "res_y":           900,
    "windowed":        True,
    "fullscreen":      False,
    "console":         True,
    "log":             True,
    "stdout":          True,
    "full_stdout":     True,
    "unattended":      False,
    "nullrhi":         False,
    "nosound":         False,
    "exec_cmds":       "",
    "log_cmds":        "",
    "abs_log":         "",
    "ini_overrides":   [],
    "extra_args":      [],
}
SERVER_DEFAULTS = {
    "port":             7827,
    "log":              True,
    "windowed":         True,
    "console":          True,
    "nullrhi":          True,
    "useperfcounters":  True,
    "unattended":       True,
    "exec_cmds":        "",
    "log_cmds":         "",
    "abs_log":          "",
    "ini_overrides":    [],
    "extra_args":       [],
}
EDITOR_DEFAULTS = {
    "abs_log":          "",
    "extra_args":       [],
}

# --- Env vars + firewall ---
ADD_TO_PATH                  = True
ENABLE_LONG_PATHS            = True
FIREWALL_PORT                = 7827
FIREWALL_RULE_NAME           = "Starcel Server"
COPY_SCRIPTS_TO_INSTALL_ROOT = True

# --- Install behavior toggles ---
AUTO_INSTALL              = True
INSTALL_SHORTCUTS         = True
INSTALL_PREREQS           = True
INSTALL_FIREWALL_RULE     = True
INSTALL_ENV_VARS          = True
DEV_BUILD_UE_FROM_SOURCE  = True
DEV_BUILD_UE_DEFAULT_DIR  = Path(r"C:\UnrealEngine-4.27-chaos")

# --- Donation / support ---
DONATION_URLS = {
    "Patreon": "https://www.patreon.com/RecursionIs",
    "PayPal":  "https://www.paypal.com/paypalme/RecursionIs",
}
SUPPORT_EMAIL            = "help@recursion.is"
COMMERCIAL_LICENSE_EMAIL = "nick@recursion.is"

# --- Release manifest ---
MANIFEST_FILENAME = "starcel_manifest.json"
MANIFEST_VERSION  = 1
