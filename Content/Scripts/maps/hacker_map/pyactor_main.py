"""
pyactor_main.py — HackerMap controller (Content/Maps/HackerMap.umap).

A glowing-green, eDEX-style terminal screen built from Starcel's own pieces:
sysmon data + MathPlotter / Screen Cube graphs, spawn_earth globe, the
FileExplorer, keyboard image generator + nd_table legends, a focused shell
executor and BP_StarcelLogo in neofetch. Black panels, green glowing text
and lines, the star map as the sky.

The view is a fixed screen: a CameraActor at layout.CAMERA_LOC looks at the
wall with a 90 deg FOV; no pawn is possessed, so there is no flying around.
The mouse cursor is on for clicking.

Usage:
    Run build_hacker_material.build() and build_hacker_level.build() once in
    the editor (see their docstrings). That places a BP_PyActorEmpty with
        PythonModule = maps.hacker_map.pyactor_main
        PythonClass  = Main
    so StarcelGameInstance skips auto-spawning main.Main here.

Input (hotkeys are ignored while the shell has keyboard focus, except Esc
during the intro):
    click the shell prompt and type; Enter runs a command (`help`)
    click an on-screen key to see what it does in Starcel
    click COPY / PASTE, or a file-explorer icon/name to open it
    F4  graphs: 3D MathPlotter lines <-> Screen Cube
    F5  replay the boot intro          Space / Esc  skip the intro
    F6  colour preset: 'black' (default: black background, green text)
        <-> 'green' (bright green background, white-hot text)
    M   toggle the mouse cursor
    mouse wheel: terminal scrollback, file list scrolling, globe zoom
"""

import os

import unreal_engine as ue
from unreal_engine import FVector, FTransform

import unreal_engine_tools
from unreal_engine_tools import startup, post_startup, get_world
from input_devices import Keyboard, Mouse, HotkeyManager

from maps.hacker_map import theme, ui, layout, graphs
from maps.hacker_map.theme import rot

SKY_MESH = '/Engine/MapTemplates/Sky/SM_SkySphere.SM_SkySphere'
SKY_MATERIAL = '/Game/Materials/M_SkyBox.M_SkyBox'     # starmap_g8k cubemap
SKY_RADIUS_FACTOR = 40.0     # sky radius = this x the wall distance

_begin_play_ran = False


