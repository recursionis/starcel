"""Command-line entry point. Dispatches subcommands to the relevant module.

Every UE launch flag is exposed as a CLI arg. Values follow 3-layer precedence:
CLI > settings.ini > config defaults.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from . import config, downloader, launch_options, launcher, paths, post_install
from .launch_options import (
    ClientLaunchOptions,
    EditorLaunchOptions,
    ServerLaunchOptions,
    load_options,
    show_effective_config,
)


def _parse_res(value: str) -> tuple[int, int]:
    if "x" not in value.lower():
        raise argparse.ArgumentTypeError(f"--res expects WxH (e.g. 1920x1080), got {value!r}")
    x, y = value.lower().split("x", 1)
    return int(x), int(y)


def _add_client_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--server", dest="server_host", metavar="HOST:PORT",
                   help="connect to this server (e.g. 192.168.1.20:7827)")
    p.add_argument("--offline", action="store_true",
                   help="don't check GitHub for a newer build before launching")
    p.add_argument("--standalone", action="store_const", const="", dest="server_host",
                   help="launch without connecting to a server (overrides --server)")
    p.add_argument("--res", dest="_res", type=_parse_res, metavar="WxH",
                   help="window resolution, e.g. 1920x1080")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--windowed", action="store_true", default=None)
    mode.add_argument("--fullscreen", action="store_true", default=None)
    _tristate(p, "console")
    _tristate(p, "log")
    _tristate(p, "stdout")
    _tristate(p, "full-stdout", dest="full_stdout")
    p.add_argument("--unattended", action="store_true", default=None)
    p.add_argument("--nullrhi", action="store_true", default=None)
    p.add_argument("--nosound", action="store_true", default=None)
    p.add_argument("--exec", dest="exec_cmds", metavar='"CMDS"',
                   help='-ExecCmds="cmd1;cmd2" passthrough')
    p.add_argument("--log-cmds", dest="log_cmds", metavar='"CATEGORY VERBOSITY"',
                   help='-LogCmds="LogNet Verbose,LogTemp Warning"')
    p.add_argument("--abs-log", dest="abs_log", metavar="PATH",
                   help='-ABSLOG="PATH" — write UE log to a custom absolute file path')
    p.add_argument("--extra", dest="extra_args", action="append", default=None,
                   help="free-form passthrough (repeatable)")
    p.add_argument("--dry-run", action="store_true",
                   help="print the exact UE command line without launching")


def _add_server_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--port", type=int)
    _tristate(p, "log")
    _tristate(p, "windowed")
    _tristate(p, "console")
    _tristate(p, "nullrhi")
    _tristate(p, "useperfcounters")
    _tristate(p, "unattended")
    p.add_argument("--exec", dest="exec_cmds", metavar='"CMDS"')
    p.add_argument("--log-cmds", dest="log_cmds", metavar='"CATEGORY VERBOSITY"')
    p.add_argument("--abs-log", dest="abs_log", metavar="PATH",
                   help='-ABSLOG="PATH" — write UE log to a custom absolute file path')
    p.add_argument("--extra", dest="extra_args", action="append", default=None)
    p.add_argument("--dry-run", action="store_true")


def _add_editor_flags(p: argparse.ArgumentParser) -> None:
    p.add_argument("--abs-log", dest="abs_log", metavar="PATH",
                   help='-ABSLOG="PATH" — write UE log to a custom absolute file path')
    p.add_argument("--extra", dest="extra_args", action="append", default=None)
    p.add_argument("--dry-run", action="store_true")


def _tristate(p: argparse.ArgumentParser, name: str, *, dest: str | None = None) -> None:
    """Add --foo / --no-foo pair that yields True / False / None (unset)."""
    dest = dest or name.replace("-", "_")
    p.add_argument(f"--{name}", dest=dest, action="store_true", default=None)
    p.add_argument(f"--no-{name}", dest=dest, action="store_false", default=None)


def _extract_cli_overrides(args: argparse.Namespace, cls: type) -> dict[str, Any]:
    """Pull CLI args matching dataclass field names into a dict of overrides."""
    from dataclasses import fields as dc_fields
    field_names = {f.name for f in dc_fields(cls)}
    overrides: dict[str, Any] = {}
    data = vars(args)
    for k, v in data.items():
        if k in field_names and v is not None:
            overrides[k] = v
    if getattr(args, "_res", None):
        overrides["res_x"], overrides["res_y"] = args._res
    return overrides


def _run_client(args: argparse.Namespace) -> int:
    overrides = _extract_cli_overrides(args, ClientLaunchOptions)
    opts: ClientLaunchOptions = load_options("client", overrides)
    if args.dry_run:
        print(" ".join(launcher.dry_run_args("client", opts)))
        return 0
    # First run downloads the build; later runs pick up newer GitHub releases.
    downloader.ensure_build(offline=args.offline, on_download=_gui_download_notice if _GUI else None)
    proc = launcher.launch_client(opts)
    return proc.wait()


def _run_server(args: argparse.Namespace) -> int:
    overrides = _extract_cli_overrides(args, ServerLaunchOptions)
    opts: ServerLaunchOptions = load_options("server", overrides)
    if args.dry_run:
        print(" ".join(launcher.dry_run_args("server", opts)))
        return 0
    proc = launcher.launch_server(opts)
    print(f"Started Starcel dedicated server (PID {proc.pid}).")
    return 0


def _run_editor(args: argparse.Namespace) -> int:
    overrides = _extract_cli_overrides(args, EditorLaunchOptions)
    opts: EditorLaunchOptions = load_options("editor", overrides)
    if args.dry_run:
        print(" ".join(launcher.dry_run_args("editor", opts)))
        return 0
    proc = launcher.launch_editor(opts)
    return proc.wait()


def _config_show(_args: argparse.Namespace) -> int:
    print(show_effective_config())
    return 0


def _config_edit(_args: argparse.Namespace) -> int:
    path = config.USER_SETTINGS_FILE
    if not path.exists():
        _config_reset(_args)
    os.startfile(str(path))
    return 0


def _config_reset(_args: argparse.Namespace) -> int:
    import importlib.resources
    config.USER_SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    template = importlib.resources.files(__package__).joinpath("templates", "settings.ini").read_text(encoding="utf-8")
    config.USER_SETTINGS_FILE.write_text(template, encoding="utf-8")
    print(f"Wrote defaults to {config.USER_SETTINGS_FILE}")
    return 0


def _config_path(_args: argparse.Namespace) -> int:
    print(config.USER_SETTINGS_FILE)
    return 0


def _install(args: argparse.Namespace) -> int:
    post_install.install(manual=args.manual, offline=args.offline, force=args.force)
    return 0


def _update(args: argparse.Namespace) -> int:
    downloader.ensure_build(force=args.force)
    return 0


def _scripts(args: argparse.Namespace) -> int:
    try:
        folder = paths.scripts_dir()
    except FileNotFoundError:
        print("No Starcel build installed yet; run `starcel update` first.", file=sys.stderr)
        return 1
    print(folder)
    if args.open:
        os.startfile(str(folder))
    return 0


def _install_dev(args: argparse.Namespace) -> int:
    ue_dir = Path(args.ue_dir) if args.ue_dir else None
    post_install.install_dev(manual=args.manual, ue_target_dir=ue_dir)
    return 0


def _install_shortcuts(_args: argparse.Namespace) -> int:
    from . import shortcuts
    created = shortcuts.create_all()
    for p in created:
        print(f"  {p}")
    return 0


def _install_prereqs(_args: argparse.Namespace) -> int:
    from . import prereqs
    prereqs.install_ue4_prereqs()
    return 0


def _install_env(_args: argparse.Namespace) -> int:
    from . import env
    env.install_all()
    return 0


def _uninstall(args: argparse.Namespace) -> int:
    post_install.uninstall(delete_files=args.delete_files)
    return 0


def _version(_args: argparse.Namespace) -> int:
    from . import donations
    print(f"starcel {config.VERSION}")
    release = downloader.installed_release()
    print(f"installed build: {release['name'] + ' (' + release['tag'] + ')' if release else 'none'}")
    print(f"install root:    {paths.install_root()}")
    if paths.is_installed():
        print(f"executable:      {paths.client_exe()}")
        try:
            print(f"scripts:         {paths.scripts_dir()}")
        except FileNotFoundError:
            pass
    donations.print_line()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="starcel", description="Starcel UE4.27 launcher and installer")
    sub = p.add_subparsers(dest="command")

    p_run = sub.add_parser("run", help="launch the client")
    _add_client_flags(p_run)
    p_run.set_defaults(func=_run_client)

    p_server = sub.add_parser("server", help="launch the dedicated server")
    _add_server_flags(p_server)
    p_server.set_defaults(func=_run_server)

    p_editor = sub.add_parser("editor", help="open Starcel9.uproject in UE4.27 editor")
    _add_editor_flags(p_editor)
    p_editor.set_defaults(func=_run_editor)

    p_install = sub.add_parser("install", help="download build + install prereqs + shortcuts + env + firewall")
    p_install.add_argument("--manual", action="store_true", help="write click-through guide instead of silent install")
    p_install.add_argument("--offline", action="store_true", help="don't download; use the installed build")
    p_install.add_argument("--force", action="store_true", help="re-download the build even if up to date")
    p_install.set_defaults(func=_install)

    p_update = sub.add_parser("update", help="download the newest build from GitHub if there is one")
    p_update.add_argument("--force", action="store_true", help="re-download even if up to date")
    p_update.set_defaults(func=_update)

    p_scripts = sub.add_parser("scripts", help="print the installed Content/Scripts folder")
    p_scripts.add_argument("--open", action="store_true", help="open it in Explorer")
    p_scripts.set_defaults(func=_scripts)

    p_dev = sub.add_parser("install-dev", help="install VS 2019 + build UE4.27.2 from source")
    p_dev.add_argument("--manual", action="store_true")
    p_dev.add_argument("--ue-dir", metavar="PATH", help=f"UE source clone dir (default: {config.DEV_BUILD_UE_DEFAULT_DIR})")
    p_dev.set_defaults(func=_install_dev)

    p_sc = sub.add_parser("install-shortcuts", help="re-create Desktop + Start Menu shortcuts")
    p_sc.set_defaults(func=_install_shortcuts)

    p_pr = sub.add_parser("install-prereqs", help="run UE4PrereqSetup_x64.exe silently")
    p_pr.set_defaults(func=_install_prereqs)

    p_env = sub.add_parser("install-env", help="re-apply STARCEL_HOME + PATH + long-path registry flag")
    p_env.set_defaults(func=_install_env)

    p_uninst = sub.add_parser("uninstall", help="remove shortcuts, env vars, firewall rule (asks before deleting files)")
    keep = p_uninst.add_mutually_exclusive_group()
    keep.add_argument("--delete-files", dest="delete_files", action="store_const", const=True, default=None,
                      help="also delete the install folder without asking")
    keep.add_argument("--keep-files", dest="delete_files", action="store_const", const=False,
                      help="keep the install folder without asking")
    p_uninst.set_defaults(func=_uninstall)

    p_cfg = sub.add_parser("config", help="view or edit launch settings")
    p_cfg_sub = p_cfg.add_subparsers(dest="config_action")
    p_cfg_sub.add_parser("show").set_defaults(func=_config_show)
    p_cfg_sub.add_parser("edit").set_defaults(func=_config_edit)
    p_cfg_sub.add_parser("reset").set_defaults(func=_config_reset)
    p_cfg_sub.add_parser("path").set_defaults(func=_config_path)

    sub.add_parser("version", help="show the package version, install location and installed build").set_defaults(func=_version)

    # --dir works before or after the subcommand: `starcel --dir D:\Starcel install`
    # or `starcel install --dir D:\Starcel`. SUPPRESS keeps a subparser from
    # overwriting a value given at the top level.
    dir_help = (f"install location (default: {config.DEFAULT_INSTALL_ROOT}); "
                f"remembered for future runs via the {config.ENV_VAR_HOME} user variable")
    for parser in [p, *sub.choices.values(), *p_cfg_sub.choices.values()]:
        parser.add_argument("--dir", metavar="PATH", default=argparse.SUPPRESS, help=dir_help)

    return p


def _apply_dir(path: str) -> None:
    """Switch to `path` and remember it as the install location."""
    from . import env

    new_root = Path(path).expanduser().resolve()
    old_root = config.INSTALL_ROOT
    if new_root == old_root:
        return
    try:
        old_on_path = env.starcel_on_path()
        if old_on_path:
            env.remove_starcel_from_path()
        config.set_install_root(new_root)
        os.environ[config.ENV_VAR_HOME] = str(new_root)
        env.set_starcel_home()
        if old_on_path:
            env.prepend_starcel_to_path()
        env._broadcast_env_change()
        print(f"Starcel location set to {new_root} (remembered for future runs).")
    except OSError as exc:
        config.set_install_root(new_root)
        print(f"Using {new_root} for this run (could not save it: {exc}).")
    if (old_root / "release.json").exists():
        print(f"Note: the existing install in {old_root} was not moved. Move or delete it yourself "
              f"if you no longer need it.")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    argv = sys.argv[1:] if argv is None else argv
    args = parser.parse_args(argv)
    if getattr(args, "dir", None):
        _apply_dir(args.dir)
    if not getattr(args, "func", None):
        return _run_client(parser.parse_args(argv + ["run"]))
    return args.func(args) or 0


def main_run() -> int:
    return main(["run"] + sys.argv[1:])


def main_server() -> int:
    return main(["server"] + sys.argv[1:])


def main_editor() -> int:
    return main(["editor"] + sys.argv[1:])


_GUI = False


def _gui_message(text: str, *, error: bool = False) -> None:
    import ctypes
    flags = 0x10 if error else 0x40  # MB_ICONERROR / MB_ICONINFORMATION
    ctypes.windll.user32.MessageBoxW(None, text, "Starcel", flags | 0x10000)  # MB_SETFOREGROUND


def _gui_download_notice(release: dict) -> None:
    _gui_message(
        f"Downloading {release['name']} ({release['size'] / 1e9:.2f} GB).\n\n"
        f"Starcel will start automatically when the download finishes.\n"
        f"Progress is logged to {_gui_log_path()}."
    )


def _gui_log_path() -> Path:
    return config.INSTALL_ROOT / "starcelw.log"


def main_run_gui() -> int:
    """GUI-mode entry (starcelw.exe, run by pythonw with no console).

    pythonw sets sys.stdout/sys.stderr to None, so any print or progress bar
    would crash invisibly. Send output to starcelw.log and show errors in a dialog.
    """
    global _GUI
    _GUI = True
    log = None
    if sys.stdout is None or sys.stderr is None:
        try:
            config.INSTALL_ROOT.mkdir(parents=True, exist_ok=True)
            log = open(_gui_log_path(), "w", encoding="utf-8", buffering=1)
        except OSError:
            log = open(os.devnull, "w", encoding="utf-8")
        sys.stdout = sys.stdout or log
        sys.stderr = sys.stderr or log
    try:
        return main(["run"] + sys.argv[1:])
    except SystemExit as exc:
        if exc.code not in (None, 0):
            _gui_message(str(exc.code), error=True)
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        _gui_message(f"Starcel failed to start:\n\n{exc}\n\nDetails: {_gui_log_path()}", error=True)
        return 1
    finally:
        if log:
            log.flush()


if __name__ == "__main__":
    sys.exit(main())
