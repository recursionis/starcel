"""
pyactor_stickman.py — Crosshair overlay for StickManCharacter
==============================================================
Spawns a tiny image plane (same pattern as spawn_image) textured with
crosshair.png and attaches it to the center of the Screen component.

The Screen cube represents the physical display — its size maps 1:1 to
the monitor when fullscreen.  The crosshair is a separate actor parented
to Screen so it stays centered regardless of camera movement.

Blueprint requirements (StickManCharacter):
  • Python component → pyactor_stickman.PyActorStickMan
  • A StaticMeshComponent named `Screen` parented to the first-person
    camera (already exists)

Material note:
  Uses M_TexturePicture for the crosshair plane.
"""

import os
import unreal_engine as ue
from unreal_engine import FVector, FRotator, FTransform

try:
    from unreal_engine.classes import StaticMeshActor, StaticMesh, Material
    from unreal_engine.enums import EComponentMobility
except Exception:
    StaticMeshActor = None
    StaticMesh = None
    Material = None
    EComponentMobility = None

from unreal_engine_tools import find_component


def _spawn_crosshair_plane(world, crosshair_path, material_path, fallback_mat,
                           param_name):
    """
    Spawn a StaticMeshActor cube textured with the crosshair PNG,
    scaled to the image's pixel size (1 px = 1 UU).  Same pattern as
    ue_spawn.spawn_image.

    Returns (actor, img_w, img_h) or (None, 0, 0).
    """
    from PIL import Image as PILImage
    from unreal_engine_tools import pil_image_to_texture

    if not os.path.exists(crosshair_path):
        ue.log_warning(f'PyActorStickMan: crosshair not found: "{crosshair_path}"')
        return None, 0, 0

    try:
        pil_img = PILImage.open(crosshair_path).convert('RGBA')
    except Exception as e:
        ue.log_warning(f'PyActorStickMan: cannot open crosshair: {e}')
        return None, 0, 0

    img_w, img_h = float(pil_img.width), float(pil_img.height)

    # Spawn cube actor
    actor = world.actor_spawn(StaticMeshActor)
    smc = actor.StaticMeshComponent
    cube = ue.load_object(StaticMesh, '/Engine/BasicShapes/Cube.Cube')
    smc.SetStaticMesh(cube)
    smc.Mobility = EComponentMobility.Movable

    # Load material (try primary, then fallbacks)
    mat = None
    mat_paths = [p for p in (material_path, fallback_mat) if p is not None]
    # Also try M_TextureUnlit as extra fallback
    if '/Game/Materials/M_TextureUnlit' not in mat_paths:
        mat_paths.append('/Game/Materials/M_TextureUnlit')
    for mp in mat_paths:
        if mat is not None:
            break
        for path in (mp + '.' + mp.split('/')[-1], mp):
            try:
                mat = ue.load_object(Material, path)
                break
            except Exception:
                pass

    # Apply MID with crosshair texture — destroy actor on failure to avoid
    # leaving a black untextured cube that covers the Screen.
    if mat is None:
        ue.log_warning('PyActorStickMan: no usable material — destroying crosshair '
                       'to avoid black screen')
        actor.actor_destroy()
        return None, 0, 0

    try:
        tex = pil_image_to_texture(pil_img)
        if tex is None:
            ue.log_warning('PyActorStickMan: texture conversion failed — '
                           'destroying crosshair')
            actor.actor_destroy()
            return None, 0, 0
        mid = smc.create_material_instance_dynamic(mat)
        mid.set_material_texture_parameter(param_name, tex)
        smc.set_material(0, mid)
    except Exception as e:
        ue.log_warning(f'PyActorStickMan: MID setup failed: {e} — '
                       'destroying crosshair')
        actor.actor_destroy()
        return None, 0, 0

    # Scale: vertical picture frame, 1 px = 1 UU
    # Cube default = 100 UU per side → divide by 100
    scale = FVector(img_w / 100.0, 0.01, img_h / 100.0)
    actor.set_actor_transform(
        FTransform(FVector(0, 0, 0), FRotator(0, 0, 0), scale))

    return actor, img_w, img_h


