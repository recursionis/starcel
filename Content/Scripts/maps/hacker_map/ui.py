"""
ui.py — building blocks for HackerMap panels.

A Panel is one root actor (an empty, movable StaticMeshActor) plus every
part attached to it. Parts are placed in *panel pixel space* (u right,
v down, both in reference-video pixels from the panel's top-left), using
the flat wall frame (panel root yaw 0, viewer looking +X), and attached with
KeepWorld rules. After that, layout.py only moves the ~5 roots and every
part follows — so the wall can curve or fold into a room.

Parts
    Panel.text(...)      glowing Text3D (BP_Cell) label
    Panel.bar(...)       thin glowing cube (borders, separators, the boot line)
    Panel.frame(...)     rectangle outline made of 4 bars
    Panel.screen(...)    ScreenCube: a PIL image on a flattened cube (2D UI)
    Panel.add(actor)     attach anything else (globe, logo, table cells)

Text3D faces -X and reads along +Y with the default rotation, which is
exactly the flat wall frame, so no text rotation is needed.
"""

import math
import random

import unreal_engine as ue
from unreal_engine import FVector, FTransform

from maps.hacker_map import theme
from maps.hacker_map.theme import S, U, rot

KEEP_RELATIVE, KEEP_WORLD, SNAP = 0, 1, 2


def get_world():
    from unreal_engine_tools import get_world as _gw
    return _gw()


def attach(child, parent, rule=KEEP_WORLD):
    """Attach actor *child* to actor *parent* keeping its world transform."""
    if child is None or parent is None:
        return
    try:
        child.attach_to_actor(parent, '', rule, rule, rule, False)
    except Exception:
        try:
            child.attach_to_actor(parent, '', rule, rule, rule)
        except Exception as e:
            theme.warn(f'attach failed: {e}')


def _movable(smc):
    from unreal_engine.enums import EComponentMobility
    try:
        smc.SetMobility(EComponentMobility.Movable)
    except Exception:
        try:
            smc.Mobility = EComponentMobility.Movable
        except Exception:
            pass


def spawn_empty(location, rotation=None, name=None):
    """Movable StaticMeshActor with no mesh — a cheap transform root."""
    from unreal_engine.classes import StaticMeshActor
    world = get_world()
    a = world.actor_spawn(StaticMeshActor, location, rotation or rot())
    _movable(a.StaticMeshComponent)
    try:
        a.SetActorEnableCollision(False)
    except Exception:
        pass
    if name:
        try:
            a.set_actor_label(name)
        except Exception:
            pass
    return a


_mesh_cache = {}


def load_mesh(path):
    m = _mesh_cache.get(path)
    if m is None:
        from unreal_engine.classes import StaticMesh
        m = ue.load_object(StaticMesh, path)
        _mesh_cache[path] = m
    return m


def spawn_mesh(path, location, rotation=None, scale=None, collision=False):
    from unreal_engine.classes import StaticMeshActor
    world = get_world()
    a = world.actor_spawn(StaticMeshActor, location, rotation or rot())
    smc = a.StaticMeshComponent
    _movable(smc)
    smc.SetStaticMesh(load_mesh(path))
    if scale is not None:
        a.set_actor_transform(FTransform(location, rotation or rot(), scale))
    if not collision:
        try:
            a.SetActorEnableCollision(False)
        except Exception:
            pass
    return a


CUBE = '/Engine/BasicShapes/Cube.Cube'
CYLINDER = '/Engine/BasicShapes/Cylinder.Cylinder'
SPHERE = '/Engine/BasicShapes/Sphere.Sphere'


def set_hidden(actor, hidden):
    try:
        actor.SetActorHiddenInGame(bool(hidden))
    except Exception:
        pass


def destroy(actor):
    if actor is None:
        return
    theme.forget(actor)
    try:
        actor.actor_destroy()
    except Exception:
        pass


def set_text(actor, text):
    """Set a BP_Cell's Text3D text only when it changed (rebuilds glyphs)."""
    if actor is None:
        return
    try:
        t3d = actor.get_actor_component('Text3DComponent')
        if t3d is not None and str(t3d.Text or '') != text:
            t3d.Text = text
            theme.apply_now(actor)      # new glyphs exist now: glow them
            theme.mark_dirty(actor)
    except Exception:
        pass


