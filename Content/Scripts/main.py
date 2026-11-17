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
# BUG: imported classes are not reloaded, you need to restart the editor
# Code placed outside the Main class will not run when connecting to a server and may run twice
# You can ignore and delete .uasset files as you'd like. They are regenerated on run

ue.log('I am a Python module.')

#TODO: Completely empty main.py
def get_public_ip_via_dns(resolver="8.8.4.4", timeout=3.0):
    """Ask Google Public DNS for our public IP by querying the special TXT
    record o-o.myaddr.l.google.com, which the resolver answers with the
    client's egress IP. In-process UDP DNS, no HTTP server hop."""
    # serious shit below
    # identity function be like
    qname = b"".join(struct.pack("B", len(p)) + p
                     for p in b"o-o.myaddr.l.google.com".split(b".")) + b"\x00"
    # Header: id=0x1234, RD flag set, 1 question; QTYPE=16 (TXT), QCLASS=1 (IN)
    query = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0) + qname + struct.pack(">HH", 16, 1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.settimeout(timeout)
        sock.sendto(query, (resolver, 53))
        resp, _ = sock.recvfrom(512)
    finally:
        sock.close()
    # Skip the echoed header(12) + question, then walk to the TXT rdata.
    idx = 12
    while resp[idx] != 0:
        idx += resp[idx] + 1
    idx += 5  # null label byte + QTYPE(2) + QCLASS(2)
    # Answer RR: name(2, compressed ptr) type(2) class(2) ttl(4) rdlen(2)
    idx += 12
    txt_len = resp[idx]  # first byte of TXT rdata is the string length
    return resp[idx + 1: idx + 1 + txt_len].decode("ascii")

# Use this if you want to rebuild the unreal_engine intellisense(.pyi, etc.) and cli
rebuild_generated_modules()

# ret = ue.message_dialog_open(ue.APP_MSG_TYPE_YES_NO, "Do you want to test dialogs?")
# if ret == ue.APP_RETURN_TYPE_YES:
#     ue.log('You choose "YES"')

# help_cmd("ls")

class Main:
    def end_play(self, reason):
        ue.log("Ending play")
        import unreal_engine_tools
        unreal_engine_tools.invalidate_world_cache()
        for i, ticker in enumerate(tickers):
            ue.remove_ticker(ticker)
            del tickers[i]
            print(ticker, "stopped.")
            self.input.release_mouse()
        if hasattr(self, 'input'):
            self.input.shutdown()

    def ctrl_shift_b(self):
        ue.log("Pressed Ctrl+Shift+B")

    def left_click(self):
        ue.log("Left mouse button")

    def mouse_wheel(self, value):
        ue.log("Wheel: {}".format(value))

    def sequence_action(self):
        ue.log("Sequence fired: Ctrl+K → MouseX → Click")

    def print_mouse_world(self):
        data = self.input.get_mouse_position(deproject=True)
        if not data:
            return
        x, y, world, dir = data
        ue.log(f"Mouse {x},{y}")
        ue.log(f"World {world} Dir {dir}")

    def on_move_forward(self, value):
        """Handle analog movement input"""
        if value != 0:
            ue.log(f"Moving forward: {value:.2f}")
            # Add movement code here

    def interact(self):
        """Interaction bound to multiple keys"""
        ue.log("Interact!")
        # Perform interaction

    def toggle_window_transparency(self):
        """T-key: flip the game window between per-pixel transparent (DWM) and opaque.
        First call lazily resolves UWindowTransparencyLibrary and caches a transient
        instance — UEP's pattern for invoking static UFUNCTIONs on a
        UBlueprintFunctionLibrary (matches ue_spawn.spawn_gltf_runtime's lib usage).
        No-op in PIE / editor — the underlying library guards on GIsEditor."""
        if not hasattr(self, "_wt_lib") or self._wt_lib is None:
            wt_cls = ue.find_class("WindowTransparencyLibrary")
            if wt_cls is None:
                ue.log_warning(
                    "toggle_window_transparency: WindowTransparencyLibrary not found — "
                    "is the WindowTransparency plugin enabled and compiled?")
                return
            self._wt_lib = ue.new_object(wt_cls)
            self._window_transparent = False

        if self._window_transparent:
            self._wt_lib.call_function("DisableWindowTransparency")
            self._window_transparent = False
            ue.log("Window transparency: OFF")
        else:
            # bKeepBorder=True matches the C++ default; flip to False for borderless.
            self._wt_lib.call_function("EnableWindowTransparency", True)
            self._window_transparent = True
            ue.log("Window transparency: ON")

    def shift_click(self):
        """Shift + Click action"""
        ue.log("Shift + Click")
        # Multi-select logic, etc.

    def on_ctrl_shift_b(self):
        ue.log("Pressed Ctrl+Shift+B")

    def on_left_click(self):
        ue.log("Left mouse button clicked")

    def check_key_states(self):
        """Example of manually checking key states without binding"""
        if self.input.is_key_down("W"):
            ue.log("W is currently down")
        if self.input.is_key_down("LeftControl"):
            ue.log("Left Control is currently down")
        if self.input.is_chord_down("Ctrl+Shift"):
            ue.log("Ctrl+Shift combo is down")

    def print_mouse_world(self):
        """Print mouse screen position and world projection"""
        data = self.input.get_mouse_position(deproject=True)
        if not data:
            ue.log("Could not get mouse position")
            return

        x, y, world, direction = data
        ue.log(f"Mouse Screen: ({x:.1f}, {y:.1f})")
        ue.log(f"World Pos: {world}")
        ue.log(f"World Dir: {direction}")

    def print_cursor_and_trace(self):
        """Get and print cursor info using the new get_cursor_info() method"""
        # Method 1: Using get_cursor_info()
        cursor_info = self.input.get_cursor_info()
        if cursor_info:
            ue.log("=== CURSOR INFO ===")
            ue.log(f"Screen X: {cursor_info['screen_x']:.1f}")
            ue.log(f"Screen Y: {cursor_info['screen_y']:.1f}")
            ue.log(f"World Pos: {cursor_info['world_pos']}")
            ue.log(f"World Dir: {cursor_info['world_dir']}")

        # Method 2: Trace to see what we're pointing at
        hit = self.trace.trace_cursor()
        if hit:
            ue.log(f"Hit Actor: {hit.get('actor')}")
            ue.log(f"Hit Location: {hit.get('location')}")
        else:
            ue.log("No hit under cursor")

    def trace_from_cursor(self):
        """Trace from cursor into the world"""
        ue.log("=== CURSOR TRACE ===")
        hit = self.trace.trace_cursor(ECollisionChannel.ECC_Visibility)

        if hit:
            actor = hit.get('actor')
            location = hit.get('location')
            normal = hit.get('normal')

            ue.log(f"Hit Actor: {actor.get_name() if actor else 'None'}")
            ue.log(f"Hit Location: {location}")
            ue.log(f"Hit Normal: {normal}")
        else:
            ue.log("Nothing hit under cursor")

    def trace_from_camera(self):
        """Trace forward from camera/pawn"""
        ue.log("=== FORWARD TRACE ===")
        hit = self.trace.trace_forward(dist=5000)

        if hit:
            actor = hit.get('actor')
            location = hit.get('location')

            ue.log(f"Hit Actor: {actor.get_name() if actor else 'None'}")
            ue.log(f"Hit Location: {location}")
            ue.log(f"Distance: {hit.get('distance', 0):.1f}")
        else:
            ue.log("Nothing hit in forward trace")

    def print_key_registry(self, key):
        """Print all bindings registered for a specific key"""
        bindings = self.input.get_key_bindings(key)
        ue.log(f"=== Bindings for '{key}' ===")
        for binding in bindings:
            ue.log(f"  Type: {binding['type']}, Keys: {binding['keys']}, Callback: {binding['callback']}")

    def move_icon(self):
        # self.icon.get_actor_component('PhysicsHandle').SetTargetLocation(FVector(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))) # not needed
        # self.icon.get_actor_component('Sphere').SetSimulatePhysics(False) # not needed
        self.icon.set_actor_transform(FTransform(FVector(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100)), FRotator(0, 0, 0), FVector(1, 1, 1)))
        # self.icon.get_actor_component('Sphere').SetSimulatePhysics(True) # not needed

    # this is called on game start
    def begin_play(self):
        ue.log('Begin Play on Main class')
        change_background("transparent")  # window-transparency test — green sky punches through to desktop
        ue.log('Running startup')
        startup()

        # Stop the background music
        bg_music = find_actor("BackgroundMusic")
        if bg_music is not None:
            for ac in bg_music.get_components_by_type(AudioComponent):
                ac.call('Stop')

        global world
        world = get_world()
        print("begin_play found world", world)
        unreal_engine_tools.world = world
        # print(world)
        global tickers
        tickers = []

        is_dedicated_server = KismetSystemLibrary.IsDedicatedServer(self.uobject)

        if not is_dedicated_server:
            self.uobject.enable_input()

            self.keyboard = Keyboard()
            self.mouse = Mouse()

            self.input = HotkeyManager(self.uobject, self.keyboard, self.mouse)
            self.trace = TraceHelper(self.uobject)

            self.input.bind_press("M", self.input.toggle_cursor)
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
                bp_drone = ue.load_object(Blueprint, '/Game/Blueprints/Assets/DroneCharacter/BP_PyDroneCharacter.BP_PyDroneCharacter')
                player = world.actor_spawn(bp_drone.GeneratedClass)
                transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
                player.set_actor_transform(transform)
                # player.get_actor_component('Text3DComponent').Text = "HI"
                player_controller.Possess(player)
                py_player = player.get_py_proxy()
                py_player._setup_input()

                # print("Begin StickMan Possession")
                # bp_stickman = ue.load_object(Blueprint, '/Game/ThirdPersonCPP/Blueprints/StickManCharacter.StickManCharacter')
                # player = world.actor_spawn(bp_stickman.GeneratedClass)
                # transform = FTransform(FVector(100, 100, 200), FRotator(0, 0, 0), FVector(1, 1, 1))
                # player.set_actor_transform(transform)
                # uobject.get_player_controller().Possess(player)
                # py_player = player.get_py_proxy()
                # py_player._setup_input()

                # apply_material(
                #     actor_name="StickManCharacter",  # runtime instance name (check via print)
                #     component_name="SkeletalMeshOutline",
                #     material_path="/Game/Materials/M_Outline.M_Outline",
                #     params={
                #         "LineThickness": 3.0,
                #         "Color": (0, 0, 0, 1),
                #     }
                # )
                # apply_material(
                #     actor_name="StickManCharacter",  # runtime instance name (check via print)
                #     component_name="SkeletalMeshHeadlessOutline",
                #     material_path="/Game/Materials/M_Outline.M_Outline",
                #     params={
                #         "LineThickness": 3.0,
                #         "Color": (0, 0, 0, 1),
                #     }
                # )

                global RPC_ACTOR, SERVER_HELPER

                if not RPC_ACTOR:
                    print("RPC_ACTOR not found, making one")
                    try:
                        ue.log("Server making a LargeStringRPCActor.")
                        RPC_ACTOR = world.actor_spawn(LargeStringRPCActor)
                        RPC_ACTOR.SetOwner(player_controller)
                        RPC_ACTOR.LargeString = ue.new_object(LargeStringAsync)  # attach ULargeStringAsync
                        print("Created new LargeStringAsync instance", RPC_ACTOR, RPC_ACTOR.LargeString)

                        # Bind the C++ event manually after creating LargeString
                        try:
                            RPC_ACTOR.LargeString.bind_event('OnFullyReceived', RPC_ACTOR.Server_OnFullStringReceived)
                            ue.log_warning("[SERVER] Manually bound OnFullyReceived to Server_OnFullStringReceived")
                        except Exception as e:
                            ue.log_error(f"Failed to bind OnFullyReceived: {e}")

                    except Exception as e:
                        ue.log_error(f"Actor creation error: {e}")
                        return
                else:
                    ue.log_warning(f"[SERVER PY] LargeStringRPCActor already created")

                # Create SERVER helper with SERVER callback
                if not SERVER_HELPER:
                    ue.log_warning("[SERVER] Creating SERVER helper")
                    SERVER_HELPER = LargeStringAsyncStandalone(
                        large_string_obj=RPC_ACTOR.LargeString,
                        rpc_actor=RPC_ACTOR,
                        on_received_callback=None,  # Server doesn't need client callback
                        on_server_received_callback=server_on_full_string_received,  # THIS is the key
                        on_progress_callback=None,
                        auto_send=False  # Server doesn't auto-send from OnChunksBuilt
                    )
                    ue.log_warning("[SERVER] Server rpc helper created and bound")
            if gm:
                gm.bind_event("OnPlayerJoined", on_player_joined)
                ue.log_warning("[SERVER] Bound OnPlayerJoined")

            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ue.log(f"Server LAN IP: {local_ip}")
            public_ip = None
            try:
                public_ip = get_public_ip_via_dns()
                ue.log(f"Public IP: {public_ip}")
            except Exception as e:
                ue.log(f"Could not fetch public IP: {e}")
            if public_ip:
                ue.log("If you correctly port forwarded the LAN IP, the server is on the public IP: " + public_ip)
            # # Server-originated multicast test
            # ue.log("Calling test_multicast_flag() from server")
            # self.test_multicast_flag("hello via multicast flag")

        else:
            if self.uobject.HasAuthority():
                ue.log("BeginPlay on LISTEN SERVER / STANDALONE (has authority)")
            else:
                ue.log("BeginPlay on CLIENT (connected to remote server)")


            apply_material(
                actor_name="TestSphere",  # M_Color is default
                material_path="/Game/Materials/M_Color.M_Color",
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

        if not is_dedicated_server:
            # Explicit drone possession method (same as master's main.py): spawn
            # BP_PyDroneCharacter and Possess it so it overrides whatever pawn the
            # GameMode auto-possessed. Single possession only — the duplicate
            # post_startup() possession below is disabled (master has none).
            print("Begin Drone Possession")
            bp_drone = ue.load_object(Blueprint, '/Game/Blueprints/Assets/DroneCharacter/BP_PyDroneCharacter.BP_PyDroneCharacter')
            player = world.actor_spawn(bp_drone.GeneratedClass)
            transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
            player.set_actor_transform(transform)
            self.uobject.get_player_controller().Possess(player)
            py_player = player.get_py_proxy()
            py_player._setup_input()


            self.test_kingdon()
            # self.test_cylinder()
            # self.test_text()

            results = test_spawn_all(uobject=self.uobject, input_manager=self.input, tests=['test_text3d_click', 'test_text3d_executor'])
            print(results)

        # post_startup() re-spawned and possessed a second drone (with a stale
        # world global), competing with the possession done above. Disabled so
        # there is a single possession method in main.py, as on master.
        # post_startup(self.uobject)




    # this is called at every 'tick'
    def tick(self, delta_time):
        # get current location
        location = self.uobject.get_actor_location()
        # increase Z honouring delta_time
        location.z += 100 * delta_time
        # set new location
        self.uobject.set_actor_location(location)

        # self.input.print_cursor_info()

        # Gizmo + Text3D ticks now run on their own PyActors
        # (pyactor_gizmo.GizmoController, pyactor_global_click.PyActorGlobalClick).


    def test_kingdon(self):
        import unicodedata
        ue.log("testing kingdon:")
        from kingdon import Algebra
        alg = Algebra(3, 0, 1)
        locals().update(alg.blades)
        b = alg.bivector(name='b')
        ue.log(unicodedata.normalize('NFKC', str(b)))

    def test_cylinder(self):
        ue.log("testing cylinder:")
        # new_actor = world.actor_spawn(Actor)
        # new_actor.set_actor_label('Test Actor')
        # new_actor.add_actor_root_component(InstancedStaticMeshComponent, 'Root')
        # instanced_component = actor.get_component_by_type(InstancedStaticMeshComponent)
        # instanced_component.StaticMesh = mesh
        # instanced_component.PerInstanceSMData = [
        #     InstancedStaticMeshInstanceData(Transform=FTransform(FVector(0, 0, 200), FRotator(90, 90, 0)).get_matrix()),
        #     InstancedStaticMeshInstanceData(Transform=FTransform(FVector(0, 0, 0), FRotator(90, 90, 45)).get_matrix()),
        # ]
        # instanced_component = actor.get_component_by_type(InstancedStaticMeshComponent # if you need to access the component again, you need to retrieve it back as the old instance will be garbaged

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
        # print(transform)
        cylinder.set_actor_transform(transform)
        # FTransform().get_matrix() # if needed

    def test_text(self):
        ue.log("testing text:")
        bp_cell = ue.load_object(Blueprint, '/Game/Blueprints/Assets/BP_Cell.BP_Cell')
        cell_actor = world.actor_spawn(bp_cell.GeneratedClass)
        transform = FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), FVector(1, 1, 1))
        cell_actor.set_actor_transform(transform)
        cell_actor.get_actor_component('Text3DComponent').Text = "HI"
        # print(cell_actor.get_actor_rotation().quaternion())
