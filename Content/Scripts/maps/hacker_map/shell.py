"""
shell.py — TERMINAL / MAIN SHELL panel.

  prompt      ue_spawn.spawn_focused_shell_executor: a focused Text3D line
              (actors.pyactor_shell_executor). Enter hands the line to
              TerminalPanel.run().
  output      a ring of Text3D line actors. Scrolling re-poses the actors
              instead of retyping every line, so only new lines rebuild
              glyphs.
  commands    built-ins: neofetch, clear/cls, cd, pwd, py <python>, help,
              exit. Anything else runs in PowerShell on a worker thread;
              stdout/stderr stream back into the output.
  neofetch    BP_StarcelLogo (green, spinning on its own) where Debian's
              swirl was, system info from SysData beside it, then a row of
              green swatches.
"""

import datetime
import io
import os
import queue
import subprocess
import threading
import traceback
from contextlib import redirect_stdout, redirect_stderr

import unreal_engine as ue
from unreal_engine import FVector

from maps.hacker_map import theme, ui, layout
from maps.hacker_map.panels import BasePanel
from maps.hacker_map.sysdata import fmt_uptime
from maps.hacker_map.theme import S, U, rot

LOGO_BP = '/Game/Blueprints/Assets/BP_StarcelLogo.BP_StarcelLogo'

OUT_U, OUT_V = 14, 56          # output area top-left (panel px)
LINE_PX = 21.0                 # line pitch
FONT_PX = 12.5
N_LINES = 24
MAX_COLS = 150
PROMPT_V = OUT_V + N_LINES * LINE_PX + 8
NEO_INDENT = 300               # neofetch info column (logo sits left of it)
NEO_LINES = 14
PROMPT_FONT = FONT_PX * 1.05
CHAR_ADVANCE = 0.8             # Text3D (SourceCodePro) advance / glyph height
# The logo sits this far BEHIND the terminal plane (fraction of the camera
# distance) and is scaled up by the same perspective factor, so it reads at
# the right size on screen but has real depth behind the text.
LOGO_BACK = 0.6


def _clean(s):
    s = s.replace('\t', '    ').replace('\r', '')
    s = ''.join(ch if 32 <= ord(ch) < 127 else '?' for ch in s)
    return s[:MAX_COLS]


