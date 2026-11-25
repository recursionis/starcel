"""
gizmo_edit_mode.py — "G" key gizmo editing mode

Toggle with G (bound in main.py). While on:
  * the mouse cursor is shown
  * LMB on any actor in the map attaches the translate/rotate/scale gizmo
    (gizmo.build_gizmo) to it
  * LMB on the gizmo handles / the selected actor drags as usual
    (pyactor_gizmo.GizmoController)
  * LMB on empty space deselects
Toggling off destroys the gizmo and restores the previous cursor state.

Usage (main.py):
    from gizmo_edit_mode import GizmoEditMode
    self.gizmo_mode = GizmoEditMode(self.uobject, self.input)
    self.input.bind_press("G", self.gizmo_mode.toggle)
"""

import time
import unreal_engine as ue
from unreal_engine.enums import ECollisionChannel, EComponentMobility

# Actor classes that should never be picked (world geometry / infrastructure).
_UNSELECTABLE_CLASSES = (
    'Landscape', 'LandscapeProxy', 'LandscapeStreamingProxy',
    'Brush', 'Volume', 'WorldSettings', 'SkyAtmosphere', 'SkyLight',
    'ExponentialHeightFog', 'PostProcessVolume',
)

# Ignore selection clicks this long after enabling — toggle_cursor fires a
# synthetic LMB at screen centre to grab viewport focus.
_ENABLE_GRACE_S = 0.2


def _log(msg):
    try:
        ue.log_warning(f"[GizmoEditMode] {msg}")
    except Exception:
        pass


class GizmoEditMode:
    def __init__(self, uobject, input_manager):
        self.uobject = uobject
        self.input = input_manager
        self.enabled = False
        self.target = None
        self._gizmo = None          # dict from gizmo.build_gizmo
        self._controller = None     # GizmoController py proxy
        self._controller_actor = None
        self._cursor_was_visible = False
        self._enabled_at = 0.0

        # Bound once; the handlers no-op while the mode is off.
        self.input.bind_press("LeftMouseButton", self._on_press)
        self.input.bind_release("LeftMouseButton", self._on_release)

    # toggle
    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def enable(self):
        if self.enabled:
            return
        self.enabled = True
        self._enabled_at = time.monotonic()
        self._cursor_was_visible = bool(getattr(self.input, '_cursor_visible', False))
        if not self._cursor_was_visible:
            self.input.toggle_cursor()  # same path as "M": shows cursor + focus click
        self._ensure_controller()
        _log("ON — click an actor to attach the gizmo (G to exit)")

    def disable(self):
        if not self.enabled:
            return
        self.enabled = False
        self.deselect()
        if not self._cursor_was_visible and getattr(self.input, '_cursor_visible', False):
            self.input.show_cursor(False)
        _log("OFF")

    # controller
    def _ensure_controller(self):
        if self._controller is not None:
            return
        try:
            from ue_spawn import spawn_pyactor
            self._controller_actor = spawn_pyactor(
                'actors.pyactor_gizmo', 'GizmoController', name='GizmoEditController')
            self._controller = self._controller_actor.get_py_proxy()
            self._controller.setup(
                uobject=self.uobject, input_manager=None, target=None,
                handles={}, piece_offsets={}, bind_input=False)
        except Exception as e:
            _log(f"could not spawn GizmoController: {e}")
            self._controller = None

    # selection
    def _pick_under_cursor(self):
        try:
            hit = self.uobject.get_hit_result_under_cursor(ECollisionChannel.ECC_Visibility)
        except Exception:
            return None
        return hit.actor if hit else None

    def _is_selectable(self, actor):
        if actor is None:
            return False
        try:
            cls = actor.get_class().get_name()
            if any(cls == c or cls.startswith(c) for c in _UNSELECTABLE_CLASSES):
                return False
        except Exception:
            pass
        try:  # never grab the player's own pawn
            pawn = self.uobject.get_player_controller().K2_GetPawn()
            if pawn is not None and actor == pawn:
                return False
        except Exception:
            pass
        return True

    def select(self, actor):
        from gizmo import build_gizmo, gizmo_size_for
        self.deselect()
        self._ensure_controller()

        # Static actors can't be moved at runtime — promote the root.
        try:
            root = actor.RootComponent
            if root is not None:
                root.SetMobility(EComponentMobility.Movable)
        except Exception as e:
            _log(f"SetMobility failed on {actor.get_name()}: {e}")

        self.target = actor
        self._gizmo = build_gizmo(actor, size=gizmo_size_for(actor))
        if self._controller is not None:
            self._controller.retarget(
                actor, self._gizmo['handles'],
                self._gizmo['piece_offsets'], self._gizmo['bbox_dynamic'])
        _log(f"selected {actor.get_name()}")

    def deselect(self):
        from gizmo import destroy_gizmo, forget_target
        if self._controller is not None:
            self._controller.retarget(None)
        if self._gizmo is not None:
            destroy_gizmo(self._gizmo)
            self._gizmo = None
        if self.target is not None:
            forget_target(self.target)
            self.target = None

    # input
    def _on_press(self):
        """Select / drag in gizmo mode"""
        if not self.enabled:
            return
        if time.monotonic() - self._enabled_at < _ENABLE_GRACE_S:
            return
        actor = self._pick_under_cursor()

        # Clicked the gizmo or the selected actor → let the controller drag.
        if self._controller is not None and self._controller.owns(actor):
            self._controller._press()
            return

        if self._is_selectable(actor):
            self.select(actor)
        else:
            self.deselect()

    def _on_release(self):
        if self.enabled and self._controller is not None:
            self._controller._release()