def opaque(img):
    """Flatten a PIL image onto opaque black.

    A Screen Cube is a thin cube; with transparent pixels (and a two-sided
    material) the cube's BACK face shows through, mirrored — which made the
    line graphs look chopped in half and mirrored. Everything on screen sits
    on black anyway, so just make every image opaque."""
    from PIL import Image
    img = img.convert('RGBA')
    bg = Image.new('RGBA', img.size, (0, 0, 0, 255))
    bg.alpha_composite(img)
    return bg


class ScreenCube:
    """A PIL image shown on a thin cube — the map's 2D UI element.

    Same construction as ue_spawn.spawn_image (width on local X, thin on
    local Y, yaw 90 so the face looks down -X at the viewer). update(img)
    rewrites the existing texture in place when the size is unchanged, so
    animating graphs/boot text doesn't allocate a texture every frame."""

    def __init__(self, img, center, w_uu, h_uu, strength=theme.GLOW_SOFT,
                 tint=(1.0, 1.0, 1.0), collision=False):
        from unreal_engine_tools import pil_image_to_texture
        img = opaque(img)
        self.strength = strength
        self.size = img.size
        self.tex = pil_image_to_texture(img)
        self.actor = spawn_mesh(CUBE, center, rot(yaw=90),
                                FVector(w_uu / 100.0, 0.01 * U, h_uu / 100.0),
                                collision=collision)
        self.mid = theme.tex_mid(self.actor.StaticMeshComponent, self.tex,
                                 strength, tint)

    def update(self, img):
        import numpy as np
        img = opaque(img)
        if img.size == self.size and self.tex is not None:
            try:
                self.tex.texture_set_data(np.array(img, dtype=np.uint8).tobytes())
                return
            except Exception:
                pass
        from unreal_engine_tools import pil_image_to_texture
        self.size = img.size
        self.tex = pil_image_to_texture(img)
        if self.mid is not None:
            try:
                self.mid.set_material_texture_parameter('Texture', self.tex)
            except Exception:
                pass

    def set_strength(self, strength):
        if self.mid is not None:
            try:
                self.mid.set_material_scalar_parameter('Emissive Multiplier',
                                                     float(strength) * theme.glow_scale())
            except Exception:
                pass


