"""
pyactor_main.py — watermap map controller (WaterMap level).

Copy of Scripts/main.py, changed to drop the physics desktop-icon balls
onto the water instead of at the main level's ICON_BALLS_ORIGIN.

The water mesh sits at loc=(0, 0, 0), scale=(100, 100, 25). On
begin_play this finds a "Water Physics - Water Volume" actor in the level
(or spawns one sized from the WATER_* constants below) so the balls float
via the WaterPhysics plugin, then queues the icon balls above it.

Usage:
    In WaterMap, select the BP_PyActorEmpty and set
        PythonModule = maps.watermap.pyactor_main
        PythonClass  = Main
    (StarcelGameInstance then skips auto-spawning main.Main here.)
"""

import unreal_engine as ue
import unreal_engine.classes
from unreal_engine_tools import *
import unreal_engine_tools
import numpy as np
import warnings as _warnings
with _warnings.catch_warnings():
    _warnings.filterwarnings('ignore', message='pkg_resources is deprecated', category=UserWarning)
    import fast_autocomplete
import os, sys, subprocess, importlib, socket, struct, math, sympy, numba, kingdon, asyncio, time, random
from unreal_engine import FVector, FRotator, FTransform, FHitResult, CLASS_CONFIG, CLASS_DEFAULT_CONFIG, CPF_CONFIG, CPF_GLOBAL_CONFIG, CPF_EXPOSE_ON_SPAWN, CPF_NET, CPF_REP_NOTIFY
from unreal_engine.classes import Actor, Character, PlayerController, StaticMeshActor, KismetMathLibrary, KismetSystemLibrary, Object, StrProperty, IntProperty, Blueprint, Material, Texture, LargeStringAsync, LargeStringRPCActor, StaticMesh, StaticMeshActor, AudioComponent
from unreal_engine.enums import EInputEvent, ETraceTypeQuery, EDrawDebugTrace, EComponentMobility, EMouseCursor, ECollisionChannel
import constants, windowtool
from constants import Constants, WorldSize
from languages import *
from cli import *
from typing import List, Dict, Union, Optional
from input_devices import Keyboard, Mouse, HotkeyManager, TraceHelper
from ue_spawn import spawn_icon
from icon_to_image import extract_icon
from test_spawn import test_spawn_all


# Warning:
# BUG: imported classes are not reloaded, you need to restart the unreal engine editor if you are using that (doesn't affect .exe)
# Code placed outside the Main class will not run when connecting to a server and may run twice
# You can ignore and delete .uasset files as you'd like. They are regenerated on run

ue.log('I am a Python module.')

#TODO: Completely empty main.py

# Use this if you want to rebuild the unreal_engine intellisense(.pyi, etc.) and cli
# rebuild_generated_modules()

# ret = ue.message_dialog_open(ue.APP_MSG_TYPE_YES_NO, "Do you want to test dialogs?")
# if ret == ue.APP_RETURN_TYPE_YES:
#     ue.log('You choose "YES"')