class PyActorStickMan:
    """
    Adds a StaticMeshComponent (crosshair cube) to the owning actor and
    attaches it to the Screen component.  Does NOT touch Screen's material.
    """

    # Content/Scripts/assets/crosshair.png — lives under Scripts so it is staged
    # as a raw file in packaged builds (Content/Materials only ships the .uasset).
    crosshair_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'crosshair.png')
    material_paths = (
        '/Game/Materials/M_TexturePicture',
        '/Game/Materials/M_TextureUnlit',
    )
    param_name = 'Texture'
    component_name = 'Screen'
    CROSSHAIR_SCALE = 3.0   # world-size multiplier (1 UU per pixel × this)

    def begin_play(self):
        self.crosshair_comp = None

        from unreal_engine.classes import StaticMeshComponent

        screen = find_component(self.uobject, self.component_name)
        if screen is None:
            ue.log_warning(
                f'PyActorStickMan: no "{self.component_name}" component on '
                f'{self.uobject.get_name()}')
            return

        if not os.path.exists(self.crosshair_path):
            ue.log_warning(f'PyActorStickMan: crosshair not found: '
                           f'"{self.crosshair_path}"')
            return

        try:
            from PIL import Image as PILImage
            from unreal_engine_tools import pil_image_to_texture

            pil_img = PILImage.open(self.crosshair_path).convert('RGBA')
            img_w, img_h = float(pil_img.width), float(pil_img.height)

            # Load material
            mat = None
            mat_name = None
            for mp in self.material_paths:
                if mat is not None:
                    break
                for path in (mp + '.' + mp.split('/')[-1], mp):
                    try:
                        mat = ue.load_object(Material, path)
                        mat_name = mp.split('/')[-1]
                        break
                    except Exception:
                        pass
            if mat is None:
                ue.log_warning('PyActorStickMan: no usable crosshair material')
                return

            tex = pil_image_to_texture(pil_img)
            if tex is None:
                ue.log_warning('PyActorStickMan: texture conversion failed')
                return

            # Spawn a SEPARATE actor for the crosshair (add_actor_component
            # crashes BP actors with construction scripts during begin_play)
            from unreal_engine_tools import get_world
            world = self.uobject.get_world() or get_world()
            actor = world.actor_spawn(StaticMeshActor)
            smc = actor.StaticMeshComponent
            cube = ue.load_object(StaticMesh, '/Engine/BasicShapes/Cube.Cube')
            smc.SetStaticMesh(cube)
            smc.Mobility = EComponentMobility.Movable

            mid = smc.create_material_instance_dynamic(mat)
            mid.set_material_texture_parameter(self.param_name, tex)
            smc.set_material(0, mid)

            actor.attach_to_component(screen)

            # Target WORLD scale: square aspect preserved regardless of
            # Screen's own (possibly non-uniform) scale. 1 UU per pixel ×
            # CROSSHAIR_SCALE, divided by parent scale to yield the relative.
            try:
                p = screen.get_world_scale()
                px = abs(p.x) or 1e-6
                py = abs(p.y) or 1e-6
                pz = abs(p.z) or 1e-6
            except Exception:
                px = py = pz = 1.0
            tgt_wx = img_w * self.CROSSHAIR_SCALE / 100.0
            tgt_wz = img_h * self.CROSSHAIR_SCALE / 100.0
            rel_scale = FVector(tgt_wx / px, 0.001 / py, tgt_wz / pz)
            try:
                actor.set_actor_relative_scale(rel_scale)
            except Exception:
                actor.set_actor_scale(rel_scale)

            # Front face of default cube is at local Y = -50. Add a small
            # world-space epsilon (scaled to local by parent Y) to avoid
            # z-fighting with the Screen plane.
            y_rel = -(50.0 + 0.5 / py)
            actor.K2_SetActorRelativeLocation(FVector(0, y_rel, 0))

            self.crosshair_comp = actor
            ue.log(f'PyActorStickMan: crosshair {int(img_w)}x{int(img_h)} px '
                   f'actor attached to "{self.component_name}" (mat={mat_name})')
        except Exception as e:
            ue.log_warning(f'PyActorStickMan: crosshair spawn failed: {e}')

    # #
    #  Modifier controls (mirrors PyPawnDrone)                             #
    #    Ctrl  + Scroll : grow / shrink (lerped)      [Ctrl > Alt > Shift] #
    #    Shift + Scroll : walk faster / slower                             #
    #    Alt   + Scroll : camera closer / farther (FreeLookSpringArm)     #
    #    Hold Alt       : free look - orbit the camera, snaps back on      #
    #                     release                                          #
    # #

    LERP_SPEED = 20.0
    # Free-look camera / arm names in StickManCharacter, in order of
    # preference (FreeLook* were added in the BP; Follow*/CameraBoom are the
    # C++ ThirdPerson defaults).
    FREELOOK_CAMS = ("FreeLookCamera", "FollowCamera")
    FREELOOK_ARM = "FreeLookSpringArm"

    @staticmethod
    def _set(obj, name, value):
        """Write a UPROPERTY without `obj.Name = value`. In editor builds
        UEP follows a plain assignment with PostEditChangeProperty, which on
        a component of this Blueprint actor reruns the construction script:
        every BP-added component is recreated, this Python component included,
        so all our references (and self.uobject) go invalid and the bindings
        die. set_property writes the value raw, with no editor notification.
        (The drone avoids the same trap with UFUNCTIONs such as
        SetOwnerNoSee / SetFreeLookArmLength.)"""
        obj.set_property(name, value)

    def _setup_input(self):
        """Called by Main.toggle_pawn right after Possess. Binds on the
        character's own InputComponent (not the PlayerController's), so the
        bindings drop out of the input stack automatically on unpossess and
        can't swallow the drone's keys."""
        from constants import FiniteRepetitionSelector
        from input_devices import Keyboard, Mouse, HotkeyManager

        actor = self.uobject.get_owner()
        comp = getattr(actor, "InputComponent", None)
        if comp is None:
            ue.log_warning("PyActorStickMan: _setup_input before Possess; aborting")
            return
        if getattr(self, "_bound_input_component", None) == comp:
            return   # already bound on this InputComponent (re-possess)
        self._bound_input_component = comp

        # Bindings from a previous _setup_input (old InputComponent, or a
        # component that was reinstanced by a BP recompile) must not keep
        # firing into this instance.
        old_input = getattr(self, "input", None)
        if old_input is not None:
            try:
                old_input.shutdown()
            except Exception:
                pass

        self.actor = actor
        # Alt+scroll zooms the free-look camera's arm: the new
        # FreeLookSpringArm when the BP has one, else the C++ CameraBoom.
        self._boom = (find_component(actor, self.FREELOOK_ARM)
                      or find_component(actor, "CameraBoom"))
        if self._boom is not None:
            # The boom's collision probe shortens the arm whenever the ground
            # or a wall is behind the character, so Alt+scroll never showed
            # the full doubled distance.
            self._set(self._boom, "bDoCollisionTest", False)
            # FreeLookSpringArm is left at the SpringArm defaults in the BP
            # (bUsePawnControlRotation = False), so it only inherited the
            # capsule's rotation: yaw because the body turns with the
            # controller, never pitch. Drive it from the control rotation.
            self._set(self._boom, "bUsePawnControlRotation", True)
        try:
            self._move = actor.CharacterMovement
        except Exception:
            self._move = None
        self._target_scale = actor.get_actor_scale()
        self._target_arm_length = self._boom.TargetArmLength if self._boom else None
        self._freelook_rot = None

        # Cameras: the first name in FREELOOK_CAMS that exists is the
        # free-look camera (like the drone's FreeLookCamera). The cameras
        # active at possess time are the normal view; Alt swaps between them.
        from unreal_engine.classes import CameraComponent
        cams = {}
        for c in actor.get_components():
            if c.is_a(CameraComponent):
                cams[c.get_name()] = c
                ue.log(f"PyActorStickMan: camera {c.get_name()} active={c.IsActive()}")
        self._follow_cam = next((cams[n] for n in self.FREELOOK_CAMS if n in cams), None)
        self._normal_cams = [c for c in cams.values()
                             if c is not self._follow_cam and c.IsActive()]
        if self._follow_cam is not None and self._normal_cams:
            self._follow_cam.SetActive(False, False)
        ue.log("PyActorStickMan: free-look camera = "
               f"{self._follow_cam.get_name() if self._follow_cam else None}, "
               f"normal = {[c.get_name() for c in self._normal_cams]}")

        # Meshes: in the normal view the owner sees the headless body; in free
        # look (third person) show the full body instead, like the drone's
        # _set_mesh_owner_no_see. Remember the BP's flags to restore them.
        from unreal_engine.classes import SkeletalMeshComponent
        self._mesh_flags = []
        for c in actor.get_components():
            if c.is_a(SkeletalMeshComponent):
                self._mesh_flags.append(
                    (c, "Headless" in c.get_name(), bool(c.bOwnerNoSee)))

        self.size_selector = FiniteRepetitionSelector(current_operator="*", current_operand=2.0)
        self.speed_selector = FiniteRepetitionSelector(current_operator="*", current_operand=2.0)
        self.arm_selector = FiniteRepetitionSelector(current_operator="*", current_operand=2.0)

        self.input = HotkeyManager(actor, Keyboard(), Mouse())
        self.input.bind_press("LeftAlt", self._on_alt_pressed)
        self.input.bind_release("LeftAlt", self._on_alt_released)
        self.input.bind_press("MouseScrollUp", self._on_scroll_up)
        self.input.bind_press("MouseScrollDown", self._on_scroll_down)
        ue.log("PyActorStickMan: modifier controls bound")

    def _is_typing(self):
        try:
            from actors.pyactor_global_click import PyActorGlobalClick
            return PyActorGlobalClick.is_any_focused()
        except Exception:
            return False

    def _alive(self):
        """False once this instance's UObject is gone (e.g. the BP was
        recompiled during PIE and the component reinstanced). Its key
        bindings can still fire, so drop them instead of raising
        'PyUObject is in invalid state' on every key press."""
        try:
            if self.uobject.is_valid() and self.actor.is_valid():
                return True
        except Exception:
            pass
        inp = getattr(self, "input", None)
        if inp is not None:
            try:
                inp.shutdown()
            except Exception:
                pass
            self.input = None
        return False

    def _pc(self):
        # The possessing controller, not "player 0 of whatever world".
        try:
            return self.actor.Controller or self.actor.get_player_controller()
        except Exception:
            return None

    def _on_alt_pressed(self):
        """Free-look camera (hold)"""
        if not self._alive():
            return
        if self._is_typing() or self.input.is_key_down("Ctrl"):
            return
        pc = self._pc()
        if pc is not None:
            self._freelook_rot = pc.GetControlRotation()
        # Orbit the camera only: the body must not turn with the mouse
        # while free-looking (restored on release).
        self._body_yaw = bool(self.actor.bUseControllerRotationYaw)
        self._set(self.actor, "bUseControllerRotationYaw", False)
        self._set_freelook_camera(True)

    def _on_alt_released(self):
        if not self._alive():
            return
        pc = self._pc()
        if pc is not None and self._freelook_rot is not None:
            pc.SetControlRotation(self._freelook_rot)
        self._freelook_rot = None
        body_yaw = getattr(self, "_body_yaw", None)
        if body_yaw is not None:
            self._set(self.actor, "bUseControllerRotationYaw", body_yaw)
            self._body_yaw = None
        self._set_freelook_camera(False)

    def _set_freelook_camera(self, on):
        """Swap to FollowCamera while Alt is held (no-op when FollowCamera
        is already the only view)."""
        if self._follow_cam is None or not self._normal_cams:
            return
        self._follow_cam.SetActive(on, False)
        for c in self._normal_cams:
            c.SetActive(not on, False)
        # UFUNCTION setters only (see _set): full body visible to the owner
        # in free look, headless hidden; restore the BP flags afterwards.
        for c, headless, owner_no_see in getattr(self, "_mesh_flags", ()):
            try:
                c.SetOwnerNoSee(headless if on else owner_no_see)
            except Exception as e:
                ue.log_warning(f"PyActorStickMan: SetOwnerNoSee({c.get_name()}): {e}")

    def _on_scroll_up(self):
        """Ctrl: grow / Alt: camera closer / Shift: faster"""
        if not self._alive() or self._is_typing():
            return
        if self.input.is_key_down("Ctrl"):
            new = max(0.0, self.size_selector.increase_value(self._target_scale.x))
            self._target_scale = FVector(new, new, new)
        elif self.input.is_key_down("LeftAlt"):
            if self._target_arm_length is not None:
                self._target_arm_length = max(0.0, self.arm_selector.decrease_value(self._target_arm_length))
                ue.log(f"PyActorStickMan: camera distance -> {self._target_arm_length:.0f}")
        elif self.input.is_key_down("Shift"):
            self._scale_speed(self.speed_selector.increase_value)

    def _on_scroll_down(self):
        """Ctrl: shrink / Alt: camera farther / Shift: slower"""
        if not self._alive() or self._is_typing():
            return
        if self.input.is_key_down("Ctrl"):
            new = max(0.0, self.size_selector.decrease_value(self._target_scale.x))
            self._target_scale = FVector(new, new, new)
        elif self.input.is_key_down("LeftAlt"):
            if self._target_arm_length is not None:
                self._target_arm_length = max(0.0, self.arm_selector.increase_value(self._target_arm_length))
                ue.log(f"PyActorStickMan: camera distance -> {self._target_arm_length:.0f}")
        elif self.input.is_key_down("Shift"):
            self._scale_speed(self.speed_selector.decrease_value)

    def _scale_speed(self, fn):
        """Scale walk speed AND acceleration/braking by the same factor.
        Raising MaxWalkSpeed alone does nothing visible: with the default
        MaxAcceleration (2048 cm/s^2) the character takes seconds to reach
        even 10000 cm/s, so the speed looked capped."""
        if self._move is None:
            return
        old = self._move.MaxWalkSpeed
        new = max(0.0, fn(old))
        if old <= 0.0 or new <= 0.0:
            return   # can't scale out of zero
        k = new / old
        self._set(self._move, "MaxWalkSpeed", new)
        self._set(self._move, "MaxAcceleration", self._move.MaxAcceleration * k)
        self._set(self._move, "BrakingDecelerationWalking",
                  self._move.BrakingDecelerationWalking * k)
        ue.log(f"PyActorStickMan: walk speed -> {new:.0f} "
               f"(accel {self._move.MaxAcceleration:.0f})")

    def tick(self, dt):
        if getattr(self, "actor", None) is None:
            return   # _setup_input not run yet
        a = min(1.0, self.LERP_SPEED * dt)
        cur = self.actor.get_actor_scale()
        tgt = self._target_scale
        if abs(tgt.x - cur.x) > 1e-4:
            self.actor.set_actor_scale(FVector(
                cur.x + (tgt.x - cur.x) * a,
                cur.y + (tgt.y - cur.y) * a,
                cur.z + (tgt.z - cur.z) * a))
        if self._boom is not None and self._target_arm_length is not None:
            cur_len = self._boom.TargetArmLength
            if abs(self._target_arm_length - cur_len) > 0.01:
                self._set(self._boom, "TargetArmLength",
                          cur_len + (self._target_arm_length - cur_len) * a)

    def set_hidden(self, hidden):
        """Called by Main.toggle_pawn. The crosshair is a separate actor
        attached to Screen, so hiding the stickman doesn't hide it."""
        if getattr(self, "crosshair_comp", None) is not None:
            try:
                self.crosshair_comp.SetActorHiddenInGame(hidden)
            except Exception:
                pass

    def end_play(self, reason):
        if getattr(self, "input", None):
            self.input.shutdown()
        # The crosshair is a separate actor attached to Screen; attached
        # actors outlive their parent, so destroy it with the stickman.
        if getattr(self, "crosshair_comp", None) is not None:
            try:
                self.crosshair_comp.actor_destroy()
            except Exception:
                pass
            self.crosshair_comp = None

    def set_crosshair(self, path):
        """Swap the crosshair image at runtime."""
        self.crosshair_path = path
        if self.crosshair_comp is not None:
            try:
                self.crosshair_comp.DestroyComponent()
            except Exception:
                pass
            self.crosshair_comp = None
        self.begin_play()