class Panel:
    """One panel of the wall: root actor + attached parts."""

    DEPTH = 6.0 * U   # parts sit this far in front of the panel plane

    def __init__(self, key, rect_px, title_left='', title_right=''):
        from maps.hacker_map import layout
        self.key = key
        self.x, self.y, self.w, self.h = rect_px
        self.origin = layout.flat_pivot(rect_px)          # top-left, flat wall
        self.root = spawn_empty(self.origin, rot(), name=f'HM_{key}')
        self.parts = []
        self.revealed = True
        self._flicker_seed = random.random() * 10.0
        self.title_left = title_left
        self.title_right = title_right

    # coordinates

    def at(self, u, v, depth=None):
        """Panel pixel (u, v) -> world location in the flat build frame."""
        d = self.DEPTH if depth is None else depth
        o = self.origin
        return FVector(o.x - d, o.y + u * S, o.z - v * S)

    # parts

    def add(self, actor, track=True):
        if actor is None:
            return None
        attach(actor, self.root)
        if track:
            self.parts.append(actor)
        return actor

    def track(self, actor):
        """Count *actor* as part of the panel (show/hide) without attaching
        it to the root (it is attached to a sub-pivot instead)."""
        if actor is not None:
            self.parts.append(actor)
        return actor

    # data binding

    def bind(self, data):
        self._data = data
        return self

    @property
    def data(self):
        return self._data

    def text(self, txt, u, v, size_px=12.0, strength=theme.GLOW_TEXT,
             color=theme.GREEN, depth=None):
        """Glowing Text3D whose glyph height is ~size_px video pixels."""
        from ue_spawn import spawn_text3d
        s = size_px * S / theme.TEXT_H
        a = spawn_text3d(str(txt), self.at(u, v, depth), rot(),
                         FVector(s, s, s), enable_collision=False,
                         generate_overlap_events=False)
        theme.glow_text(a, strength, color)
        return self.add(a)

    def button(self, txt, u, v, w_px, h_px, size_px=11.0):
        """Outlined text button (the video's COPY / PASTE). Returns the
        Text3D actor; collision stays on so clicks can hit it."""
        from ue_spawn import spawn_text3d
        self.frame(u, v, w_px, h_px, thick_px=1.0, strength=theme.GLOW_SOFT)
        s = size_px * S / theme.TEXT_H
        tw = len(txt) * size_px * 0.6
        a = spawn_text3d(txt, self.at(u + (w_px - tw) / 2.0, v + (h_px - size_px) / 2.0 - 1),
                         rot(), FVector(s, s, s), enable_collision=True)
        theme.glow_text(a, theme.GLOW_TEXT)
        return self.add(a)

    def bar(self, u0, v0, u1, v1, thick_px=1.2, strength=theme.GLOW_LINE,
            color=theme.GREEN, depth=None):
        """Straight glowing bar from (u0,v0) to (u1,v1); axis-aligned or not."""
        p0, p1 = self.at(u0, v0, depth), self.at(u1, v1, depth)
        t = max(0.6 * U, thick_px * S)
        center = FVector((p0.x + p1.x) / 2, (p0.y + p1.y) / 2, (p0.z + p1.z) / 2)
        elev, length = wall_elevation(u0, v0, u1, v1)
        # Cube: local X = length, local Y = depth (thin), local Z = thickness.
        a = spawn_mesh(CUBE, center, rot(pitch=elev, yaw=90),
                       FVector(max(length, t) / 100.0, 0.02 * U, t / 100.0))
        theme.glow(a, strength, color)
        return self.add(a)

    def frame(self, u, v, w, h, thick_px=1.0, strength=theme.GLOW_LINE,
              color=theme.GREEN):
        return [self.bar(u, v, u + w, v, thick_px, strength, color),
                self.bar(u, v + h, u + w, v + h, thick_px, strength, color),
                self.bar(u, v, u, v + h, thick_px, strength, color),
                self.bar(u + w, v, u + w, v + h, thick_px, strength, color)]

    def screen(self, img, u, v, w_px, h_px, strength=theme.GLOW_SOFT,
               depth=None, collision=False):
        c = self.at(u + w_px / 2.0, v + h_px / 2.0, depth)
        sc = ScreenCube(img, c, w_px * S, h_px * S, strength, collision=collision)
        self.add(sc.actor)
        return sc

    def chrome(self, header=True):
        """eDEX panel dressing: top rule with two tiny header labels."""
        if header:
            self.text(self.title_left, 2, -12, 7.5, theme.GLOW_SOFT)
            if self.title_right:
                self.text(self.title_right, self.w - len(self.title_right) * 7.5 * 0.62 - 2,
                          -12, 7.5, theme.GLOW_SOFT)
            self.bar(0, -2, self.w, -2, 1.0, theme.GLOW_SOFT)

    # visibility / reveal animation

    def suppress(self, actor, hidden):
        """Keep *actor* hidden regardless of the panel's visibility (used to
        swap graph backends, hide inactive pages, etc.)."""
        if actor is None:
            return
        if not hasattr(self, '_suppressed'):
            self._suppressed = set()
        if hidden:
            self._suppressed.add(id(actor))
        else:
            self._suppressed.discard(id(actor))
        set_hidden(actor, hidden or not self.revealed)

    def _is_suppressed(self, actor):
        return id(actor) in getattr(self, '_suppressed', ())

    def set_visible(self, visible):
        self.revealed = bool(visible)
        for a in self.parts:
            set_hidden(a, (not visible) or self._is_suppressed(a))

    def reveal(self, t):
        """t in [0,1]: flicker in like the video's panels (random parts pop
        on, then everything settles visible at t>=1)."""
        if t >= 1.0:
            if not self.revealed:
                self.set_visible(True)
            return
        if not self.parts:
            return
        self.revealed = False
        cut = t * t
        rnd = random.Random(int(self._flicker_seed * 1000))
        for a in self.parts:
            on = rnd.random() < cut or (t > 0.6 and random.random() < 0.5)
            set_hidden(a, (not on) or self._is_suppressed(a))

    def destroy(self):
        for a in self.parts:
            destroy(a)
        self.parts = []
        destroy(self.root)


