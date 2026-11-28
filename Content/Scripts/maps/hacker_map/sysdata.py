"""
sysdata.py — live system data for HackerMap (the sysmon, in numbers).

Launches Scripts/sysinfo_worker.py in --json mode with an external Python
(same interpreter discovery as actors/pyactor_sysmon.py — never
sys.executable, which inside UE is the editor) and reads its snapshot file
twice a second. Keeps ring buffers for the graphs:

    cpu_a / cpu_b   average % of the first / second half of the cores
                    (the video's "#1-2" and "#3-4" graphs)
    net_up / net_down   bytes per second
    mem             % used

If the worker can't start (no external Python / psutil), a light fallback
fills the same fields from the stdlib so the map still animates.
"""

import json
import os
import subprocess
import time
from collections import deque
from pathlib import Path

import unreal_engine as ue

HISTORY = 120
READ_INTERVAL = 0.5

_DATA_DIR = Path(os.environ.get('APPDATA', str(Path.home()))) / 'sysinfo'
JSON_PATH = _DATA_DIR / 'hackermap_sysdata.json'
_PID_FILE = _DATA_DIR / 'sysmon_json_worker.pid'
_SCRIPTS = Path(__file__).resolve().parent.parent.parent
_WORKER = _SCRIPTS / 'sysinfo_worker.py'


def _find_python():
    try:
        from actors.pyactor_sysmon import _find_python as fp
        return fp()
    except Exception:
        import shutil
        for name in ('python', 'python3', 'py'):
            p = shutil.which(name)
            if p and 'ue4editor' not in p.lower():
                return p
    return None


def _kill_prior():
    try:
        pid = int(_PID_FILE.read_text().strip())
    except Exception:
        return
    try:
        subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
                       timeout=3)
    except Exception:
        pass


def human_bytes(n, suffix='B'):
    n = float(n or 0)
    for unit in ('', 'K', 'M', 'G', 'T'):
        if abs(n) < 1024.0:
            return f'{n:.1f}{unit}{suffix}' if unit else f'{n:.0f}{suffix}'
        n /= 1024.0
    return f'{n:.1f}P{suffix}'


def fmt_uptime(sec):
    sec = int(sec or 0)
    d, rem = divmod(sec, 86400)
    h, rem = divmod(rem, 3600)
    m, s = divmod(rem, 60)
    return f'{d}d {h:02d}:{m:02d}' if d else f'{h:02d}:{m:02d}:{s:02d}'


class SysData:
    def __init__(self):
        self.snap = {}
        self.static = {}
        self.cpu_a = deque([0.0] * HISTORY, maxlen=HISTORY)
        self.cpu_b = deque([0.0] * HISTORY, maxlen=HISTORY)
        self.net_up = deque([0.0] * HISTORY, maxlen=HISTORY)
        self.net_down = deque([0.0] * HISTORY, maxlen=HISTORY)
        self.mem = deque([0.0] * HISTORY, maxlen=HISTORY)
        self.proc = None
        self._acc = 0.0
        self._last_t = 0.0
        self.version = 0          # bumps every new snapshot
        self.cpu_min = None
        self.cpu_max = None

    # worker lifecycle

    def start(self):
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        _kill_prior()
        py = _find_python()
        if py is None or not _WORKER.exists():
            ue.log_warning('hacker_map.sysdata: no external Python — using fallback data')
            return
        try:
            self.proc = subprocess.Popen(
                [py, str(_WORKER), '--json', str(JSON_PATH), '--interval', '0.5',
                 '--parent-pid', str(os.getpid())],
                cwd=str(_SCRIPTS),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            ue.log(f'hacker_map.sysdata: worker started (pid {self.proc.pid})')
        except Exception as e:
            ue.log_warning(f'hacker_map.sysdata: worker launch failed: {e}')
            self.proc = None

    def stop(self):
        if self.proc is not None:
            try:
                self.proc.terminate()
            except Exception:
                pass
            self.proc = None

    # polling

    def tick(self, dt):
        self._acc += dt
        if self._acc < READ_INTERVAL:
            return False
        self._acc = 0.0
        snap = None
        try:
            snap = json.loads(JSON_PATH.read_text(encoding='utf-8'))
        except Exception:
            snap = None
        if snap is None or snap.get('t', 0) == self._last_t:
            # no fresh worker data: fall back when there is no worker, or
            # when it has produced nothing for 5 s (crashed / no psutil)
            stale = time.time() - (self._last_t or 0) > 5.0
            if self.proc is None or (stale and not self.snap):
                snap = self._fallback()
            else:
                return False
        self._last_t = snap.get('t', time.time())
        self._ingest(snap)
        return True

    def _ingest(self, snap):
        self.snap = snap
        self.static = snap.get('static', self.static) or self.static
        cores = snap.get('cpu_per_core') or [0.0]
        half = max(1, len(cores) // 2)
        a = sum(cores[:half]) / half
        b = sum(cores[half:]) / max(1, len(cores) - half) if len(cores) > 1 else a
        self.cpu_a.append(a)
        self.cpu_b.append(b)
        net = snap.get('net', {})
        self.net_up.append(float(net.get('up_bps', 0.0)))
        self.net_down.append(float(net.get('down_bps', 0.0)))
        self.mem.append(float(snap.get('mem', {}).get('pct', 0.0)))
        f = snap.get('cpu_freq_ghz')
        if f:
            self.cpu_min = f if self.cpu_min is None else min(self.cpu_min, f)
            self.cpu_max = f if self.cpu_max is None else max(self.cpu_max, f)
        self.version += 1

    def _fallback(self):
        """Stdlib-only snapshot: wobbling values so the panels still move."""
        import math
        import platform
        import socket
        import shutil
        t = time.time()
        n = os.cpu_count() or 4
        cores = [max(0.0, 25 + 20 * math.sin(t * 0.7 + i)) for i in range(n)]
        try:
            du = shutil.disk_usage(os.path.expanduser('~'))
            disk = {'path': os.path.splitdrive(os.path.expanduser('~'))[0] or '/',
                    'pct': 100.0 * du.used / du.total, 'used': du.used, 'total': du.total}
        except Exception:
            disk = {}
        return {
            't': t,
            'static': self.static or {
                'hostname': socket.gethostname(),
                'user': os.environ.get('USERNAME', 'user'),
                'os': f'{platform.system()} {platform.release()}',
                'arch': platform.machine(), 'cpu_name': platform.processor(),
                'cores_logical': n, 'gpu': '', 'resolution': '',
                'boot_time': t - 3600, 'mem_total': 0},
            'cpu_per_core': cores, 'tasks': 0,
            'mem': {'pct': 40 + 5 * math.sin(t * 0.2), 'used': 0, 'total': 0},
            'net': {'up_bps': 2e4 * (1 + math.sin(t)), 'down_bps': 6e4 * (1 + math.sin(t * 1.3)),
                    'ip': '127.0.0.1', 'ping_ms': None, 'online': False},
            'uptime_sec': 3600 + t % 3600, 'processes': [], 'disk': disk,
        }

    # convenience getters for the panels

    def get(self, *path, default=None):
        d = self.snap
        for p in path:
            if not isinstance(d, dict) or p not in d:
                return default
            d = d[p]
        return d

    @property
    def user(self):
        return self.static.get('user') or os.environ.get('USERNAME', 'user')

    @property
    def host(self):
        return self.static.get('hostname') or 'starcel'

    @property
    def resolution(self):
        r = self.static.get('resolution') or ''
        parts = [p.strip() for p in r.split(',') if p.strip() and 'None' not in p]
        return ', '.join(parts) or '1920x1080'
