import unreal_engine as ue


# Python proxy for spawn_text3d_executor — hosted on BP_PyActorEmpty, paired
# with a BP_Cell Text3D child set up by ue_spawn.spawn_text3d_pyactor.
#
# Spawn structure:
#   parent  = BP_PyActorEmpty (this proxy)
#   child   = BP_Cell  (attached to parent, exposed as parent.text3d_actor)
#
# Three ways to fire:
#   - Ctrl+Enter (rising edge) — Win32 GetAsyncKeyState polling, works
#     regardless of UE focus. Fires when this executor's text3d is the
#     globally-focused actor (PyActorGlobalClick) OR when no actor is
#     focused (so a freshly-spawned executor works without test_text3d_click
#     set up first).
#   - Shift+Enter (rising edge) — same polling/focus gating as Ctrl+Enter.
#     Jupyter parity: either chord runs the cell.
#   - Mouse click on the Text3D child (rising edge) — tick-based cursor
#     trace via click_helpers.cursor_hit_actor. No focus gating; clicking
#     directly is an unambiguous "run me now" gesture.
#
# Tick is force-enabled in begin_play so the polling runs even if the
# host BP forgot to flip bStartWithTickEnabled.


class PyActorText3DExecutor:
    """Run the BP_Cell child's text as Python on Ctrl+Enter, Shift+Enter, or click."""

    TEXT_COMPONENT_NAME = 'Text3DComponent'

    VK_CONTROL = 0x11
    VK_SHIFT = 0x10
    VK_RETURN = 0x0D

    def begin_play(self):
        # parent.text3d_actor is set by spawn_text3d_pyactor AFTER actor_spawn
        # returns from BeginPlay, so it's not visible here. Read on first tick.
        self._text3d_actor = None
        self._first_tick = True
        self._prev_ctrl_enter_down = False
        self._prev_shift_enter_down = False
        self._prev_mouse_down = False
        # Relayout-watch state: only armed briefly after a run (see
        # _arm_relayout_watch / _sync_caret_to_geometry).
        self._watch_relayout = False
        self._watch_idx = None
        self._geom_sig = None
        self._relayout_changed = False

        # Force tick on regardless of BP defaults — without this the Win32
        # poll never runs and Ctrl+Enter / Shift+Enter silently do nothing.
        try:
            self.uobject.set_actor_tick_enabled(True)
        except Exception as e:
            ue.log_warning(
                f'PyActorText3DExecutor: set_actor_tick_enabled failed ({e})')

        # Player controller for cursor trace + click event routing.
        self._player_controller = None
        try:
            from click_helpers import setup_player_controller
            self._player_controller = setup_player_controller(self.uobject)
        except Exception as e:
            ue.log_warning(
                f'PyActorText3DExecutor: player controller setup failed ({e}); '
                'click-to-run disabled.')

        self._win32_ok = False
        self._user32 = None
        try:
            import ctypes
            self._user32 = ctypes.WinDLL('user32', use_last_error=True)
            self._user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
            self._user32.GetAsyncKeyState.restype = ctypes.c_short
            self._win32_ok = True
        except Exception as e:
            ue.log_warning(
                f'PyActorText3DExecutor: ctypes init failed ({e}); '
                'Ctrl+Enter / Shift+Enter execution disabled.')

        ue.log(f'PyActorText3DExecutor: ready on {self.uobject.get_name()}')

    def tick(self, dt):
        if self._first_tick:
            self._first_tick = False
            try:
                self._text3d_actor = getattr(self.uobject, 'text3d_actor', None)
            except Exception:
                self._text3d_actor = None
            if self._text3d_actor is None:
                ue.log_warning(
                    'PyActorText3DExecutor: parent.text3d_actor missing — '
                    'spawn via ue_spawn.spawn_text3d_executor.')
            else:
                ue.log(
                    f'PyActorText3DExecutor: bound to '
                    f'{self._text3d_actor.get_name()} '
                    f'(Ctrl+Enter, Shift+Enter, or click to run)')
                # Register the child with PyActorText3D's typing system so
                # clicking the text focuses it for editing.  Without this,
                # the global click poll treats every click on this child
                # as off-target and unfocuses.  Both calls are idempotent.
                try:
                    from pyactor_text3d import PyActorText3D
                    PyActorText3D.register_actor(self._text3d_actor)
                    PyActorText3D._ensure_global_typing()
                except Exception as e:
                    ue.log_warning(
                        f'PyActorText3DExecutor: typing registration failed ({e})')

        if self._text3d_actor is None:
            return

        # Ctrl+Enter / Shift+Enter (Win32 polling). Tracked separately so a
        # rolling chord (e.g. release Ctrl, press Shift while still holding
        # Enter) doesn't double-fire and so each chord's rising edge is clean.
        if self._win32_ok and self._is_target_focused():
            ctrl_enter = self._is_ctrl_enter_down()
            shift_enter = self._is_shift_enter_down()
            if ctrl_enter and not self._prev_ctrl_enter_down:
                self._run_code(trigger='Ctrl+Enter')
            elif shift_enter and not self._prev_shift_enter_down:
                self._insert_newline() 
            self._prev_ctrl_enter_down = ctrl_enter
            self._prev_shift_enter_down = shift_enter
        else:
            self._prev_ctrl_enter_down = False
            self._prev_shift_enter_down = False

        # Click on the child Text3D
        self._poll_click()

        # After a run, re-pin the caret once this cell's relayout settles —
        # but bow out the moment the user types (the typing system relayouts
        # synchronously and renders the caret itself, so it owns it then).
        self._sync_caret_to_geometry()

    def _poll_click(self):
        if self._player_controller is None:
            return
        try:
            from click_helpers import is_mouse_down, cursor_hit_actor
        except Exception:
            return

        mouse_down = is_mouse_down(self._player_controller)
        try:
            on_target = (
                cursor_hit_actor(self.uobject, self._player_controller)
                is self._text3d_actor)
        except Exception:
            on_target = False

        if mouse_down and not self._prev_mouse_down and on_target:
            self._run_code(trigger='click')
        self._prev_mouse_down = mouse_down

    def _is_target_focused(self):
        """True when this executor's text3d should respond to the run chords.

        Fires when our text3d is the globally-focused actor OR when no
        actor is focused at all (so a fresh executor without the typing
        system set up still runs)."""
        try:
            from pyactor_global_click import PyActorGlobalClick
            focused = PyActorGlobalClick.get_focused_actor()
        except Exception:
            return True
        if focused is None:
            return True
        return focused is self._text3d_actor

    def _is_ctrl_enter_down(self):
        ctrl = self._user32.GetAsyncKeyState(self.VK_CONTROL) & 0x8000
        enter = self._user32.GetAsyncKeyState(self.VK_RETURN) & 0x8000
        return bool(ctrl) and bool(enter)

    def _is_shift_enter_down(self):
        shift = self._user32.GetAsyncKeyState(self.VK_SHIFT) & 0x8000
        enter = self._user32.GetAsyncKeyState(self.VK_RETURN) & 0x8000
        return bool(shift) and bool(enter)

    def _insert_newline(self):
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is not self._text3d_actor:
                return
            t3d = self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
            text = str(t3d.Text or '')
            a, b = sorted((PyActorText3D._string_idx, PyActorText3D._anchor))
            t3d.Text = text[:a] + '\n' + text[b:]
            PyActorText3D._string_idx = PyActorText3D._anchor = a + 1
            self._reshow_caret()
            self._arm_relayout_watch(True)
        except Exception as e:
            ue.log_warning(f'PyActorText3DExecutor: newline insert failed: {e}')

    def _run_code(self, trigger='?'):
        try:
            t3d = self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
        except Exception as e:
            ue.log_warning(
                f'PyActorText3DExecutor: get_actor_component failed: {e}')
            return
        if t3d is None:
            return
        try:
            code = str(t3d.Text or '')
        except Exception:
            return
        if not code.strip():
            return

        # Several executors can co-exist (e.g. test_text3d_pyactor spawns one
        # whose text is a plain English label, not Python). When Ctrl+Enter
        # fires unfocused, all executors run — silently skip texts that don't
        # parse as Python rather than spamming SyntaxError warnings.
        try:
            compiled = compile(code, '<text3d>', 'exec')
        except SyntaxError:
            return

        ue.log(
            f'PyActorText3DExecutor: running {trigger} on '
            f'{self._text3d_actor.get_name()}\n{code}')
        env = {
            '__name__': '__main__',
            'ue': ue,
            'self': self,
            'actor': self._text3d_actor,
            'parent': self.uobject,
        }
        # Running must not move the edit caret. Executed code routinely
        # rebuilds the scene, which resets PyActorText3D's class-level caret
        # state to 0 — so snapshot the caret before exec and re-pin it after,
        # leaving the user where they were typing.
        caret = self._snapshot_caret()
        try:
            exec(compiled, env)
        except Exception as e:
            ue.log_warning(f'PyActorText3DExecutor: exec failed: {e}')
        self._restore_caret(caret)
        self._arm_relayout_watch(caret is not None)

    def _snapshot_caret(self):
        """Caret (string_idx, anchor) iff our text3d is focused, else None."""
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is self._text3d_actor:
                return (PyActorText3D._string_idx, PyActorText3D._anchor)
        except Exception:
            pass
        return None

    def _restore_caret(self, caret):
        """Re-pin the caret captured before a run. No-op if focus moved
        (executed code may have intentionally focused another cell)."""
        if caret is None:
            return
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is not self._text3d_actor:
                return
            t3d = self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
            text = str(t3d.Text or '') if t3d is not None else ''
            si = max(0, min(caret[0], len(text)))
            anc = max(0, min(caret[1], len(text)))
            PyActorText3D._string_idx = si
            PyActorText3D._anchor = anc
            PyActorText3D.show_cursor_at(
                self._text3d_actor,
                PyActorText3D._string_idx_to_glyph(text, si),
                string_idx=si, text=text)
        except Exception as e:
            ue.log_warning(f'PyActorText3DExecutor: caret restore failed: {e}')

    def _reshow_caret(self):
        """Re-render the caret at its CURRENT index against fresh Text3D
        geometry. Reads (not resets) _string_idx, so caret moves the user
        makes right after a run are preserved."""
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is not self._text3d_actor:
                return
            t3d = self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
            text = str(t3d.Text or '') if t3d is not None else ''
            si = max(0, min(PyActorText3D._string_idx, len(text)))
            PyActorText3D.show_cursor_at(
                self._text3d_actor,
                PyActorText3D._string_idx_to_glyph(text, si),
                string_idx=si, text=text)
        except Exception:
            pass

    def _arm_relayout_watch(self, armed):
        """Begin watching this cell's relayout after a run so the caret can be
        re-pinned once the layout settles. Records the caret index now so we
        can tell if the user later moves it (types/navigates) and bow out."""
        self._watch_relayout = False
        self._watch_idx = None
        self._relayout_changed = False
        if not armed:
            return
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is not self._text3d_actor:
                return
            self._watch_relayout = True
            self._watch_idx = PyActorText3D._string_idx
            self._geom_sig = self._geometry_signature()
        except Exception:
            self._watch_relayout = False

    def _sync_caret_to_geometry(self):
        """Re-pin the caret once a run's relayout settles. Inert unless armed
        by a run; once armed it disarms on the first of: relayout settled (and
        re-pinned), user took over, or focus lost.

        Bows out the instant the user types or moves the caret: the typing
        system relayouts synchronously and renders the caret itself, so once
        the user takes over it owns the caret and we must not fight it. If the
        user does nothing, we wait for the layout signature to go stable after
        a change (the relayout finishing — however long the command took) and
        re-pin exactly once."""
        if not self._watch_relayout:
            return
        try:
            from pyactor_text3d import PyActorText3D
            if PyActorText3D._get_focused() is not self._text3d_actor:
                self._watch_relayout = False
                return
            # User took over (typed / moved caret) → stop; typing owns it now.
            if PyActorText3D._string_idx != self._watch_idx:
                self._watch_relayout = False
                return
            sig = self._geometry_signature()
            if sig != self._geom_sig:
                self._geom_sig = sig
                self._relayout_changed = True     # relayout in progress
            elif self._relayout_changed:
                self._watch_relayout = False       # settled → re-pin once, done
                self._reshow_caret()
        except Exception:
            self._watch_relayout = False

    def _geometry_signature(self):
        """Fingerprint of the cell's glyph layout — glyph count plus the
        first and last kerning positions. Changes whenever the Text3D
        relayouts (char count or glyph positions shift)."""
        t3d = self._text3d_actor.get_actor_component(self.TEXT_COMPONENT_NAME)
        kernings = t3d.CharacterKernings if t3d is not None else None
        n = len(kernings) if kernings else 0
        sig = [n]
        seen = set()
        for i in (0, n - 1):
            if i in seen or not (0 <= i < n):
                continue
            seen.add(i)
            k = kernings[i]
            if k is None:
                sig += [None, None, None]
                continue
            try:
                r = k.get_relative_location()
                sig += [round(r.x, 1), round(r.y, 1), round(r.z, 1)]
            except Exception:
                sig += [None, None, None]
        return tuple(sig)
