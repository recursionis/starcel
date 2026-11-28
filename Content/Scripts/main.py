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
        ue.log('Begin Play on Main class')
        change_background("sky")  # BP_SkySphere with the sun (time-of-day sun position)
        ue.log('Running startup')
        startup()

        global world
        world = get_world()
        print("begin_play found world", world)
        unreal_engine_tools.world = world
        # print(world)

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


            apply_material(
                actor_name="TestSphere",
                material_path="/Game/Materials/M_Color.M_Color", # M_Color is default
                params = {
                    "Color": (0, 1, 0, 1),
                    "Metallic": 0.5,
                    "Specular": 0.5,
                    "Roughness": 0.2,
                    "Anisotropy": 0.1,
                    "Emissive Multiplier": 10.0,
                    "Ambient Occlusion": 1.0,
                }
            )

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

            results = test_spawn_all(uobject=self.uobject, input_manager=self.input, tests=['test_earth'])  # was: ['test_text3d_click', 'test_text3d_executor', 'test_3d_table_5x5x5']
            print(results)

            self.spawn_icon_balls()

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

    # Moving desktop-icon balls, all spawned at one spot with physics on.
    ICON_BALLS_ORIGIN = FVector(5850.0, -230.0, 200.0)
    ICON_BALLS_MAX = 50        # cap on how many desktop icons to spawn
    ICON_BALLS_RANGE = 200.0   # UU; random offset from origin on every axis
    ICON_BALLS_MIN_GAP = 110.0 # UU; min distance between ball centers at spawn (sphere is 100 across)
    ICON_BALLS_INTERVAL = 0.5  # seconds between spawns, so they don't pile up and explode
    ICON_BALLS_SPEED = 150.0   # UU/s; max initial sideways speed

    def spawn_icon_balls(self):
        """Queue desktop icons (like StaringAtSkyMap) to spawn one at a time
        at ICON_BALLS_ORIGIN; _tick_icon_balls does the actual spawning."""
        from icon_to_image import get_folder_icons

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
            sphere.SetSimulatePhysics(True)
            actor.set_actor_location(loc, False, True)   # teleport the physics body too
            sphere.SetPhysicsLinearVelocity(FVector(
                random.uniform(-v, v), random.uniform(-v, v), 0.0))
            self.icon_balls.append(actor)
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
