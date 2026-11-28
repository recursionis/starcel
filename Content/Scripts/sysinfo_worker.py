"""
sysinfo_worker.py
=================
Background daemon that periodically calls sysinfo.get_info_string() and writes
the result to a text file. Spawned by pyactor_sysmon.py via subprocess.Popen
against an external system Python interpreter, so the heavy WMI / PowerShell /
HTTP collection work doesn't block the UE thread.

Run:
    python sysinfo_worker.py [--parent-pid PID] [--interval SECS]
                             [--mode MODE] [--units UNITS]
                             [--json PATH]

Exits when --parent-pid is no longer alive (so workers don't leak if the
editor crashes) or on SIGTERM / SIGINT.

Writes:
    {APPDATA}/sysinfo/sysmon_text.txt    formatted display string
    {APPDATA}/sysinfo/sysmon_worker.pid  own PID (cleared on graceful exit)

--json mode (used by maps.hacker_map.sysdata) instead writes a small,
fast numeric snapshot every --interval seconds (0.5 s is fine): per-core
CPU %, memory, network bytes/s, top processes, uptime, IPv4, ping, disk.
It only touches psutil/stdlib per tick (static facts like CPU/GPU names
are collected once at start), and uses its own PID file so it can run
next to the text worker.
"""

from __future__ import annotations

import argparse
import os
import platform
import signal
import sys
import time
from pathlib import Path

import psutil

# sysinfo.py / activity_tracker.py live in the same directory. Make sure
# they import even if cwd is somewhere else.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sysinfo import get_info_string  # noqa: E402


def _data_dir() -> Path:
    p = platform.system()
    if p == "Windows":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif p == "Darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    d = base / "sysinfo"
    d.mkdir(parents=True, exist_ok=True)
    return d


DATA_DIR = _data_dir()
RESULT_FILE = DATA_DIR / "sysmon_text.txt"
PID_FILE = DATA_DIR / "sysmon_worker.pid"


def _write_atomic(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _format(mode: str, units: str) -> str:
    """sysinfo string + optional activity_tracker APM line — matches the
    original PyActorSysmon._update() output exactly."""
    parts = []
    try:
        s = get_info_string(mode=mode, units=units)
        if s:
            parts.append(s.strip())
    except Exception as e:
        parts.append(f"[sysinfo error: {e}]")

    try:
        from activity_tracker import read_stats
        stats = read_stats()
        if stats:
            parts.append(
                f"APM: {stats.get('actions_per_min', 0.0):.1f}  "
                f"Clicks/min: {stats.get('clicks_per_min', 0.0):.1f}  "
                f"Keys/min: {stats.get('keys_per_min', 0.0):.1f}  "
                f"Mouse px: {stats.get('mouse_distance_px', 0.0):.0f}"
            )
    except Exception:
        pass

    return "\n".join(parts) if parts else "(no data)"


def _clear_pid_if_ours() -> None:
    try:
        if PID_FILE.exists() and int(PID_FILE.read_text().strip()) == os.getpid():
            PID_FILE.unlink()
    except Exception:
        pass


def _shutdown(*_):
    _clear_pid_if_ours()
    sys.exit(0)


JSON_PID_FILE = DATA_DIR / "sysmon_json_worker.pid"


def _static_info() -> dict:
    """Slow, unchanging facts — collected once per worker start."""
    import socket
    out = {
        "hostname": socket.gethostname(),
        "user": os.environ.get("USERNAME") or os.environ.get("USER") or "user",
        "os": f"{platform.system()} {platform.release()}",
        "os_version": platform.version(),
        "arch": platform.machine(),
        "cpu_name": platform.processor(),
        "cores_logical": psutil.cpu_count(logical=True),
        "cores_physical": psutil.cpu_count(logical=False),
        "mem_total": psutil.virtual_memory().total,
        "gpu": "",
        "resolution": "",
        "boot_time": psutil.boot_time(),
    }
    try:
        import sysinfo
        sysinfo._MINIMAL = True
        cpu = sysinfo._collect_cpu("usa")
        out["cpu_name"] = cpu.get("cpu_name") or out["cpu_name"]
        out["clock_max_ghz"] = cpu.get("base_clock_ghz")
    except Exception:
        pass
    try:
        import sysinfo
        gpus = sysinfo._collect_gpu("usa")
        if gpus:
            out["gpu"] = gpus[0].get("name", "")
    except Exception:
        pass
    try:
        import sysinfo
        disp = sysinfo._collect_display()
        if disp:
            out["resolution"] = ", ".join(d.get("resolution", "") for d in disp[:3])
    except Exception:
        pass
    return out


def _ipv4() -> str:
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))      # no packets sent for UDP connect
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"


def _ping_ms(host: str = "1.1.1.1", port: int = 443, timeout: float = 1.0):
    """TCP connect round-trip in ms (no ICMP privileges needed)."""
    import socket
    t0 = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            pass
        return round((time.perf_counter() - t0) * 1000.0, 1)
    except Exception:
        return None


