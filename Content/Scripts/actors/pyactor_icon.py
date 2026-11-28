import os
import subprocess
import unreal_engine as ue
from unreal_engine import FVector
import icon_picker

# Python component: hover-shrink + clickable file-open for spawn_icon
#
# CRASH NOTE: do NOT call `smc.bind_event('OnClicked', ...)` — two-param
# sparse delegates crash UEP at UEPyModule.cpp:4502.
#
# HOVER/CLICK: resolved by icon_picker (screen-space with a pixel margin),
# NOT by UE's OnBeginCursorOver. See icon_picker.py for why the shared state
# can't live on this class (UEP reloads this module once per icon component).


def _open_with_default_app(path):
    """Open *path* with the OS's default handler, the same as a Windows
    Explorer double-click — the "open" verb for that file type."""
    try:
        if hasattr(os, 'startfile'):
            os.startfile(path)
        else:
            subprocess.Popen(
                ['cmd', '/c', 'start', '', path],
                shell=False,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
            )
        ue.log(f'IconSphere: opened "{path}"')
    except Exception as e:
        ue.log_warning(f'IconSphere: open failed for "{path}": {e}')


class IconSphere:
    """Hover-shrink + click-to-open for BP_Icon."""

    # Hovered icons shrink to (1 - HOVER_SHRINK) of their size. Relative,
    # so it reads the same on a scale-1 file icon and a scale-7 star.
    HOVER_SHRINK = 0.2
    LERP_SPEED = 8.0
    # Mesh radius at scale 1 (/Engine/BasicShapes/Sphere is 100 UU across).
    UNIT_RADIUS = 50.0

    def begin_play(self):
        self.uobject.enable_input()
        self.player_controller = self.uobject.get_player_controller()

        # Captured lazily on first tick: spawn_icon's set_actor_transform
        # runs AFTER world.actor_spawn() returns, so begin_play here would
        # see the BP default scale, not the caller's requested scale.
        self.base_scale = None
        self.target_scale = None
        self._hovered = False

        # Find the owner actor for source_path lookup
        self.owner_actor = None
        for getter in ('get_owner', 'get_actor'):
            try:
                self.owner_actor = getattr(self.uobject, getter)()
                if self.owner_actor is not None:
                    break
            except Exception:
                continue

        icon_picker.register(self)
        ue.log(f'IconSphere: ready  owner={self.name()}  '
               f'pc={self.player_controller is not None}')

    def end_play(self, reason):
        icon_picker.unregister(self)

    # Called by icon_picker

    def name(self):
        try:
            return self.owner_actor.get_name()
        except Exception:
            return '?'

    def pick_radius(self):
        """World radius from the BASE scale, so the hover-shrink never moves
        the pick area out from under the cursor."""
        bs = self.base_scale
        return self.UNIT_RADIUS * max(abs(bs.x), abs(bs.y), abs(bs.z))

    def set_hovered(self, hovered):
        if hovered == self._hovered or self.base_scale is None:
            return
        self._hovered = hovered
        if hovered:
            k = 1.0 - self.HOVER_SHRINK
            bs = self.base_scale
            self.target_scale = FVector(bs.x * k, bs.y * k, bs.z * k)
        else:
            self.target_scale = self.base_scale

    def on_click(self):
        path = self._get_source_path()
        if path:
            ue.log(f'IconSphere: CLICK → "{path}"')
            _open_with_default_app(path)
        else:
            ue.log('IconSphere: CLICK (no source_path)')

    def _get_source_path(self):
        """Read source_path lazily from the owner actor (set after spawn)."""
        if self.owner_actor is not None:
            p = getattr(self.owner_actor, 'source_path', None)
            if p:
                return p
        return getattr(self.uobject, 'source_path', None)

    # Tick

    def tick(self, dt):
        # First tick: capture the post-spawn actor scale as our base.
        if self.base_scale is None:
            self.base_scale = self.uobject.get_actor_scale()
            self.target_scale = self.base_scale
            return

        if self.player_controller is not None:
            icon_picker.maybe_run(self.player_controller, dt)

        # hover scale lerp
        cur = self.uobject.get_actor_scale()
        tgt = self.target_scale
        # Skip when already at target: re-setting scale every frame on a
        # physics-simulating sphere rebuilds its collision shape, which
        # makes touching balls depenetrate violently (get flung).
        if (abs(tgt.x - cur.x) < 1e-3 and abs(tgt.y - cur.y) < 1e-3
                and abs(tgt.z - cur.z) < 1e-3):
            return
        a = min(1.0, self.LERP_SPEED * dt)
        self.uobject.set_actor_scale(FVector(
            cur.x + (tgt.x - cur.x) * a,
            cur.y + (tgt.y - cur.y) * a,
            cur.z + (tgt.z - cur.z) * a,
        ))
