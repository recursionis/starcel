"""Typed launch options with 3-layer precedence: CLI > settings.ini > config defaults.

Each launch kind (client/server/editor) has a dataclass. Every UE command-line
flag that could be passed lives as a field on that dataclass. `to_ue_args()`
turns the dataclass into the actual list of strings UE4 understands.

load_options() merges the three layers:
  1. Factory defaults from config.CLIENT_DEFAULTS / SERVER_DEFAULTS / EDITOR_DEFAULTS
  2. User overrides from Documents\\Starcel\\settings.ini (if present)
  3. Per-run overrides from CLI args

Precedence: CLI wins over INI wins over defaults.
"""
from __future__ import annotations

import configparser
from dataclasses import dataclass, field, fields, asdict
from pathlib import Path
from typing import Any, Mapping

from . import config


@dataclass
class ClientLaunchOptions:
    server_host: str | None = None
    res_x: int = 1600
    res_y: int = 900
    windowed: bool = True
    fullscreen: bool = False
    console: bool = True
    log: bool = True
    stdout: bool = True
    full_stdout: bool = True
    unattended: bool = False
    nullrhi: bool = False
    nosound: bool = False
    exec_cmds: str = ""
    log_cmds: str = ""
    abs_log: str = ""
    ini_overrides: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)

    def to_ue_args(self) -> list[str]:
        args: list[str] = []
        if self.server_host:
            args.append(self.server_host)
        if self.log:
            args.append("-log")
        if self.abs_log:
            args.append(f'-ABSLOG="{self.abs_log}"')
        if self.fullscreen:
            args.append("-fullscreen")
        elif self.windowed:
            args.append("-windowed")
        args += [f"-ResX={self.res_x}", f"-ResY={self.res_y}"]
        if self.console:
            args.append("-Console")
        if self.stdout:
            args.append("-stdout")
        if self.full_stdout:
            args.append("-FullStdOutLogOutput")
        if self.unattended:
            args.append("-unattended")
        if self.nullrhi:
            args.append("-nullrhi")
        if self.nosound:
            args.append("-nosound")
        if self.exec_cmds:
            args.append(f'-ExecCmds="{self.exec_cmds}"')
        if self.log_cmds:
            args.append(f'-LogCmds="{self.log_cmds}"')
        args += list(self.ini_overrides)
        args += list(self.extra_args)
        return args


@dataclass
class ServerLaunchOptions:
    port: int = 7827
    log: bool = True
    windowed: bool = True
    console: bool = True
    nullrhi: bool = True
    useperfcounters: bool = True
    unattended: bool = True
    exec_cmds: str = ""
    log_cmds: str = ""
    abs_log: str = ""
    ini_overrides: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)

    def to_ue_args(self) -> list[str]:
        args: list[str] = [f"-port={self.port}"]
        if self.log:
            args.append("-log")
        if self.abs_log:
            args.append(f'-ABSLOG="{self.abs_log}"')
        if self.windowed:
            args.append("-windowed")
        if self.console:
            args.append("-Console")
        if self.nullrhi:
            args.append("-nullrhi")
        if self.useperfcounters:
            args.append("-useperfcounters")
        if self.unattended:
            args.append("-unattended")
        if self.exec_cmds:
            args.append(f'-ExecCmds="{self.exec_cmds}"')
        if self.log_cmds:
            args.append(f'-LogCmds="{self.log_cmds}"')
        args += list(self.ini_overrides)
        args += list(self.extra_args)
        return args


@dataclass
class EditorLaunchOptions:
    abs_log: str = ""
    extra_args: list[str] = field(default_factory=list)

    def to_ue_args(self) -> list[str]:
        args: list[str] = []
        if self.abs_log:
            args.append(f'-ABSLOG="{self.abs_log}"')
        args += list(self.extra_args)
        return args


_KIND_MAP: dict[str, tuple[type, Mapping[str, Any]]] = {
    "client": (ClientLaunchOptions, config.CLIENT_DEFAULTS),
    "server": (ServerLaunchOptions, config.SERVER_DEFAULTS),
    "editor": (EditorLaunchOptions, config.EDITOR_DEFAULTS),
}


def _coerce(cls: type, key: str, raw: str) -> Any:
    """Convert an INI string to the type declared on the dataclass field."""
    annotation = {f.name: f.type for f in fields(cls)}.get(key)
    raw = raw.strip()
    if annotation is None:
        return raw
    if annotation == "bool":
        return raw.lower() in ("true", "yes", "1", "on")
    if annotation == "int":
        return int(raw)
    if annotation == "str":
        return raw
    if annotation == "str | None":
        return raw if raw else None
    if annotation == "list[str]":
        if not raw:
            return []
        if "," in raw:
            return [part.strip() for part in raw.split(",") if part.strip()]
        return raw.split()
    return raw


def _read_settings_section(kind: str) -> dict[str, Any]:
    """Load [kind] section from Documents\\Starcel\\settings.ini."""
    path = config.USER_SETTINGS_FILE
    if not path.exists():
        return {}
    parser = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    parser.read(path, encoding="utf-8")
    if not parser.has_section(kind):
        return {}
    cls = _KIND_MAP[kind][0]
    out: dict[str, Any] = {}
    for key, value in parser[kind].items():
        out[key] = _coerce(cls, key, value)
    return out


def load_options(kind: str, cli_overrides: Mapping[str, Any] | None = None):
    """Merge defaults < settings.ini < CLI overrides into a typed options dataclass."""
    if kind not in _KIND_MAP:
        raise ValueError(f"Unknown launch kind: {kind!r}. Expected one of {list(_KIND_MAP)}.")
    cls, defaults = _KIND_MAP[kind]
    merged: dict[str, Any] = dict(defaults)
    merged.update(_read_settings_section(kind))
    if cli_overrides:
        merged.update({k: v for k, v in cli_overrides.items() if v is not None})
    valid_keys = {f.name for f in fields(cls)}
    filtered = {k: v for k, v in merged.items() if k in valid_keys}
    return cls(**filtered)


def show_effective_config() -> str:
    """Return a human-readable dump of all three kinds' merged effective config."""
    lines: list[str] = []
    for kind in ("client", "server", "editor"):
        opts = load_options(kind)
        lines.append(f"[{kind}]")
        for k, v in asdict(opts).items():
            lines.append(f"  {k} = {v!r}")
        lines.append(f"  # resolves to UE args: {' '.join(opts.to_ue_args()) or '(none)'}")
        lines.append("")
    lines.append(f"settings file: {config.USER_SETTINGS_FILE}  "
                 f"({'exists' if config.USER_SETTINGS_FILE.exists() else 'not created yet'})")
    return "\n".join(lines)
