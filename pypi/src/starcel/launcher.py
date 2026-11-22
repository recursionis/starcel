"""Programmatic launchers for the client, dedicated server, and UE4 editor.

Each launcher returns a subprocess.Popen. Call .wait() if you want to block
until the process exits.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from . import paths
from .launch_options import (
    ClientLaunchOptions,
    EditorLaunchOptions,
    ServerLaunchOptions,
    load_options,
)


def launch_client(opts: ClientLaunchOptions | None = None) -> subprocess.Popen:
    """Launch the game client. Mirrors _StartClient.bat with configurable flags."""
    if opts is None:
        opts = load_options("client")
    exe = paths.client_exe()
    args = [str(exe), *opts.to_ue_args()]
    return subprocess.Popen(args, cwd=str(exe.parent))


def launch_server(opts: ServerLaunchOptions | None = None) -> subprocess.Popen:
    """Launch the dedicated server. Mirrors _StartServer.bat with configurable flags.

    Runs in a detached process group so closing the CLI window doesn't kill the server.
    """
    if opts is None:
        opts = load_options("server")
    exe = paths.server_exe()
    args = [str(exe), *opts.to_ue_args()]
    return subprocess.Popen(
        args,
        cwd=str(exe.parent),
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
    )


def launch_editor(opts: EditorLaunchOptions | None = None, uproject: Path | None = None) -> subprocess.Popen:
    """Open the .uproject in the UE4.27 editor. Requires UE4.27 installed or built."""
    if opts is None:
        opts = load_options("editor")
    editor = paths.ue4_editor_exe()
    project = uproject if uproject else paths.uproject()
    args = [str(editor), str(project), *opts.to_ue_args()]
    return subprocess.Popen(args, cwd=str(editor.parent))


def dry_run_args(kind: str, opts) -> list[str]:
    """Return the exact argv list that would be passed to subprocess, without launching."""
    if kind == "client":
        return [str(paths.client_exe()), *opts.to_ue_args()]
    if kind == "server":
        return [str(paths.server_exe()), *opts.to_ue_args()]
    if kind == "editor":
        return [str(paths.ue4_editor_exe()), str(paths.uproject()), *opts.to_ue_args()]
    raise ValueError(f"Unknown launch kind: {kind!r}")
