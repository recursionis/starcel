"""Shared screen-space picker for pyactor_icon.IconSphere.

Lives in its own module ON PURPOSE: UnrealEnginePython reloads a Python
component's module every time a component initialises (PythonComponent.cpp,
`PyImport_ReloadModule` under WITH_EDITOR). Any registry stored on the
IconSphere class is therefore split into one-class-per-icon. This module is
only ever imported, never reloaded by UEP, so its state is truly shared.

Why not UE's OnBeginCursorOver?
  It needs a pixel-exact hit on the sphere, so small/distant icons are hard
  to hover, and the hover-shrink pulls the sphere out from under the cursor
  at the edge (flicker).

What this does instead (once per frame, for all icons):
  1. Build the camera basis + tan(half-FOV) per axis from
     DeprojectScreenPositionToWorld.
  2. Project each icon centre to screen pixels, and a point on its rim to
     get its on-screen radius.
     NOTE: assumes a plain perspective image — r.Upscale.Panini.D must be 0,
     or the drawn image no longer matches this projection.
  3. Compare to the mouse in pixels: an icon is hit if the cursor is within
     its drawn radius + PICK_TOLERANCE_PX (STICKY_TOLERANCE_PX for the icon
     already hovered, measured from its unshrunk radius -> no flicker).
     Cursor inside several icons -> nearest to camera wins; otherwise the
     smallest pixel gap wins.
  4. LMB rising edge -> click the hovered icon (exactly one per click).
"""
import math
import time

import unreal_engine as ue
from click_helpers import is_mouse_down

PICK_TOLERANCE_PX = 6.0
STICKY_TOLERANCE_PX = 14.0
DEBUG_CLICKS = True

_registry = []
_hovered = None
_was_mouse_down = False
_last_pick_time = 0.0


# Registration

def register(icon):
    if icon not in _registry:
        _registry.append(icon)


def unregister(icon):
    global _hovered
    try:
        _registry.remove(icon)
    except ValueError:
        pass
    if _hovered is icon:
        _hovered = None


# Vector helpers (plain tuples; avoids relying on FVector operators)

def _v(x):
    return (float(x.x), float(x.y), float(x.z))


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _mul(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _normalize(a):
    n = math.sqrt(_dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n) if n > 1e-9 else a


# Camera / projection

class _View:
    """Camera basis for projecting world points to screen pixels."""

    def __init__(self, pc, vw, vh):
        cx, cy = vw * 0.5, vh * 0.5
        ok0, o, f = pc.DeprojectScreenPositionToWorld(cx, cy)
        ok1, _, dr = pc.DeprojectScreenPositionToWorld(vw, cy)   # right edge
        ok2, _, du = pc.DeprojectScreenPositionToWorld(cx, 0.0)  # top edge
        if not (ok0 and ok1 and ok2):
            raise RuntimeError('deproject failed')
        self.o = _v(o)
        self.f = _normalize(_v(f))
        dr, du = _v(dr), _v(du)
        self.r = _normalize(_sub(dr, _mul(self.f, _dot(dr, self.f))))
        self.u = _normalize(_sub(du, _mul(self.f, _dot(du, self.f))))
        self.tan_x = _dot(dr, self.r) / _dot(dr, self.f)
        self.tan_y = _dot(du, self.u) / _dot(du, self.f)
        self.cx, self.cy, self.hw, self.hh = cx, cy, vw * 0.5, vh * 0.5

    def project(self, p):
        """World point -> (screen x, screen y, depth), or None if behind."""
        v = _sub(p, self.o)
        z = _dot(v, self.f)
        if z <= 1e-3:
            return None
        x = _dot(v, self.r) / z   # tangent space (== ScreenPos * tanHalfFOV)
        y = _dot(v, self.u) / z
        return (self.cx + x / self.tan_x * self.hw,
                self.cy - y / self.tan_y * self.hh,
                z)


def _viewport_size(pc):
    try:
        w, h = ue.get_viewport_size()
        if w > 0 and h > 0:
            return float(w), float(h)
    except Exception:
        pass
    w, h = pc.GetViewportSize()
    return float(w), float(h)


# Per-frame entry point

def maybe_run(pc, dt):
    """Called from every IconSphere.tick; runs the picker once per frame."""
    global _last_pick_time
    now = time.perf_counter()
    if now - _last_pick_time < dt * 0.5:
        return
    _last_pick_time = now
    try:
        _run(pc)
    except Exception as e:
        ue.log_warning(f'icon_picker: {e}')


def _run(pc):
    global _hovered, _was_mouse_down
    hovered = None
    debug = None

    ok, mx, my = False, 0.0, 0.0
    try:
        ok, mx, my = pc.GetMousePosition()
    except Exception:
        pass
    try:
        if not pc.bShowMouseCursor:
            ok = False
    except Exception:
        pass

    if ok:
        view = _View(pc, *_viewport_size(pc))
        best_inside = None   # (depth, icon)
        best_near = None     # (gap_px, icon)
        ranked = []
        for icon in list(_registry):
            if icon.base_scale is None:
                continue
            try:
                c = _v(icon.uobject.get_actor_location())
            except Exception:
                unregister(icon)  # stale actor (e.g. previous PIE session)
                continue
            sc = view.project(c)
            if sc is None:
                continue  # behind the camera
            r = icon.pick_radius()
            rim = [view.project(_add(c, _mul(axis, r)))
                   for axis in (view.r, view.u)]
            r_px = max([math.hypot(p[0] - sc[0], p[1] - sc[1])
                        for p in rim if p is not None] or [0.0])
            gap = math.hypot(mx - sc[0], my - sc[1]) - r_px
            ranked.append((gap, icon, r_px))
            if gap <= 0.0:
                if best_inside is None or sc[2] < best_inside[0]:
                    best_inside = (sc[2], icon)
            else:
                allow = STICKY_TOLERANCE_PX if icon is _hovered \
                    else PICK_TOLERANCE_PX
                if gap <= allow and (best_near is None or gap < best_near[0]):
                    best_near = (gap, icon)
        if best_inside is not None:
            hovered = best_inside[1]
        elif best_near is not None:
            hovered = best_near[1]
        debug = (mx, my, view, ranked)

    if hovered is not _hovered:
        if _hovered is not None:
            _hovered.set_hovered(False)
        if hovered is not None:
            hovered.set_hovered(True)
        _hovered = hovered

    mouse_down = is_mouse_down(pc)
    if mouse_down and not _was_mouse_down:
        _log_click(hovered, debug)
        if hovered is not None:
            hovered.on_click()
    _was_mouse_down = mouse_down


def _log_click(hovered, debug):
    if not DEBUG_CLICKS:
        return
    if debug is None:
        ue.log('icon_picker click: cursor hidden or mouse position unavailable')
        return
    mx, my, view, ranked = debug
    top = sorted(ranked, key=lambda t: t[0])[:3]
    near = ', '.join(f'{i.name()} gap={g:.0f}px r={r:.0f}px'
                     for g, i, r in top)
    ue.log(f'icon_picker click: mouse=({mx:.0f},{my:.0f}) '
           f'icons={len(_registry)} '
           f'picked={hovered.name() if hovered else None} nearest=[{near}]')