class Main:

    # lifecycle

    def begin_play(self):
        global _begin_play_ran
        if _begin_play_ran:
            ue.log('hacker_map: begin_play already ran, skipping')
            return
        _begin_play_ran = True
        ue.log('hacker_map: Begin Play')

        startup()
        self.world = get_world()
        unreal_engine_tools.world = self.world
        theme.set_outer(self.uobject)
        graphs.clear_registry()

        self.panels = {}
        self.terminal = None
        self.building = True
        self._build_queue = []
        self._camera = None
        self._sky = None
        self._t = 0.0
        self._prev_mouse = False
        self._view_checks = 0

        from maps.hacker_map.sysdata import SysData
        self.data = SysData()
        self.data.start()

        self._spawn_sky()
        theme.on_preset(self._apply_env_preset)
        self._apply_env_preset(theme.PRESETS[theme.PRESET])
        self._setup_input()
        self._setup_camera()
        self._queue_builds()

        from maps.hacker_map.boot import BootSequence
        self.boot = BootSequence(self)
        self.boot.start()

        post_startup(self.uobject)

    def tick(self, dt):
        if not _begin_play_ran or not hasattr(self, 'boot'):
            return
        self._t += dt
        theme.tick()
        if self.building:
            self._build_step()
        if self.data.tick(dt):
            for p in self.panels.values():
                if p.built:
                    try:
                        p.update(self.data)
                    except Exception as e:
                        theme.warn(f'{p.key} update: {e}')
        for p in self.panels.values():
            if p.built:
                try:
                    p.tick(dt)
                except Exception as e:
                    theme.warn(f'{p.key} tick: {e}')
        try:
            self.boot.tick(dt)
        except Exception as e:
            theme.warn(f'boot: {e}; skipping intro')
            self.boot.skip()
        self._poll_clicks()
        # other systems (game mode, pawns spawning late) may grab the view
        # in the first seconds; keep it on our camera
        if self._view_checks < 20 and self._t > self._view_checks * 0.25:
            self._view_checks += 1
            self._hold_view()

    def end_play(self, reason):
        global _begin_play_ran
        _begin_play_ran = False
        ue.log('hacker_map: Ending play')
        try:
            self.data.stop()
        except Exception:
            pass
        graphs.clear_registry()
        theme.reset()
        unreal_engine_tools.invalidate_world_cache()
        for ticker in unreal_engine_tools.tickers:
            ue.remove_ticker(ticker)
        unreal_engine_tools.tickers.clear()
        if hasattr(self, 'input'):
            self.input.shutdown()

    # sky

    def _spawn_sky(self):
        """The star map (M_SkyBox / starmap_g8k) on an engine sky sphere,
        far behind the wall."""
        try:
            from unreal_engine.classes import MaterialInterface
            sky = ui.spawn_mesh(SKY_MESH, FVector(0, 0, 0), rot(), FVector(1, 1, 1))
            origin, extent = sky.GetActorBounds()
            r = max(extent.x, extent.y, extent.z, 1.0)
            k = layout.WALL_X * SKY_RADIUS_FACTOR / r
            sky.set_actor_scale(FVector(k, k, k))
            mat = ue.load_object(MaterialInterface, SKY_MATERIAL)
            self._sky_mat = mat
            self._sky_mid = None
            if mat is not None:
                smc = sky.StaticMeshComponent
                smc.set_material(0, mat)
                try:
                    self._sky_mid = smc.create_material_instance_dynamic(mat)
                except Exception as e:
                    theme.warn(f'sky MID: {e}')
            theme.on_preset(self._apply_sky_preset)
            self._apply_sky_preset(theme.PRESETS[theme.PRESET])
            try:
                sky.StaticMeshComponent.CastShadow = False
            except Exception:
                pass
            self._sky = sky
        except Exception as e:
            theme.warn(f'star sky failed: {e}')

    def _apply_sky_preset(self, preset):
        """'black': star map dimmed to faint stars. 'green': the star map at
        its own brightness (bloom washes it green)."""
        if self._sky is None:
            return
        smc = self._sky.StaticMeshComponent
        e = preset.get('sky_emissive')
        if e is None or self._sky_mid is None:
            if self._sky_mat is not None:
                smc.set_material(0, self._sky_mat)
            return
        try:
            self._sky_mid.set_material_scalar_parameter('Emissive Multiplier', float(e))
            smc.set_material(0, self._sky_mid)
        except Exception as ex:
            theme.warn(f'sky preset: {ex}')

    def _apply_env_preset(self, preset):
        """The level's PostProcessVolume (green tint, bloom), any fog, and
        auto-exposure are what wash the screen green and blow out the globe.
        'black' switches them all off (fixed exposure); 'green' brings them
        back."""
        on = bool(preset.get('level_post_process'))
        for a in self.world.all_actors():
            try:
                cname = a.get_class().get_name()
            except Exception:
                continue
            try:
                if cname == 'PostProcessVolume':
                    a.bEnabled = on
                elif cname == 'ExponentialHeightFog':
                    a.SetActorHiddenInGame(not on)
                    comp = a.get_actor_component_by_type(
                        ue.find_class('ExponentialHeightFogComponent'))
                    if comp is not None:
                        comp.SetVisibility(on, False)
            except Exception as e:
                theme.warn(f'env preset on {cname}: {e}')
        self._console(f"ShowFlag.EyeAdaptation {1 if on else 0}")

    def _console(self, cmd):
        try:
            from unreal_engine.classes import KismetSystemLibrary
            KismetSystemLibrary.ExecuteConsoleCommand(self.uobject, cmd)
        except Exception:
            try:
                self.uobject.get_player_controller().ConsoleCommand(cmd)
            except Exception as e:
                theme.warn(f'console "{cmd}": {e}')

    # camera: one fixed screen, no pawn

    def _setup_camera(self):
        from unreal_engine.classes import CameraActor
        loc, r = layout.camera_spot()
        try:
            self._camera = self.world.actor_spawn(CameraActor, loc, r)
            cam = self._camera.get_actor_component_by_type(ue.find_class('CameraComponent'))
            if cam is not None:
                cam.FieldOfView = layout.FOV
                cam.bConstrainAspectRatio = False
        except Exception as e:
            theme.warn(f'camera spawn failed: {e}')
        self._hold_view()

    def _hold_view(self):
        """Park whatever pawn the game mode gave us (hidden, no input) and
        look through the fixed camera."""
        try:
            pc = self.uobject.get_player_controller()
        except Exception:
            return
        if pc is None:
            return
        try:
            pc.bAutoManageActiveCameraTarget = False
        except Exception:
            pass
        pawn = None
        try:
            pawn = pc.K2_GetPawn()
        except Exception:
            pass
        if pawn is not None:
            try:
                pawn.SetActorHiddenInGame(True)
                pawn.DisableInput(pc)
                pawn.SetActorEnableCollision(False)
                proxy = pawn.get_py_proxy()
                if proxy is not None and hasattr(proxy, 'set_suspended'):
                    proxy.set_suspended(True)
            except Exception:
                pass
            try:
                pc.UnPossess()
            except Exception:
                pass
        if self._camera is not None:
            try:
                if pc.GetViewTarget() is not self._camera:
                    pc.SetViewTargetWithBlend(self._camera, 0.0)
            except Exception:
                try:
                    pc.SetViewTargetWithBlend(self._camera, 0.0)
                except Exception as e:
                    theme.warn(f'view target: {e}')

    # building (one step per tick, during the boot log)

    def _queue_builds(self):
        from maps.hacker_map.panels import SystemPanel, NetworkPanel, FilesystemPanel
        from maps.hacker_map.keyboard3d import KeyboardPanel
        from maps.hacker_map.shell import TerminalPanel
        order = [('terminal', TerminalPanel), ('keyboard', KeyboardPanel),
                 ('system', SystemPanel), ('network', NetworkPanel),
                 ('filesystem', FilesystemPanel)]
        for key, cls in order:
            self._build_queue.append(('panel', key, cls))

    def _build_step(self):
        if not self._build_queue:
            self.building = False
            theme.log(f'built {len(self.panels)} panels')
            return
        item = self._build_queue.pop(0)
        try:
            if item[0] == 'panel':
                _, key, cls = item
                p = cls(key)
                p.built = False
                p.bind(self.data)
                self.panels[key] = p
                if key == 'terminal':
                    self.terminal = p
                steps = p.build_steps()
                for i, step in enumerate(steps):
                    self._build_queue.insert(i, ('step', key, step))
                self._build_queue.insert(len(steps), ('done', key, None))
            elif item[0] == 'step':
                _, key, step = item
                step()
                self.panels[key].set_visible(False)
            elif item[0] == 'done':
                p = self.panels[item[1]]
                p.built = True
                p.set_visible(False)
                try:
                    p.update(self.data)
                except Exception:
                    pass
        except Exception as e:
            import traceback
            theme.warn(f'build {item[0]} {item[1]} failed: {e}\n{traceback.format_exc()}')

    def build_all_now(self):
        while self.building:
            self._build_step()

    def build_status(self):
        done = sum(1 for p in self.panels.values() if getattr(p, 'built', False))
        pending = [k for k in layout.PANELS if k not in self.panels or
                   not getattr(self.panels[k], 'built', False)]
        return f'building panels {done}/{len(layout.PANELS)} ' + (f'[{pending[0]}]' if pending else '')

    # panel visibility (used by boot)

    def hide_all_panels(self):
        for p in self.panels.values():
            p.set_visible(False)
        self.set_globe_grow(0.0)

    def show_all_panels(self):
        for p in self.panels.values():
            p.set_visible(True)
        self.set_globe_grow(1.0)

    def reveal_panel(self, key, t):
        p = self.panels.get(key)
        if p is not None and getattr(p, 'built', False):
            p.reveal(t)

    def set_globe_grow(self, k):
        p = self.panels.get('network')
        if p is not None and getattr(p, 'built', False) and hasattr(p, 'grow'):
            p.grow(max(0.0, min(1.0, k)))

    # input

    def _setup_input(self):
        if _is_server(self.uobject):
            return
        self.uobject.enable_input()
        self.keyboard = Keyboard()
        self.mouse = Mouse()
        self.input = HotkeyManager(self.uobject, self.keyboard, self.mouse)
        b = self.input.bind_press
        b('M', self._unless_typing(self.input.toggle_cursor))
        b('F4', self._unless_typing(self.toggle_graphs))
        b('F5', self._unless_typing(self.replay_boot))
        b('F6', self._unless_typing(theme.cycle_preset))
        # mouse wheel scrolls whatever panel is under the cursor
        b('MouseScrollUp', lambda: self._on_wheel(+1))
        b('MouseScrollDown', lambda: self._on_wheel(-1))
        b('Escape', self.skip_boot)
        b('SpaceBar', self._unless_typing(self.skip_boot))   # Esc stops PIE in the editor
        # cursor on from the start: this is a screen you click on
        try:
            if not self.input._cursor_visible:
                self.input.toggle_cursor()
        except Exception as e:
            theme.warn(f'cursor: {e}')

    @staticmethod
    def _unless_typing(fn):
        def _wrapped(*args):
            try:
                from actors.pyactor_global_click import PyActorGlobalClick
                if PyActorGlobalClick.is_any_focused():
                    return
            except Exception:
                pass
            return fn(*args)
        return _wrapped

    def skip_boot(self):
        if hasattr(self, 'boot') and not self.boot.done:
            self.boot.skip()

    def replay_boot(self):
        if self.building or not self.boot.done:
            return
        self.boot.replay()

    def toggle_graphs(self):
        mode = graphs.toggle_all()
        theme.log(f'graphs -> {mode}')

    # clicks (COPY / PASTE, keyboard keys, explorer icons)

    def _poll_clicks(self):
        pc = None
        try:
            from click_helpers import is_mouse_down, cursor_hit_actor
            pc = self.uobject.get_player_controller()
            down = is_mouse_down(pc)
        except Exception:
            return
        rising = down and not self._prev_mouse
        self._prev_mouse = down
        # dragging the globe: follow the mouse until the button is released
        if getattr(self, '_drag', None) is not None:
            if not down:
                self._drag = None
            else:
                pos = _mouse_pos(pc)
                if pos is not None:
                    net = self.panels.get('network')
                    dx, dy = pos[0] - self._drag[0], pos[1] - self._drag[1]
                    if net is not None and (dx or dy):
                        net.drag(dx, dy)
                    self._drag = pos
            return
        if not rising:
            return
        try:
            hit = cursor_hit_actor(self.uobject, pc)
        except Exception:
            hit = None
        if hit is None:
            return
        net = self.panels.get('network')
        if net is not None and getattr(net, 'built', False) and net.is_view(hit):
            self._drag = _mouse_pos(pc)      # start orbiting the globe
            return
        term = self.panels.get('terminal')
        if term is not None and getattr(term, 'built', False) and                 getattr(term, 'backdrop_sc', None) is not None and                 _same(hit, term.backdrop_sc.actor):
            term.focus_prompt()              # click on the terminal = type in the shell
            return
        sysp = self.panels.get('system')
        if sysp is not None and getattr(sysp, 'built', False):
            if _same(hit, getattr(sysp, 'copy_btn', None)):
                self._copy()
                return
            if _same(hit, getattr(sysp, 'paste_btn', None)):
                self._paste()
                return
        kb = self.panels.get('keyboard')
        if kb is not None and getattr(kb, 'built', False):
            legend = kb.click(hit)
            if legend is not None:
                self._report_key(kb)
                return
        fs = self.panels.get('filesystem')
        if fs is not None and getattr(fs, 'built', False):
            try:
                fs.click(hit)
            except Exception as e:
                theme.warn(f'explorer click: {e}')

    def _panel_under_cursor(self):
        try:
            from click_helpers import cursor_hit_actor
            hit = cursor_hit_actor(self.uobject, self.uobject.get_player_controller())
        except Exception:
            return None, None
        if hit is None:
            return None, None
        for _ in range(2):
            m = getattr(self, '_part_owner', None)
            if m is not None and id(hit) in m:
                return self.panels.get(m[id(hit)]), hit
            # (re)build the actor -> panel map (explorer re-renders add parts)
            self._part_owner = {id(a): key for key, p in self.panels.items()
                                for a in p.parts}
        for key, p in self.panels.items():
            for a in p.parts:
                if _same(a, hit):
                    return p, hit
        return None, hit

    def _on_wheel(self, steps):
        """Wheel over: terminal = scrollback, filesystem = scroll the
        listing, network = zoom the globe (clipped to its window)."""
        panel, hit = self._panel_under_cursor()
        if panel is None:
            return
        try:
            if panel.key == 'terminal':
                panel.scroll(steps)
            elif panel.key == 'filesystem':
                proxy = getattr(panel, 'explorer_proxy', None)
                if proxy is not None and hasattr(proxy, 'scroll'):
                    proxy.scroll(steps)
            elif panel.key == 'network':
                panel.zoom(steps)
        except Exception as e:
            theme.warn(f'wheel on {panel.key}: {e}')

    def _prompt_proxy(self):
        t = self.terminal
        if t is None or t.prompt is None:
            return None
        try:
            return t.prompt.get_py_proxy()
        except Exception:
            return None

    def _report_key(self, kb):
        """On-screen key clicked: the keyboard panel shows the first use;
        list every Starcel binding for it in the terminal."""
        face, uses = kb.last_usage or ('?', [])
        t = self.terminal
        if t is None:
            return
        if not uses:
            t.write(f'[{face}] not bound to anything in Starcel')
            return
        t.write(f'[{face}] used in Starcel for:')
        for line in uses:
            t.write(f'   {line}')

    def _type_key(self, legend):
        """On-screen key clicked: type it into the shell prompt."""
        proxy = self._prompt_proxy()
        if proxy is None:
            return
        cur = proxy._get_text()
        special = {'Space': ' ', 'Tab': '    '}
        if legend == 'Backspace':
            proxy.set_text(cur[:-1])
        elif legend == 'Enter':
            proxy._submit(cur)
        elif legend in special:
            proxy.set_text(cur + special[legend])
        elif len(legend) == 1:
            proxy.set_text(cur + legend)
        else:
            return
        if self.terminal is not None:
            self.terminal.focus_prompt()

    def _copy(self):
        from actors.pyactor_text3d import PyActorText3D
        proxy = self._prompt_proxy()
        text = proxy._get_text() if proxy is not None else ''
        if not text and self.terminal is not None and self.terminal.entries:
            text = self.terminal.entries[-1][0]
        PyActorText3D._ensure_global_typing()
        PyActorText3D._clipboard_set_text(text)
        theme.log(f'copied {len(text)} chars')

    def _paste(self):
        from actors.pyactor_text3d import PyActorText3D
        PyActorText3D._ensure_global_typing()
        clip = PyActorText3D._clipboard_get_text() or ''
        proxy = self._prompt_proxy()
        if proxy is not None:
            proxy.set_text(proxy._get_text() + clip.replace('\r', '').split('\n')[0])
            if self.terminal is not None:
                self.terminal.focus_prompt()


def _mouse_pos(pc):
    """Mouse position in viewport pixels, or None."""
    try:
        r = pc.GetMousePosition()
    except Exception:
        return None
    try:
        if len(r) == 3:
            ok, x, y = r
            return (float(x), float(y)) if ok else None
        x, y = r
        return float(x), float(y)
    except Exception:
        return None


def _is_server(uobject):
    try:
        from unreal_engine.classes import KismetSystemLibrary
        return bool(KismetSystemLibrary.IsDedicatedServer(uobject))
    except Exception:
        return False


def _same(a, b):
    if a is None or b is None:
        return False
    if a is b:
        return True
    try:
        return a.get_name() == b.get_name()
    except Exception:
        return False