class Main:
    # this is called on game start
    def begin_play(self):
        ue.log('watermap: Begin Play on Main class')
        # No change_background() here: WaterMap doesn't have the main level's
        # sky/fog/light/post-process actors, and it crashes on the missing
        # SkyLight5 (it only bails when *none* of them exist, and WaterMap
        # has a BP_SkySphere).
        ue.log('Running startup')
        startup()

        global world
        world = get_world()
        print("begin_play found world", world)
        unreal_engine_tools.world = world
        # print(world)

        try:
            self.spawn_lighting()
        except Exception as e:
            ue.log_warning(f'watermap: spawn_lighting failed: {e}')

        is_dedicated_server = KismetSystemLibrary.IsDedicatedServer(self.uobject)

        if not is_dedicated_server:
            self.uobject.enable_input()

            self.keyboard = Keyboard()
            self.mouse = Mouse()

            self.input = HotkeyManager(self.uobject, self.keyboard, self.mouse)
            self.trace = TraceHelper(self.uobject)

            self.input.bind_press("M", self.input.toggle_cursor)

            # G: gizmo editing mode — click any actor to attach the
            # translate/rotate/scale gizmo to it.
            from gizmo_edit_mode import GizmoEditMode
            self.gizmo_mode = GizmoEditMode(self.uobject, self.input)
            self.input.bind_press("G", self._unless_typing(self.gizmo_mode.toggle))

            # =: spawn a Text3D Python executor in front of the camera and
            # focus it (caret ready for typing, Ctrl+Enter to run).
            self.input.bind_press("=", self._unless_typing(self.spawn_executor))

            # P: switch possession between the drone and the stickman.
            self.input.bind_press("P", self._unless_typing(self.toggle_pawn))
            # L: toggle background music on/off (temporary).
            self.input.bind_press("L", self._unless_typing(self.toggle_music))
            # self.input.bind_press("T", self.toggle_window_transparency)

        if is_dedicated_server: # WARNING, Only Client -> Server sending of Multi-GB strings currently implemented
            ue.log("BeginPlay on DEDICATED SERVER")
            print("using world", world.get_name())
            # print(world.all_actors())
            # for actor in world.all_actors():
            #     print(actor.get_class().get_name())
            gm = find_actor("StarcelGameMode")
            print("Gamemode: ", gm)

            def on_player_joined(player_controller):
                ue.log_warning(f"[SERVER PY] Player joined: {player_controller}") # START HERE
                # Spawn drone pawn and possess it
                drone_class = load_blueprint_class('/Game/Blueprints/Assets/DroneCharacter/BP_PyDroneCharacter.BP_PyDroneCharacter')
                player = world.actor_spawn(drone_class)
                transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
                player.set_actor_transform(transform)
                player_controller.Possess(player)
                py_player = player.get_py_proxy()
                py_player._setup_input()

        else:
            if self.uobject.HasAuthority():
                ue.log("BeginPlay on LISTEN SERVER / STANDALONE (has authority)")
            else:
                ue.log("BeginPlay on CLIENT (connected to remote server)")


            # Explicit drone possession method (same as master's main.py): spawn
            # BP_PyDroneCharacter and Possess it so it overrides whatever pawn the
            # GameMode auto-possessed. Single possession only — the duplicate
            # post_startup() possession below is disabled (master has none).
            print("Begin Drone Possession")
            drone_class = load_blueprint_class('/Game/Blueprints/Assets/DroneCharacter/BP_PyDroneCharacter.BP_PyDroneCharacter')
            player = world.actor_spawn(drone_class)
            transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
            player.set_actor_transform(transform)
            self.uobject.get_player_controller().Possess(player)
            py_player = player.get_py_proxy()
            py_player._setup_input()
            self.pawn = player          # the visible, possessed pawn
            self.controlling_drone = True
            self._pawns = {"drone": player}   # stickman added on first P

            # self.test_cylinder()
            # self.test_text()

            # main.py's test_spawn_all() (5x5x5 table at (0,0,500), executor,
            # click test) is left out: it would spawn right on top of the water.

            try:
                self.spawn_icon_balls()
            except Exception as e:
                ue.log_warning(f'watermap: spawn_icon_balls failed: {e}')

        post_startup(self.uobject)

    # this is called at every 'tick'
    def tick(self, delta_time):
        # get current location
        location = self.uobject.get_actor_location()
        # increase Z honouring delta_time
        location.z += 100 * delta_time
        # set new location
        self.uobject.set_actor_location(location)

        self._tick_icon_balls(delta_time)
        self._tick_waves(delta_time)

        # self.input.print_cursor_info()

    def end_play(self, reason):
        ue.log("Ending play")
        import unreal_engine_tools
        unreal_engine_tools.invalidate_world_cache()
        for ticker in unreal_engine_tools.tickers:
            ue.remove_ticker(ticker)
            print(ticker, "stopped.")
        unreal_engine_tools.tickers.clear()
        if hasattr(self, 'input'):
            self.input.shutdown()

    def ctrl_shift_b(self):
        ue.log("Pressed Ctrl+Shift+B")

    def on_ctrl_shift_b(self):
        ue.log("Pressed Ctrl+Shift+B")

    def left_click(self):
        ue.log("Left mouse button")

    def on_left_click(self):
        ue.log("Left mouse button clicked")

    def shift_click(self):
        """Shift + Click action"""
        ue.log("Shift + Click")
        # Multi-select logic, etc.

    def mouse_wheel(self, value):
        ue.log("Wheel: {}".format(value))

    def sequence_action(self):
        ue.log("Sequence fired: Ctrl+K → MouseX → Click")

    def on_move_forward(self, value):
        """Handle analog movement input"""
        if value != 0:
            ue.log(f"Moving forward: {value:.2f}")
            # Add movement code here

    def check_key_states(self):
        """Example of manually checking key states without binding"""
        if self.input.is_key_down("W"):
            ue.log("W is currently down")
        if self.input.is_key_down("LeftControl"):
            ue.log("Left Control is currently down")
        if self.input.is_chord_down("Ctrl+Shift"):
            ue.log("Ctrl+Shift combo is down")

    @staticmethod
    def _unless_typing(fn):
        """Wrap a hotkey so it does nothing while a Text3D has keyboard
        focus — the key is being typed as text, not used as a command."""
        def _wrapped(*args):
            try:
                from actors.pyactor_global_click import PyActorGlobalClick
                if PyActorGlobalClick.is_any_focused():
                    return
            except Exception:
                pass
            return fn(*args)
        return _wrapped

    def toggle_music(self):
        """L-key (temporary): stop the BackgroundMusic actor's audio if it's
        playing, otherwise start it again."""
        bg_music = find_actor("BackgroundMusic")
        if bg_music is None:
            ue.log_warning("toggle_music: no BackgroundMusic actor")
            return
        for ac in bg_music.get_components_by_type(AudioComponent):
            if ac.IsPlaying():
                ac.call('Stop')
                ue.log("Background music: off")
            else:
                ac.call('Play')
                ue.log("Background music: on")

    def spawn_executor(self):
        from ue_spawn import spawn_focused_text3d_executor
        spawn_focused_text3d_executor()

    def toggle_pawn(self):
        """P-key: swap between the drone and the stickman. Both stay alive;
        the outgoing one is hidden (no collision, movement paused) and the
        incoming one is shown and moved to where the outgoing one was. Each
        keeps its own size; the first stickman matches the drone."""
        if getattr(self, "pawn", None) is None:
            return
        pc = self.uobject.get_player_controller()

        old = self.pawn
        old_kind = "drone" if self.controlling_drone else "stickman"
        new_kind = "stickman" if self.controlling_drone else "drone"
        py_old = self._pawn_py(old)
        loc = old.get_actor_location()
        look = self._view_rotation(pc)   # where you're looking right now

        # Park the outgoing pawn first so its spot is free.
        self._set_pawn_shown(old, False)
        if old_kind == "drone" and py_old is not None:
            # Detaches the PC InputComponent holding the drone's bindings
            # (they consume WASD/mouse before the stickman sees them).
            py_old.set_suspended(True)

        new_pawn = self._pawns.get(new_kind)
        if new_pawn is None:
            # First stickman: spawn it where the drone is, at the drone's size.
            s = old.get_actor_scale()
            size = max(s.x, s.y, s.z)
            for lift in (0, 100, 300, 600):
                try:
                    new_pawn = world.actor_spawn(
                        load_blueprint_class(self._PAWN_CLASSES[new_kind]),
                        FVector(loc.x, loc.y, loc.z + lift * size),
                        FRotator(0, 0, 0))
                    break
                except Exception:
                    continue
            if new_pawn is None:
                self._set_pawn_shown(old, True)
                if old_kind == "drone" and py_old is not None:
                    py_old.set_suspended(False)
                ue.log_warning(f"toggle_pawn: no free spot to spawn the {new_kind}")
                return
            new_pawn.set_actor_scale(FVector(size, size, size))
            self._pawns[new_kind] = new_pawn
        else:
            new_pawn.set_actor_location(loc)
            self._set_pawn_shown(new_pawn, True)

        pc.Possess(new_pawn)
        py_new = self._pawn_py(new_pawn)
        if new_kind == "drone":
            if py_new is not None:
                py_new.set_suspended(False)   # re-attach its PC bindings
        elif py_new is not None and hasattr(py_new, "_setup_input"):
            py_new._setup_input()   # no-op after the first time
        # After Possess, which resets the control rotation to the pawn's.
        self._apply_view_rotation(new_kind, new_pawn, py_new, pc, look)

        self.pawn = new_pawn
        self.controlling_drone = new_kind == "drone"
        ue.log(f"Possessing: {new_kind}")

    @staticmethod
    def _view_rotation(pc):
        """Pitch/yaw of what's on screen (the active camera), roll dropped."""
        try:
            r = pc.PlayerCameraManager.GetCameraRotation()
        except Exception:
            try:
                r = pc.GetControlRotation()
            except Exception:
                return None
        return FRotator(0.0, r.pitch, r.yaw)   # FRotator(roll, pitch, yaw)

    @staticmethod
    def _apply_view_rotation(kind, pawn, py, pc, look):
        """Point the incoming pawn's view along `look`. Only the rotation
        carries over between swaps (location is handled by toggle_pawn)."""
        if look is None:
            return
        try:
            if kind == "drone":
                # The drone looks along its actor rotation (first-person
                # camera); keep its cached angles in sync for non-legacy mode.
                pawn.set_actor_rotation(look)
                if py is not None:
                    py._roll, py._pitch, py._yaw = 0.0, look.pitch, look.yaw
            else:
                # The stickman looks along the control rotation; turn the
                # body to the same yaw so it doesn't swing round first.
                pawn.set_actor_rotation(FRotator(0.0, 0.0, look.yaw))
            pc.SetControlRotation(look)
        except Exception as e:
            ue.log_warning(f"toggle_pawn: could not carry view rotation: {e}")

    def _set_pawn_shown(self, actor, shown):
        """Show/hide a pawn in game. Hidden pawns also lose collision and
        have their movement component paused — otherwise a hidden Character
        with no collision falls forever and gets killed at KillZ."""
        actor.SetActorHiddenInGame(not shown)
        actor.SetActorEnableCollision(shown)
        move = getattr(actor, "CharacterMovement", None)
        if move is not None:
            if shown:
                move.StopMovementImmediately()
            move.SetComponentTickEnabled(shown)
        py = self._pawn_py(actor)
        if py is not None and hasattr(py, "set_hidden"):
            py.set_hidden(not shown)   # e.g. the stickman's attached crosshair

    _PAWN_CLASSES = {
        "drone": '/Game/Blueprints/Assets/DroneCharacter/BP_PyDroneCharacter.BP_PyDroneCharacter',
        "stickman": '/Game/ThirdPersonCPP/Blueprints/StickManCharacter.StickManCharacter',
    }

    @staticmethod
    def _pawn_py(actor):
        """Python object driving a pawn. The drone is a Python pawn (proxy on
        the actor); StickManCharacter is a C++ Character with a Python
        *component* (PyActorStickMan), so its proxy is on that component."""
        py = actor.get_py_proxy()
        if py is not None:
            return py
        for c in actor.get_components():
            py = c.get_py_proxy()
            if py is not None and hasattr(py, "_setup_input"):
                return py
        return None

    # The water: mesh at (0, 0, 0), scale (100, 100, 25). The physics volume
    # is a box whose TOP face is the water surface. Tweak these if the
    # balls float above/below the visible waves.
    WATER_CENTER = FVector(0.0, 0.0, 0.0)
    WATER_SURFACE_Z = 0.0          # world Z of the water surface
    WATER_HALF_SIZE_XY = 5000.0    # UU; 100 UU plane x scale 100 / 2
    WATER_DEPTH = 2500.0           # UU; 100 UU x scale 25
    WATER_VOLUME_CLASS = 'WaterPhysics_WaterVolume'

    # Desktop-icon balls, spawned above the water with physics on.
    ICON_BALLS_DROP_HEIGHT = 1600.0   # UU above the water surface
    ICON_BALLS_ORIGIN = FVector(0.0, 0.0, WATER_SURFACE_Z + ICON_BALLS_DROP_HEIGHT)
    ICON_BALLS_MAX = 50        # cap on how many desktop icons to spawn
    ICON_BALLS_RANGE = 400.0   # UU; random offset from origin on every axis
    # BP_Icon's 100 UU sphere displaces ~524 kg of water, so anything
    # lighter floats. Lower = rides higher; above ~524 it sinks.
    ICON_BALL_MASS_KG = 150.0

    # --- Fake waves for bobbing ------------------------------------------
    # The physics water surface is the flat top of the volume and the
    # material's waves are only a moving normal map, so on their own the
    # balls just sit still. Each tick, every ball near the surface gets a
    # vertical acceleration proportional to a wave height h(x, y, t), a sum
    # of travelling sine waves. That shifts where buoyancy balances, so the
    # ball rides h up and down; neighbours get different phases.
    #
    # Each wave: (dir_x, dir_y, wavelength_uu, amplitude_uu, period_s).
    # Directions follow the material's two panners (small ripples heading
    # +X/+Y, big swells heading -X/+Y) so the motion reads as the same sea.
    WAVES = [
        (0.83, 0.55, 3000.0, 30.0, 4.5),    # main swell
        (-0.55, 0.83, 1700.0, 15.0, 3.2),   # cross swell
        (0.30, -0.95, 700.0, 6.0, 1.9),     # chop
    ]
    WAVES_ENABLED = True
    # Acceleration (cm/s²) per cm of wave height. ≈ buoyancy stiffness / mass
    # for a 150 kg ball half in water; raise for stronger bobbing.
    WAVE_ACCEL_PER_UU = 50.0
    # Sideways push along each wave's direction while on a crest (cm/s²
    # per cm of that wave's height), so balls drift and jostle a little.
    WAVE_DRIFT_PER_UU = 2.0
    # Only push balls whose centre is within this many UU of the surface
    # (so balls still falling through the air aren't affected).
    WAVE_ACTIVE_BAND = 150.0

    def _wave_height(self, x, y, t):
        """Sum of travelling sines. Returns (height, drift_x, drift_y)."""
        h = dx = dy = 0.0
        for wx, wy, wavelength, amp, period in self.WAVES:
            k = 2.0 * math.pi / wavelength
            w = 2.0 * math.pi / period
            s = amp * math.sin(k * (wx * x + wy * y) - w * t)
            h += s
            dx += wx * s
            dy += wy * s
        return h, dx, dy

    def _tick_waves(self, delta_time):
        if not self.WAVES_ENABLED:
            return
        balls = getattr(self, 'icon_balls', None)
        surface = getattr(self, 'water_surface_z', None)
        if not balls or surface is None:
            return
        self._wave_time = getattr(self, '_wave_time', 0.0) + delta_time
        t = self._wave_time
        for b in balls:
            try:
                p = b.get_actor_location()
                if abs(p.z - surface) > self.WAVE_ACTIVE_BAND:
                    continue
                h, dx, dy = self._wave_height(p.x, p.y, t)
                sphere = b.get_actor_component('Sphere')
                # bAccelChange=True: value is an acceleration, mass-independent.
                sphere.AddForce(FVector(dx * self.WAVE_DRIFT_PER_UU,
                                        dy * self.WAVE_DRIFT_PER_UU,
                                        h * self.WAVE_ACCEL_PER_UU),
                                'None', True)
            except Exception:
                continue
    ICON_BALLS_MIN_GAP = 110.0 # UU; min distance between ball centers at spawn (sphere is 100 across)
    ICON_BALLS_INTERVAL = 0.5  # seconds between spawns, so they don't pile up and explode
    ICON_BALLS_SPEED = 150.0   # UU/s; max initial sideways speed

    # Runtime lighting: sun + physical sky + real-time sky light + fog.
    # Each piece is skipped if the level already has one of that class.
    SUN_PITCH = -40.0          # degrees below the horizon line (negative = pointing down)
    SUN_YAW = 30.0
    SUN_INTENSITY_LUX = 8.0
    SKY_LIGHT_INTENSITY = 1.0
    FOG_DENSITY = 0.005
    _MOVABLE = 2               # EComponentMobility::Movable

    def spawn_lighting(self):
        """Spawn a sun, SkyAtmosphere, real-time-capture SkyLight and height
        fog. All movable: runtime-spawned lights have no baked lighting, so
        static/stationary ones would render wrong."""
        from unreal_engine.classes import (
            DirectionalLight, SkyLight, SkyAtmosphere, ExponentialHeightFog)

        present = set()
        for a in world.all_actors():
            try:
                present.add(a.get_class().get_name())
            except Exception:
                pass
        self.lighting_actors = []

        def spawn(cls, name, loc=FVector(0, 0, 0), rot=None):
            if name in present:
                ue.log(f'watermap: level already has a {name}, not spawning one')
                return None
            actor = world.actor_spawn(cls, loc, rot or FRotator(0, 0, 0))
            self.lighting_actors.append(actor)
            return actor

        # Atmosphere first: the sun and the real-time sky light both read it.
        spawn(SkyAtmosphere, 'SkyAtmosphere')

        # FRotator's constructor argument order differs between UEPython
        # builds, so set pitch/yaw by name.
        sun_rot = FRotator(0, 0, 0)
        sun_rot.pitch = self.SUN_PITCH
        sun_rot.yaw = self.SUN_YAW
        sun = spawn(DirectionalLight, 'DirectionalLight', FVector(0, 0, 1000), sun_rot)
        if sun is not None:
            lc = sun.LightComponent
            lc.SetMobility(self._MOVABLE)
            lc.SetIntensity(self.SUN_INTENSITY_LUX)
            try:
                lc.SetAtmosphereSunLight(True)
            except Exception:
                try:
                    lc.bAtmosphereSunLight = True
                except Exception as e:
                    ue.log_warning(f'watermap: could not mark sun as atmosphere sun: {e}')

        sky = spawn(SkyLight, 'SkyLight', FVector(0, 0, 500))
        if sky is not None:
            slc = sky.LightComponent
            slc.SetMobility(self._MOVABLE)
            try:
                slc.bRealTimeCapture = True   # captures the SkyAtmosphere live
            except Exception as e:
                ue.log_warning(f'watermap: real-time sky capture unavailable: {e}')
            slc.SetIntensity(self.SKY_LIGHT_INTENSITY)
            try:
                slc.RecaptureSky()
            except Exception:
                pass

        fog = spawn(ExponentialHeightFog, 'ExponentialHeightFog')
        if fog is not None:
            try:
                fog.Component.SetFogDensity(self.FOG_DENSITY)
            except Exception as e:
                ue.log_warning(f'watermap: fog density not set: {e}')

        ue.log(f'watermap: spawned {len(self.lighting_actors)} lighting actors')

    # UE Water plugin bodies the script looks for (placed in the editor).
    UE_WATER_BODY_CLASSES = ('WaterBodyOcean', 'WaterBodyLake',
                             'WaterBodyCustom', 'WaterBodyRiver')
    UE_WATER_PHYSICS_CLASS = 'WaterPhysics_WaterBody'   # "Water Physics - UE4 Water Body"
    # Exact Gerstner waves for physics (False) vs. the plugin's cheaper
    # approximation (True).
    UE_WATER_SIMPLE_WAVES = True   # exact (False) crashes: Water plugin asserts IsInGameThread from WaterPhysics worker threads

    # Float the balls with WaterPhysics' link to the UE ocean (True), or keep
    # the ocean as visuals only and float them on the flat Water Volume plus
    # the Python fake waves (False). The link crashes on this engine: the
    # trial's UEWaterIntegration queries the Water plugin from worker
    # threads and it asserts IsInGameThread, with exact AND simple waves.
    USE_UE_WATER_PHYSICS = False

    def _ocean_visual_volume_physics(self, bodies, physics, planes):
        """Ocean for looks, flat volume for physics. For this play session
        only: remove the crashing "Water Physics - UE4 Water Body" actor,
        hide the old planes, and record where the volume should go (just
        outside the ocean's coastline, top face at the ocean surface) so
        _setup_water_volume moves it there. Returns None so the caller
        falls back to the volume setup."""
        if physics is not None:
            name = physics.get_name()
            try:
                physics.K2_DestroyActor()
                ue.log(f'watermap: removed {name} for this session (its ocean link crashes)')
            except Exception as e:
                ue.log_warning(f'watermap: could not remove {name}: {e}')
        for p in planes:
            try:
                p.SetActorHiddenInGame(True)
                p.SetActorEnableCollision(False)
            except Exception:
                pass

        body = bodies[0]
        loc = body.get_actor_location()
        x, y = loc.x, loc.y
        if body.get_class().get_name() == 'WaterBodyOcean':
            pts = self._spline_points(body)
            if pts:
                import builtins   # `from cli import *` shadows sum/max
                cx = builtins.sum(p.x for p in pts) / len(pts)
                cy = builtins.sum(p.y for p in pts) / len(pts)
                radius = builtins.max(math.hypot(p.x - cx, p.y - cy) for p in pts)
                x, y = cx + radius + self.OCEAN_DROP_MARGIN + self.OCEAN_VOLUME_HALF_SIZE, cy
        self._volume_target = FVector(x, y, loc.z)
        ue.log(f'watermap: ocean is visual only; flat water volume will sit at '
               f'({x:.0f}, {y:.0f}) with its surface at the ocean height Z={loc.z:.0f}')
        return None

    # Half-size (UU) of the flat volume when it's moved next to the ocean.
    OCEAN_VOLUME_HALF_SIZE = 3000.0
    OCEAN_VOLUME_DEPTH = 1600.0

    def _setup_ue_water(self):
        """If the level has a UE Water Body, drive the balls with it:
        link it to a "Water Physics - UE4 Water Body" actor (found or
        spawned), so buoyancy follows the same waves you see. In this play
        session only, the old flat setup (Water Physics volumes + the
        engine Plane) is removed/hidden and the Python fake waves are
        switched off. Returns the water physics actor, or None to fall back
        to the volume setup."""
        bodies, physics, volumes, planes = [], None, [], []
        # Match subclasses too (e.g. a Blueprint ocean), not just exact names.
        water_body_cls = ue.find_class('WaterBody')
        waterish = []
        for a in world.all_actors():
            try:
                cls = a.get_class().get_name()
            except Exception:
                continue
            if 'water' in cls.lower() or 'water' in a.get_name().lower():
                waterish.append(f'{a.get_name()} ({cls})')
            is_body = cls in self.UE_WATER_BODY_CLASSES
            if not is_body and water_body_cls is not None \
                    and not cls.startswith('WaterPhysics'):
                try:
                    is_body = bool(a.is_a(water_body_cls))
                except Exception:
                    pass
            if is_body:
                bodies.append(a)
            elif cls == self.UE_WATER_PHYSICS_CLASS and physics is None:
                physics = a
            elif cls == self.WATER_VOLUME_CLASS:
                volumes.append(a)
            elif cls == 'StaticMeshActor':
                try:
                    mesh = a.StaticMeshComponent.StaticMesh
                    if mesh is not None and mesh.get_name() == 'Plane':
                        planes.append(a)
                except Exception:
                    pass

        ue.log(f'watermap: water-related actors in level: {waterish or "none"}')
        if not bodies:
            ue.log('watermap: no UE Water Body in level; using flat Water Physics volume. '
                   'To add an ocean, stop Play and run in the Python console: '
                   'import maps.watermap.build_water_level as b; b.build()')
            return None

        if not self.USE_UE_WATER_PHYSICS:
            return self._ocean_visual_volume_physics(bodies, physics, planes)

        if physics is None:
            cls = ue.find_class(self.UE_WATER_PHYSICS_CLASS)
            if cls is None:
                ue.log_warning('watermap: UEWaterIntegration class not found; '
                               'using flat Water Physics volume')
                return None
            # One spawned now would run BeginPlay with an empty Water Bodies
            # list and never bind to the ocean's overlap events (balls fall
            # straight through). Fall back to the flat volume, which works.
            ue.log_warning(
                'watermap: ocean found but no "Water Physics - UE4 Water Body" placed in '
                'the level; using the flat water volume instead. To float on the ocean '
                'waves, stop Play and run: import importlib, '
                'maps.watermap.build_water_level as b; importlib.reload(b); b.build()')
            return None

        try:
            existing = list(physics.WaterBodies or [])
        except Exception:
            existing = []
        if existing:
            # Configured in the editor (by build_water_level). Re-apply the
            # wave mode for the same bodies: exact waves crash (the Water
            # plugin asserts IsInGameThread when WaterPhysics queries it from
            # worker threads), and a level saved earlier may still have them.
            # The bodies are unchanged, so the overlap binding from BeginPlay
            # still holds.
            try:
                from unreal_engine.structs import WaterBodySetup
                physics.WaterBodies = [
                    WaterBodySetup(WaterBody=e.WaterBody, bIncludeWaves=True,
                                   bUseSimpleWaves=self.UE_WATER_SIMPLE_WAVES,
                                   bIncludeVelocity=True)
                    for e in existing]
                ue.log(f'watermap: water physics {physics.get_name()}: '
                       f'{len(existing)} water body/bodies, simple waves='
                       f'{self.UE_WATER_SIMPLE_WAVES}')
            except Exception as e:
                ue.log_warning(f'watermap: could not set wave mode ({e}); using the '
                               f'flat water volume to avoid the exact-wave crash')
                return None
        else:
            # Placed but never pointed at the ocean: same problem as above.
            ue.log_warning(
                f'watermap: {physics.get_name()} has an empty Water Bodies list; using '
                f'the flat water volume instead. Add the ocean to its Water Bodies list '
                f'in the editor (or rerun build_water_level with importlib.reload).')
            return None

        # The old flat setup would fight the real water: drop it for this
        # session only (PIE runs on a copy of the level, so nothing is lost).
        for v in volumes:
            name = v.get_name()   # read before destroying: a dead actor can't be queried
            try:
                v.K2_DestroyActor()
                ue.log(f'watermap: removed flat water volume {name} for this session')
            except Exception as e:
                ue.log_warning(f'watermap: could not remove {name}: {e}')
        for p in planes:
            try:
                p.SetActorHiddenInGame(True)
                p.SetActorEnableCollision(False)
                ue.log(f'watermap: hid old water plane {p.get_name()} for this session')
            except Exception:
                pass

        # Real waves now come from the water body.
        self.WAVES_ENABLED = False

        # Where to drop the balls. An ocean's spline is its COASTLINE: water
        # fills everything outside the loop and the inside is a hole meant
        # for an island. So for an ocean, drop just outside the loop; for
        # lakes/custom bodies (water inside the spline), drop at the centre.
        body = bodies[0]
        loc = body.get_actor_location()
        self.water_surface_z = loc.z
        drop_x, drop_y = loc.x, loc.y
        if body.get_class().get_name() == 'WaterBodyOcean':
            pts = self._spline_points(body)
            if pts:
                # builtins.*: `from cli import *` shadows sum (and maybe
                # max) with shell-command wrappers.
                import builtins
                cx = builtins.sum(p.x for p in pts) / len(pts)
                cy = builtins.sum(p.y for p in pts) / len(pts)
                radius = builtins.max(math.hypot(p.x - cx, p.y - cy) for p in pts)
                drop_x = cx + radius + self.OCEAN_DROP_MARGIN
                drop_y = cy
                ue.log(f'watermap: ocean coastline centre=({cx:.0f}, {cy:.0f}) '
                       f'radius={radius:.0f}; dropping balls outside it')
            else:
                ue.log_warning('watermap: could not read the ocean spline; '
                               'dropping at the ocean origin (may be inside its island hole)')
        self.ICON_BALLS_ORIGIN = FVector(drop_x, drop_y, loc.z + self.ICON_BALLS_DROP_HEIGHT)
        ue.log(f'watermap: UE water surface ~Z={loc.z:.0f}; balls spawn at {self.ICON_BALLS_ORIGIN}')
        return physics

    # UU past the ocean's coastline loop to drop the balls (open water).
    OCEAN_DROP_MARGIN = 3000.0
    _SPLINE_WORLD = 1   # ESplineCoordinateSpace::World

    def _spline_points(self, body):
        """World-space points of a water body's spline, or [] if unreadable."""
        spl = None
        try:
            spl = body.GetWaterSpline()
        except Exception:
            pass
        if spl is None:
            try:
                from unreal_engine.classes import SplineComponent
                spl = body.get_actor_component_by_type(SplineComponent)
            except Exception:
                spl = None
        if spl is None:
            return []
        try:
            n = spl.GetNumberOfSplinePoints()
            return [spl.GetLocationAtSplinePoint(i, self._SPLINE_WORLD) for i in range(n)]
        except Exception as e:
            ue.log_warning(f'watermap: reading spline points failed: {e}')
            return []

    def _make_water_planes_non_solid(self, surface_z):
        """The visible water is a StaticMeshActor using /Engine/BasicShapes/
        Plane, which has collision on by default. Balls land on it like a
        floor and roll instead of floating in the physics volume, so turn
        its collision off (visual only). Also warn if it isn't at the
        volume's surface height."""
        for a in world.all_actors():
            try:
                if a.get_class().get_name() != 'StaticMeshActor':
                    continue
                smc = a.StaticMeshComponent
                mesh = smc.StaticMesh
                if mesh is None or mesh.get_name() != 'Plane':
                    continue
                a.SetActorEnableCollision(False)
                z = a.get_actor_location().z
                ue.log(f'watermap: collision off on water plane {a.get_name()} (Z={z:.0f})')
                if abs(z - surface_z) > 50.0:
                    ue.log_warning(
                        f'watermap: water plane {a.get_name()} is at Z={z:.0f} but the '
                        f'water volume surface is Z={surface_z:.0f}; balls will float '
                        f'{surface_z - z:+.0f} UU off the visible water. Move the plane '
                        f'or resize the volume so they match.')
            except Exception as e:
                ue.log_warning(f'watermap: could not check {a}: {e}')

    def _setup_water_volume(self):
        """Return the level's WaterPhysics Water Volume, spawning one that
        matches the water mesh if the level doesn't have one. Uses the
        Trace overlap method so icon balls are picked up even if their
        sphere doesn't generate overlap events."""
        # If the level has volumes, use the biggest one (by XY footprint).
        volume, best_area = None, -1.0
        for a in world.all_actors():
            try:
                if a.get_class().get_name() != self.WATER_VOLUME_CLASS:
                    continue
                ext = a.GetBoxComponent().GetScaledBoxExtent()
                area = ext.x * ext.y
                if area > best_area:
                    volume, best_area = a, area
            except Exception:
                continue

        if volume is None:
            cls = ue.find_class(self.WATER_VOLUME_CLASS)
            if cls is None:
                ue.log_warning('watermap: WaterPhysics plugin class not found; '
                               'icon balls will not float')
                return None
            c = self.WATER_CENTER
            volume = world.actor_spawn(
                cls, FVector(c.x, c.y, self.WATER_SURFACE_Z - self.WATER_DEPTH / 2),
                FRotator(0, 0, 0))
            box = volume.GetBoxComponent()
            box.SetBoxExtent(FVector(self.WATER_HALF_SIZE_XY,
                                     self.WATER_HALF_SIZE_XY,
                                     self.WATER_DEPTH / 2))
            ue.log(f'watermap: spawned water volume, surface at Z={self.WATER_SURFACE_Z}')
        else:
            ue.log(f'watermap: using level water volume {volume.get_name()}')

        target = getattr(self, '_volume_target', None)
        if target is not None:
            # Ocean-as-visuals mode: put the volume in open water next to the
            # ocean, top face at the ocean surface.
            try:
                volume.GetBoxComponent().SetBoxExtent(FVector(
                    self.OCEAN_VOLUME_HALF_SIZE, self.OCEAN_VOLUME_HALF_SIZE,
                    self.OCEAN_VOLUME_DEPTH / 2))
                volume.set_actor_scale(FVector(1, 1, 1))
                volume.set_actor_location(FVector(
                    target.x, target.y, target.z - self.OCEAN_VOLUME_DEPTH / 2))
            except Exception as e:
                ue.log_warning(f'watermap: could not move water volume to the ocean: {e}')

        try:
            volume.SetOverlapMethod(1, True)   # EWaterVolumeOverlapMethod::Trace
        except Exception as e:
            ue.log_warning(f'watermap: SetOverlapMethod failed: {e}')

        # Drop the balls above the middle of whichever volume we ended up
        # with: top face of the box = water surface.
        try:
            loc = volume.get_actor_location()
            ext = volume.GetBoxComponent().GetScaledBoxExtent()
            surface_z = loc.z + ext.z
            self.water_surface_z = surface_z
            self._make_water_planes_non_solid(surface_z)
            self.ICON_BALLS_ORIGIN = FVector(loc.x, loc.y, surface_z + self.ICON_BALLS_DROP_HEIGHT)
            ue.log(f'watermap: volume center=({loc.x:.0f}, {loc.y:.0f}, {loc.z:.0f}) '
                   f'half-size=({ext.x:.0f}, {ext.y:.0f}, {ext.z:.0f}) '
                   f'surface Z={surface_z:.0f}; balls spawn at {self.ICON_BALLS_ORIGIN}')
        except Exception as e:
            ue.log_warning(f'watermap: could not read volume bounds ({e}); '
                           f'using default spawn point {self.ICON_BALLS_ORIGIN}')
        return volume

    def spawn_icon_balls(self):
        """Queue desktop icons (like StaringAtSkyMap) to spawn one at a time
        above the water; _tick_icon_balls does the actual spawning."""
        from icon_to_image import get_folder_icons

        # Prefer real UE water (Water Body Ocean/Lake/Custom placed in the
        # level); fall back to the flat Water Physics volume + plane.
        self.ue_water = self._setup_ue_water()
        if self.ue_water is None:
            self.water_volume = self._setup_water_volume()

        self.icon_balls = []        # hold refs so GC doesn't eat them
        self._icon_ball_queue = []
        self._icon_ball_timer = 0.0
        folder = os.path.join(os.path.expanduser('~'), 'Desktop')
        try:
            self._icon_ball_queue = list(get_folder_icons(folder).items())[:self.ICON_BALLS_MAX]
        except Exception as e:
            ue.log_warning(f'spawn_icon_balls: scan "{folder}" failed: {e}')

    def _tick_icon_balls(self, delta_time):
        queue = getattr(self, '_icon_ball_queue', None)
        if not queue:
            return
        self._icon_ball_timer -= delta_time
        if self._icon_ball_timer > 0:
            return
        self._icon_ball_timer = self.ICON_BALLS_INTERVAL

        loc = self._free_icon_ball_spot()
        if loc is None:
            return   # crowded right now; try again next interval
        path, pil_img = queue.pop(0)
        v = self.ICON_BALLS_SPEED
        try:
            actor = spawn_icon(pil_img, location=loc, source_path=path)
            if actor is None:
                return
            sphere = actor.get_actor_component('Sphere')
            try:
                sphere.SetCastShadow(False)   # icon balls don't cast shadows
            except Exception as e:
                ue.log_warning(f'spawn_icon_balls: could not turn off shadow: {e}')
            sphere.SetSimulatePhysics(True)
            try:
                sphere.SetMassOverrideInKg('None', self.ICON_BALL_MASS_KG, True)
            except Exception as e:
                ue.log_warning(f'spawn_icon_balls: mass override failed: {e}')
            actor.set_actor_location(loc, False, True)   # teleport the physics body too
            sphere.SetPhysicsLinearVelocity(FVector(
                random.uniform(-v, v), random.uniform(-v, v), 0.0))
            self.icon_balls.append(actor)
            if getattr(self, 'ue_water', None) is not None:
                # Don't call AddActorToWater here: the ball is still in the
                # air, and the plugin ensure()s ("Tried to get water info in
                # actor which is not in any water body"). It adds balls
                # itself when they overlap the water body — which needs
                # overlap events on.
                try:
                    sphere.SetGenerateOverlapEvents(True)
                except Exception as e:
                    ue.log_warning(f'watermap: could not enable overlap events: {e}')
            if len(self.icon_balls) == 1:
                # Diagnostic: confirm the icon material actually landed.
                try:
                    m = sphere.GetMaterial(0)
                    ue.log(f'watermap: first icon ball material = '
                           f'{m.get_name() if m else None} '
                           f'(parent {m.Parent.get_name() if m and getattr(m, "Parent", None) else "?"})')
                except Exception as e:
                    ue.log_warning(f'watermap: could not read ball material: {e}')
        except Exception as e:
            ue.log_warning(f'spawn_icon_balls: failed for "{path}": {e}')
        if not queue:
            ue.log(f'spawn_icon_balls: spawned {len(self.icon_balls)} at {self.ICON_BALLS_ORIGIN}')

    def _free_icon_ball_spot(self, tries=20):
        """Random point within ±ICON_BALLS_RANGE of the origin that isn't
        inside an already-spawned ball (spawning overlapped = flung)."""
        o, r, gap = self.ICON_BALLS_ORIGIN, self.ICON_BALLS_RANGE, self.ICON_BALLS_MIN_GAP
        others = []
        for b in self.icon_balls:
            try:
                others.append(b.get_actor_location())
            except Exception:
                pass
        for _ in range(tries):
            p = FVector(o.x + random.uniform(-r, r),
                        o.y + random.uniform(-r, r),
                        o.z + random.uniform(-r, r))
            if all((p.x - q.x) ** 2 + (p.y - q.y) ** 2 + (p.z - q.z) ** 2 >= gap * gap
                   for q in others):
                return p
        return None

    def move_icon(self):
        # self.icon.get_actor_component('PhysicsHandle').SetTargetLocation(FVector(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))) # not needed
        # self.icon.get_actor_component('Sphere').SetSimulatePhysics(False) # not needed
        self.icon.set_actor_transform(FTransform(FVector(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)), FRotator(0, 0, 0), FVector(1, 1, 1)))
        # self.icon.get_actor_component('Sphere').SetSimulatePhysics(True) # not needed

    def test_cylinder(self):
        ue.log("testing cylinder:")

        point1 = FVector(0, 0, 0)
        point2 = FVector(100, 100, 100)
        midpoint = (point1 + point2) / 2
        distance_between_points = KismetMathLibrary.Vector_Distance(point1, point2)
        cylinder_rotation = KismetMathLibrary.FindLookAtRotation(point1, point2)  # returns FRotator
        cylinder_rotation.pitch += 90
        cylinder = world.actor_spawn(StaticMeshActor)
        cylinder_mesh = ue.load_object(StaticMesh, '/Engine/BasicShapes/Cylinder')
        smc = cylinder.StaticMeshComponent
        smc.SetStaticMesh(cylinder_mesh)
        smc.Mobility = EComponentMobility.Movable
        transform = FTransform(midpoint, cylinder_rotation, FVector(.1, .1, distance_between_points/100))
        cylinder.set_actor_transform(transform)
        # FTransform().get_matrix() # if needed

    def test_text(self):
        ue.log("testing text:")
        cell_class = load_blueprint_class('/Game/Blueprints/Assets/BP_Cell.BP_Cell')
        cell_actor = world.actor_spawn(cell_class)
        transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
        cell_actor.set_actor_transform(transform)
        cell_actor.get_actor_component('Text3DComponent').Text = "HI"
        # print(cell_actor.get_actor_rotation().quaternion())