def wall_elevation(u0, v0, u1, v1):
    """Direction of a segment drawn on the wall -> (pitch_deg, length_uu).

    FRotator applies yaw, then pitch about the new Y axis. With yaw 90 the
    local X axis points along +Y (the wall's right) and local Y points into
    the viewer (-X), so a pitch tilts local X within the wall plane:
    rot(pitch=elev, yaw=90) aims local X along the segment."""
    dy = (u1 - u0) * S
    dz = -(v1 - v0) * S
    if dy < 0 or (dy == 0 and dz < 0):
        dy, dz = -dy, -dz
    return math.degrees(math.atan2(dz, dy)), math.hypot(dy, dz)


def rel(u, v, depth=Panel.DEPTH):
    """Panel pixel (u, v) -> location relative to the panel root."""
    return FVector(-depth, u * S, -v * S)


def adopt_actors(panel, actors, src_origin, u, v, scale, depth=None):
    """Re-parent actors laid out in world axes around *src_origin* (e.g. by
    UnrealTableRenderer, which always lays out along world +Y / -Z) under a
    new pivot at panel pixel (u, v), uniformly scaled by *scale*. Their
    offsets from *src_origin* become pivot-relative, so the group follows
    the panel through every layout mode. Returns the pivot."""
    d = Panel.DEPTH if depth is None else depth
    pivot = spawn_empty(panel.at(u, v, d), rot(), f'HM_{panel.key}_pivot')
    panel.add(pivot)
    set_rel(pivot, rel(u, v, d), rot(), FVector(scale, scale, scale))
    for a in actors:
        if a is None:
            continue
        try:
            p = a.get_actor_location()
        except Exception:
            continue
        off = FVector(p.x - src_origin.x, p.y - src_origin.y, p.z - src_origin.z)
        attach(a, pivot)
        set_rel(a, off, rot(), FVector(1, 1, 1))
        panel.track(a)
    return pivot


def table_extent(renderer):
    """Natural (width, height) in UU of the last table the renderer drew."""
    w = sum(renderer.cell_width_per_row.values()) or renderer.base_cell_spacing
    h = sum(renderer.cell_height_per_column.values()) or renderer.base_cell_spacing
    return w, h


def adopt_table(panel, renderer, table, u, v, w_px, h_px, glow=True):
    """Render *table* (nd_table.Table) with *renderer* and fit it into the
    panel rectangle (u, v, w_px, h_px). Cells are Text3D (BP_Cell) made to
    glow green. Returns renderer.cell_actors ({(col, row): actor})."""
    src = panel.at(u, v)
    try:
        renderer.render_table(table, world_location=src, render_gridlines=False)
    except Exception as e:
        theme.warn(f'table render failed: {e}')
        return {}
    tw, th = table_extent(renderer)
    s = min(w_px * S / max(1.0, tw), h_px * S / max(1.0, th))
    cells = dict(renderer.cell_actors)
    if glow:
        for a in cells.values():
            theme.glow_text(a, theme.GLOW_TEXT)
            try:
                a.SetActorEnableCollision(False)
            except Exception:
                pass
    panel._last_pivot = adopt_actors(panel, list(cells.values()), src, u, v, s)
    panel._last_scale = s
    return cells


def set_rel(actor, location=None, rotation=None, scale=None):
    """Set an attached actor's transform relative to its parent."""
    try:
        if location is not None:
            actor.K2_SetActorRelativeLocation(location)
        if rotation is not None:
            actor.K2_SetActorRelativeRotation(rotation)
        if scale is not None:
            actor.SetActorRelativeScale3D(scale)
    except Exception:
        pass