def _top_processes(n: int = 6) -> list:
    procs = []
    ncpu = psutil.cpu_count(logical=True) or 1
    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            cpu = p.cpu_percent(None) / ncpu      # primed on the previous tick
            procs.append({"pid": p.info["pid"], "name": p.info["name"] or "?",
                          "cpu": round(cpu, 1),
                          "mem": round(p.info["memory_percent"] or 0.0, 1)})
        except Exception:
            continue
    procs.sort(key=lambda d: d["cpu"], reverse=True)
    return [d for d in procs if d["name"] not in ("System Idle Process", "Idle")][:n]


def _temperature():
    try:
        temps = psutil.sensors_temperatures()   # not on Windows psutil
        vals = [e.current for entries in temps.values() for e in entries]
        return round(sum(vals) / len(vals), 1) if vals else None
    except Exception:
        return None


def _json_loop(args, json_path: Path, parent) -> None:
    import json
    static = _static_info()
    last_net = psutil.net_io_counters()
    last_t = time.time()
    ip, ping, last_slow = _ipv4(), _ping_ms(), 0.0
    psutil.cpu_percent(percpu=True)
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except Exception:
            pass
    procs, last_procs = [], 0.0
    while True:
        if parent is not None and not psutil.pid_exists(parent):
            _shutdown_json()
        time.sleep(max(0.1, args.interval))
        now = time.time()
        dt = max(1e-3, now - last_t)
        net = psutil.net_io_counters()
        up = (net.bytes_sent - last_net.bytes_sent) / dt
        down = (net.bytes_recv - last_net.bytes_recv) / dt
        last_net, last_t = net, now
        if now - last_slow > 5.0:
            ip, ping, last_slow = _ipv4(), _ping_ms(), now
        if now - last_procs > 2.0:
            procs, last_procs = _top_processes(), now
        vm = psutil.virtual_memory()
        try:
            disk = psutil.disk_usage(os.path.expanduser("~"))
            disk_d = {"path": os.path.splitdrive(os.path.expanduser("~"))[0] or "/",
                      "pct": disk.percent, "used": disk.used, "total": disk.total}
        except Exception:
            disk_d = {}
        freq = None
        try:
            f = psutil.cpu_freq()
            freq = round(f.current / 1000.0, 2) if f else None
        except Exception:
            pass
        snap = {
            "t": now,
            "static": static,
            "cpu_per_core": psutil.cpu_percent(percpu=True),
            "cpu_freq_ghz": freq,
            "cpu_temp_c": _temperature(),
            "tasks": len(psutil.pids()),
            "mem": {"pct": vm.percent, "used": vm.used, "total": vm.total},
            "net": {"up_bps": up, "down_bps": down,
                    "sent": net.bytes_sent, "recv": net.bytes_recv,
                    "ip": ip, "ping_ms": ping, "online": ping is not None},
            "uptime_sec": now - static["boot_time"],
            "battery": None,
            "processes": procs,
            "disk": disk_d,
        }
        try:
            b = psutil.sensors_battery()
            if b is not None:
                snap["battery"] = {"pct": b.percent, "plugged": b.power_plugged}
        except Exception:
            pass
        try:
            _write_atomic(json_path, json.dumps(snap))
        except Exception:
            pass


def _shutdown_json(*_):
    try:
        if JSON_PID_FILE.exists() and int(JSON_PID_FILE.read_text().strip()) == os.getpid():
            JSON_PID_FILE.unlink()
    except Exception:
        pass
    sys.exit(0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent-pid", type=int, default=None)
    ap.add_argument("--interval",   type=float, default=300.0)
    ap.add_argument("--mode",       default="minimal")
    ap.add_argument("--units",      default="usa")
    ap.add_argument("--json",       default=None,
                    help="write fast numeric JSON snapshots to this path")
    args = ap.parse_args()

    if args.json:
        JSON_PID_FILE.write_text(str(os.getpid()))
        signal.signal(signal.SIGINT,  _shutdown_json)
        signal.signal(signal.SIGTERM, _shutdown_json)
        _json_loop(args, Path(args.json), args.parent_pid)
        return 0

    PID_FILE.write_text(str(os.getpid()))

    signal.signal(signal.SIGINT,  _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    parent = args.parent_pid

    while True:
        if parent is not None and not psutil.pid_exists(parent):
            _shutdown()

        _write_atomic(RESULT_FILE, _format(args.mode, args.units))

        # Sleep in small chunks so we exit promptly when the parent dies.
        slept = 0.0
        while slept < args.interval:
            chunk = min(2.0, args.interval - slept)
            time.sleep(chunk)
            slept += chunk
            if parent is not None and not psutil.pid_exists(parent):
                _shutdown()


if __name__ == "__main__":
    sys.exit(main())
