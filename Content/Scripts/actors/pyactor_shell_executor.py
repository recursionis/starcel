import unreal_engine as ue


# Python proxy for ue_spawn.spawn_focused_shell_executor — a focused Text3D
# command line. Same structure as PyActorText3DExecutor (BP_PyActorEmpty
# parent + BP_Cell Text3D child at parent.text3d_actor), but the text is a
# SHELL command instead of Python:
#
#   Enter        run the line (the typing system inserts '\n'; we take the
#                line, clear the input and hand it to the shell)
#   Shift+Enter  same as Enter (single-line prompt)
#   Ctrl+Enter   same as Enter
#   Up / Down    walk command history
#
# Who runs the command: if the parent has a ``shell`` attribute (set after
# spawn, read on first tick) with a ``run(cmd)`` method, it gets the line —
# HackerMap's terminal uses this for built-ins, PowerShell and output
# display. Without one, the command runs in PowerShell and the output goes
# to the log.


from actors.pyactor_text3d_executor import PyActorText3DExecutor


class PyActorShellExecutor(PyActorText3DExecutor):
    """Text3D prompt that runs its line as a shell command on Enter."""

    VK_UP = 0x26
    VK_DOWN = 0x28
    MAX_HISTORY = 200

    def begin_play(self):
        super().begin_play()
        self.shell = None
        self.history = []
        self._hist_idx = None
        self._prev_up = False
        self._prev_down = False

    def tick(self, dt):
        first = self._first_tick
        super().tick(dt)
        if first:
            self.shell = getattr(self.uobject, 'shell', None)
        if self._text3d_actor is None:
            return

        text = self._get_text()
        if '\n' in text:
            self._submit(text.replace('\r', '').replace('\n', ''))
            return

        if self._win32_ok and self._is_focused():
            up = bool(self._user32.GetAsyncKeyState(self.VK_UP) & 0x8000)
            down = bool(self._user32.GetAsyncKeyState(self.VK_DOWN) & 0x8000)
            if up and not self._prev_up:
                self._history_step(-1)
            elif down and not self._prev_down:
                self._history_step(+1)
            self._prev_up, self._prev_down = up, down

    # text helpers

    def _t3d(self):
        try:
            return self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
        except Exception:
            return None

    def _get_text(self):
        t3d = self._t3d()
        try:
            return str(t3d.Text or '') if t3d is not None else ''
        except Exception:
            return ''

    def set_text(self, text, caret_to_end=True):
        t3d = self._t3d()
        if t3d is None:
            return
        t3d.Text = text
        if caret_to_end:
            try:
                from actors.pyactor_text3d import PyActorText3D
                if PyActorText3D._get_focused() is self._text3d_actor:
                    PyActorText3D._string_idx = PyActorText3D._anchor = len(text)
                    PyActorText3D._hide_highlights()
                    if text:
                        self._reshow_caret()
                    else:
                        self._park_caret()
            except Exception:
                pass

    def _park_caret(self):
        """Empty text has no glyphs to anchor the caret — park it at the
        Text3D origin (same fallback as spawn_focused_text3d_executor)."""
        try:
            from unreal_engine import FVector
            from actors.pyactor_text3d import PyActorText3D
            proxy = PyActorText3D._get_or_spawn_cursor(self._text3d_actor)
            if proxy is not None:
                s = self._text3d_actor.get_actor_scale()
                proxy.move_to(self._text3d_actor.get_actor_location(),
                              FVector(0.01, 0.04 * s.y, 0.5 * s.z),
                              self._text3d_actor.get_actor_rotation())
        except Exception:
            pass

    def _is_focused(self):
        try:
            from actors.pyactor_text3d import PyActorText3D
            return PyActorText3D._get_focused() is self._text3d_actor
        except Exception:
            return False

    # running

    def _run_code(self, trigger='?'):
        """Ctrl+Enter / click from the base class -> same as Enter."""
        if trigger == 'click':
            return          # clicking the prompt should focus it, not run it
        self._submit(self._get_text())

    def _submit(self, line):
        cmd = line.strip()
        self.set_text('')
        self._hist_idx = None
        if not cmd:
            return
        if not self.history or self.history[-1] != cmd:
            self.history.append(cmd)
            del self.history[:-self.MAX_HISTORY]
        if self.shell is not None and hasattr(self.shell, 'run'):
            try:
                self.shell.run(cmd)
            except Exception as e:
                ue.log_warning(f'PyActorShellExecutor: shell.run failed: {e}')
            return
        self._run_default(cmd)

    def _run_default(self, cmd):
        import subprocess
        import threading

        def work():
            try:
                out = subprocess.run(
                    ['powershell', '-NoProfile', '-NonInteractive', '-Command', cmd],
                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                    timeout=60, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                ue.log(f'$ {cmd}\n{out.stdout}{out.stderr}')
            except Exception as e:
                ue.log_warning(f'PyActorShellExecutor: {e}')
        threading.Thread(target=work, daemon=True).start()

    def _history_step(self, direction):
        if not self.history:
            return
        if self._hist_idx is None:
            self._hist_idx = len(self.history)
        self._hist_idx = max(0, min(len(self.history), self._hist_idx + direction))
        text = self.history[self._hist_idx] if self._hist_idx < len(self.history) else ''
        self.set_text(text)