class TerminalPanel(BasePanel):
    LEFT, RIGHT = 'TERMINAL', 'MAIN SHELL'

    def __init__(self, key='terminal'):
        super().__init__(key)
        self.entries = []          # [text, indent_px, tag]
        self.pool = []             # Text3D line actors
        self._pool_text = {}       # id(actor) -> text shown
        self._dirty = False
        self._q = queue.Queue()
        self._proc_thread = None
        self.cwd = os.path.expanduser('~')
        self.logo = None
        self._logo_entry = None
        self.prompt = None
        self.welcome = None
        self._typing = None        # (text, index, timer, on_done)
        self.scroll_lines = 0      # mouse-wheel scrollback (lines above the bottom)

    def build_steps(self):
        return [self._build_base, self._build_frame, self._build_pool, self._build_prompt]

    # black face pushed back behind the logo (see BasePanel.backdrop)
    BACKDROP_BACK = layout.WALL_X * LOGO_BACK * 1.5

    # building

    def _build_frame(self):
        self.frame(0, 0, self.w, self.h, 1.2, theme.GLOW_LINE * 0.7)
        self.head1 = self.text('', 10, 8, 9.5, theme.GLOW_SOFT)
        self.head2 = self.text('', 10, 26, 9.5, theme.GLOW_SOFT)
        self.clock = self.text('', self.w - 250, 26, 9.5, theme.GLOW_SOFT)
        self.bar(0, PROMPT_V - 6, self.w, PROMPT_V - 6, 0.6, theme.GLOW_SOFT, theme.GREEN_DIM)

    def _build_pool(self):
        for i in range(N_LINES):
            a = self.text(' ', OUT_U, OUT_V + i * LINE_PX, FONT_PX)
            self.pool.append(a)
            self._pool_text[id(a)] = ' '

    def _build_prompt(self):
        from ue_spawn import spawn_focused_shell_executor
        self._prompt_label = '~ >'
        self.prompt_lbl = self.text(self._prompt_label, OUT_U, PROMPT_V, PROMPT_FONT,
                                    theme.GLOW_TEXT * 1.3)
        s = FONT_PX * S / theme.TEXT_H
        self.prompt = spawn_focused_shell_executor(
            '', location=self.at(self._prompt_u(), PROMPT_V), rotation=rot(),
            scale=FVector(s, s, s), shell=self, focus=False, name='HM_Shell')
        if self.prompt is not None:
            self.add(self.prompt)
            child = getattr(self.prompt, 'text3d_actor', None)
            if child is not None:
                theme.glow_text(child, theme.GLOW_TEXT * 1.3, theme.GREEN_HOT)
                self.track(child)

    def _prompt_u(self):
        """Input starts one character after the '<folder> >' label."""
        return OUT_U + (len(self._prompt_label) + 1) * PROMPT_FONT * CHAR_ADVANCE

    def _set_prompt_label(self, label):
        if label == self._prompt_label:
            return
        self._prompt_label = label
        ui.set_text(self.prompt_lbl, label)
        if self.prompt is not None:
            ui.set_rel(self.prompt, ui.rel(self._prompt_u(), PROMPT_V))

    def focus_prompt(self):
        """Give the shell keyboard focus (caret at the end). Done twice:
        the typing system may only come online on the next frame."""
        child = getattr(self.prompt, 'text3d_actor', None) if self.prompt else None
        if child is not None:
            from ue_spawn import focus_text3d
            focus_text3d(child, 0.05, 'hacker_map: shell focused')
            focus_text3d(child, 0.6, 'hacker_map: shell focused')

    # output

    def write(self, text, indent=0, tag=None):
        for line in str(text).split('\n'):
            self.entries.append([_clean(line), indent, tag])
        if len(self.entries) > 2000:
            drop = len(self.entries) - 2000
            del self.entries[:drop]
            if self._logo_entry is not None:
                self._logo_entry -= drop
        self._dirty = True

    def clear(self):
        self.entries = []
        self._destroy_logo()
        self._dirty = True

    def _render(self):
        self._dirty = False
        n = len(self.entries)
        first = self._first_line()
        for row in range(N_LINES):
            i = first + row
            a = self.pool[i % N_LINES] if self.pool else None
            if a is None:
                continue
            if i < n:
                text, indent, _ = self.entries[i]
            else:
                text, indent = ' ', 0
            shown = text or ' '
            if self._pool_text.get(id(a)) != shown:
                ui.set_text(a, shown)
                self._pool_text[id(a)] = shown
            ui.set_rel(a, ui.rel(OUT_U + indent, OUT_V + row * LINE_PX))
        self._place_logo(first)

    # logo (neofetch)

    def _spawn_logo(self, entry_index):
        self._destroy_logo()
        from ue_spawn import spawn_blueprint
        size = NEO_LINES * LINE_PX * 0.92 * S          # target size in UU
        try:
            logo = spawn_blueprint(LOGO_BP, FVector(0, 0, -100000), rot(), FVector(1, 1, 1))
        except Exception as e:
            theme.warn(f'BP_StarcelLogo spawn failed: {e}')
            return
        if logo is None:
            return
        # every cylinder + sphere gets the green glow material (replacing
        # M_SunGlow); re-pushed for ~2 s in case the Blueprint resets it
        theme.glow(logo, theme.GLOW_LINE * 0.6, theme.GREEN)
        theme.mark_dirty(logo, frames=(2, 10, 30, 60, 120))
        try:
            logo.SetActorEnableCollision(False)
        except Exception:
            pass
        # scale to fit and remember the bounds centre offset
        try:
            origin, extent = logo.GetActorBounds()
            loc = logo.get_actor_location()
            big = max(extent.y, extent.z, extent.x, 1.0) * 2.0
            k = size / big
            # pivot -> bounds-centre offset at scale 1
            self._logo_off = FVector(loc.x - origin.x, loc.y - origin.y, loc.z - origin.z)
        except Exception:
            k = 1.0
            self._logo_off = FVector(0, 0, 0)
        self._logo_k = k
        logo.set_actor_scale(FVector(k, k, k))
        self.add(logo)
        self.logo = logo
        self._logo_entry = entry_index
        self._dirty = True

    def _place_logo(self, first):
        if self.logo is None or self._logo_entry is None:
            return
        row = self._logo_entry - first
        visible = -NEO_LINES < row < N_LINES and self.revealed
        if not visible:
            self.suppress(self.logo, True)
            return
        self.suppress(self.logo, False)
        cu = OUT_U + NEO_INDENT / 2.0 - 10
        cv = OUT_V + (row + NEO_LINES / 2.0) * LINE_PX
        # where it should appear on the panel, then pushed far back
        p, kp = layout.push_back(self.at(cu, cv, depth=0.0), layout.WALL_X * LOGO_BACK)
        k = self._logo_k * kp
        o = self._logo_off
        self.logo.set_actor_scale(FVector(k, k, k))
        self.logo.set_actor_location(FVector(p.x + o.x * k, p.y + o.y * k, p.z + o.z * k))

    def _destroy_logo(self):
        if self.logo is not None:
            try:
                self.parts.remove(self.logo)
            except ValueError:
                pass
            ui.destroy(self.logo)
        self.logo = None
        self._logo_entry = None

    # commands

    def _first_line(self):
        n = len(self.entries)
        self.scroll_lines = max(0, min(self.scroll_lines, n - N_LINES))
        return max(0, n - N_LINES - self.scroll_lines)

    def scroll(self, steps):
        """Mouse wheel: +steps scrolls back through output, - forward."""
        before = self.scroll_lines
        self.scroll_lines = max(0, self.scroll_lines + steps * 3)
        if self._first_line() is not None and self.scroll_lines != before:
            self._dirty = True

    def run(self, cmd):
        self.scroll_lines = 0          # jump back to the bottom on a new command
        self.write(f'~ > {cmd}')
        name, _, arg = cmd.partition(' ')
        low = name.lower()
        if low in ('clear', 'cls'):
            self.clear()
        elif low == 'neofetch':
            self.neofetch()
        elif low == 'cd':
            self._cd(arg.strip())
        elif low == 'pwd':
            self.write(self.cwd)
        elif low == 'help':
            self.write('built-ins: neofetch  clear  cd <dir>  pwd  py <python>  exit')
            self.write('anything else runs in PowerShell (in the current directory)')
            self.write('F4 graphs 3D/2D   F5 replay boot   F6 colour preset   M cursor   click a key: its Starcel use')
        elif low == 'py':
            self._py(arg)
        elif low == 'exit':
            from actors.pyactor_text3d import PyActorText3D
            PyActorText3D._unfocus()
        else:
            self._powershell(cmd)

    def _cd(self, path):
        target = os.path.expanduser(path or '~')
        if not os.path.isabs(target):
            target = os.path.join(self.cwd, target)
        target = os.path.normpath(target)
        if os.path.isdir(target):
            self.cwd = target
        else:
            self.write(f'cd: no such directory: {path}')

    def _py(self, code):
        buf = io.StringIO()
        env = {'ue': ue, 'terminal': self}
        try:
            with redirect_stdout(buf), redirect_stderr(buf):
                try:
                    res = eval(compile(code, '<shell>', 'eval'), env)
                    if res is not None:
                        print(repr(res))
                except SyntaxError:
                    exec(compile(code, '<shell>', 'exec'), env)
        except Exception:
            buf.write(traceback.format_exc(limit=2))
        out = buf.getvalue().rstrip()
        if out:
            self.write(out)

    def _powershell(self, cmd):
        if self._proc_thread is not None and self._proc_thread.is_alive():
            self.write('busy: previous command still running')
            return
        cwd = self.cwd

        def work():
            try:
                p = subprocess.Popen(
                    ['powershell', '-NoProfile', '-NonInteractive', '-Command',
                     f'{cmd} | Out-String -Width {MAX_COLS}'],
                    cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding='utf-8', errors='replace',
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                for line in p.stdout:
                    self._q.put(line.rstrip('\n'))
                p.wait(timeout=120)
            except Exception as e:
                self._q.put(f'error: {e}')
            self._q.put(None)

        self._proc_thread = threading.Thread(target=work, daemon=True)
        self._proc_thread.start()

    # neofetch

    def neofetch(self):
        d = self.data
        st = d.static if d is not None else {}
        mem = d.get('mem', default={}) if d is not None else {}
        used = (mem.get('used') or 0) // (1024 * 1024)
        total = (mem.get('total') or st.get('mem_total') or 0) // (1024 * 1024)
        user_host = f'{d.user}@{d.host}' if d is not None else 'user@starcel'
        lines = [
            user_host,
            '-' * len(user_host),
            f"OS: {st.get('os', 'Windows')} {st.get('arch', '')}",
            f"Kernel: {st.get('os_version', '')}",
            f"Uptime: {fmt_uptime(d.get('uptime_sec', default=0)) if d else '?'}",
            f"Shell: starcel-shell (PowerShell)",
            f"Resolution: {d.resolution if d else ''}",
            "WM: Unreal Engine 4.27",
            "Theme: HackerMap [green]",
            "Terminal: Starcel",
            f"CPU: {st.get('cpu_name', '?')} ({st.get('cores_logical', '?')})",
            f"GPU: {st.get('gpu', '?')}",
            f"Memory: {used}MiB / {total}MiB",
            '',
        ]
        start = len(self.entries)
        for ln in lines:
            self.write(ln, indent=NEO_INDENT, tag='neo')
        self._spawn_logo(start)
        self._spawn_swatches(start + len(lines) - 1)

    def _spawn_swatches(self, entry_index):
        """Eight green blocks (neofetch's colour row) as one Screen Cube."""
        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (8 * 32, 32), theme.PIL_CLEAR)
        dr = ImageDraw.Draw(img)
        for i in range(8):
            g = int(40 + 215 * i / 7)
            dr.rectangle((i * 32, 0, i * 32 + 31, 31), fill=(int(g * 0.25), g, int(g * 0.5), 255))
        self.entries[entry_index][0] = ' '
        self._swatch_entry = entry_index
        if getattr(self, 'swatches', None) is None:
            self.swatches = self.screen(img, OUT_U + NEO_INDENT, OUT_V, 8 * 18, 16,
                                        strength=theme.GLOW_LINE * 0.6)
        self._dirty = True

    # per-frame

    def tick(self, dt):
        super().tick(dt)
        drained = False
        while True:
            try:
                item = self._q.get_nowait()
            except queue.Empty:
                break
            drained = True
            if item is not None:
                self.write(item)
        if self._typing is not None:
            self._tick_typing(dt)
        if self._dirty or drained:
            self._render()
            self._place_swatches()

    def _place_swatches(self):
        sc = getattr(self, 'swatches', None)
        if sc is None:
            return
        n = len(self.entries)
        first = self._first_line()
        row = getattr(self, '_swatch_entry', -999) - first
        show = 0 <= row < N_LINES
        self.suppress(sc.actor, not show)
        if show:
            ui.set_rel(sc.actor, ui.rel(OUT_U + NEO_INDENT + 8 * 9, OUT_V + row * LINE_PX + 9))

    def update(self, data):
        st = data.static
        if hasattr(self, 'head1'):
            ui.set_text(self.head1, f"Starcel {data.host} {st.get('os', '')} {st.get('arch', '')}")
            load = data.cpu_a[-1], data.cpu_b[-1]
            ui.set_text(self.head2, f"{datetime.datetime.now():%H:%M:%S} up "
                                    f"{fmt_uptime(data.get('uptime_sec', default=0))}, 1 user, "
                                    f"load: {load[0]:.0f}%, {load[1]:.0f}%")
            ui.set_text(self.clock, f'{datetime.datetime.now():%a %d %b %Y %H:%M:%S}')
            self._set_prompt_label(f'{os.path.basename(self.cwd) or self.cwd} >')

    # scripted typing (boot sequence)

    def type_command(self, cmd, cps=9.0, on_done=None):
        """Type *cmd* into the prompt like a person, then run it."""
        self._typing = [cmd, 0, 0.0, cps, on_done, True]

    def _tick_typing(self, dt):
        cmd, i, t, cps, done, run = self._typing
        t += dt
        n = min(len(cmd), int(t * cps))
        child = getattr(self.prompt, 'text3d_actor', None) if self.prompt else None
        if child is not None:
            ui.set_text(child, cmd[:n] or '')
        if n >= len(cmd) and t * cps > len(cmd) + 3:
            self._typing = None
            if run:
                if child is not None:
                    ui.set_text(child, '')
                self.run(cmd)
            if done:
                done()
            return
        self._typing = [cmd, n, t, cps, done, run]

    def type_text(self, text, cps=7.0, on_done=None):
        """Type *text* into the prompt and leave it there (not run)."""
        self._typing = [text, 0, 0.0, cps, on_done, False]

    def finish_typing(self):
        if self._typing is not None:
            cmd, _, _, _, done, run = self._typing
            self._typing = None
            child = getattr(self.prompt, 'text3d_actor', None) if self.prompt else None
            if child is not None:
                ui.set_text(child, '' if run else cmd)
            if run:
                self.run(cmd)
            if done:
                done()

    # welcome text (boot)

    def show_welcome(self, user):
        if self.welcome is None:
            msg = f'Welcome back, {user}'
            size = 34.0
            self.welcome = self.text(msg, (self.w - len(msg) * size * 0.6) / 2.0,
                                     self.h / 2.0 - 60, size, theme.GLOW_TEXT * 1.5)

    def hide_welcome(self):
        if self.welcome is not None:
            try:
                self.parts.remove(self.welcome)
            except ValueError:
                pass
            ui.destroy(self.welcome)
            self.welcome = None
