"""
theme.py — the HackerMap look: one green palette, glowing materials, fonts.

Everything visible in the map goes through these helpers so the whole scene
stays a single glowing green:

    glow(actor, strength)        StaticMesh actors (bars, cubes, logo, globe shell)
    glow_text(actor, strength)   Text3D actors (BP_Cell)
    tex_mid(smc, tex, strength)  textured "Screen Cube" faces (PIL images)

Materials: /Game/Materials/M_HackerGlow and M_HackerGlowTex are built once
in the editor by build_hacker_material.py. If they are missing, the helpers
fall back to M_Color / M_TextureUnlit (both have 'Emissive Multiplier'), so
the map still runs green, just lit instead of unlit.

Notes
  * FRotator's constructor order is (roll, pitch, yaw) — always use rot().
  * Shared MIDs are cached per (color, strength) so hundreds of bars and
    glyphs don't each create their own material instance.
"""

import os

import unreal_engine as ue
from unreal_engine import FVector, FRotator

# Palette

GREEN      = (0.12, 1.00, 0.42)     # main glow
GREEN_HOT  = (0.55, 1.00, 0.70)     # highlights (pressed keys, caret)
GREEN_DIM  = (0.03, 0.40, 0.16)     # gridlines, inactive
GREEN_DARK = (0.01, 0.08, 0.035)    # panel backgrounds

# 8-bit versions for PIL-rendered Screen Cubes (RGBA)
PIL_GREEN  = (60, 255, 130, 255)
PIL_HOT    = (190, 255, 210, 255)
PIL_DIM    = (25, 125, 65, 255)
PIL_FAINT  = (12, 60, 32, 255)
PIL_BG     = (3, 14, 8, 235)
PIL_CLEAR  = (0, 0, 0, 0)

# Presets (F6 cycles them at runtime)
#   'black'  default: black background, green glowing text and lines, the
#            star map dimmed to faint stars
#   'green'  the bright look: full-strength star sky washed green by bloom,
#            text glowing so hard it reads white
PRESETS = {
    'black': {'glow_scale': 0.5, 'sky_emissive': 0.06, 'level_post_process': False,
              'label': 'black background, green text'},
    'green': {'glow_scale': 1.0, 'sky_emissive': None, 'level_post_process': True,
              'label': 'green background, white text'},
}
PRESET = 'black'
_preset_listeners = []


def glow_scale():
    return PRESETS[PRESET]['glow_scale']


def on_preset(fn):
    """Register fn(preset_dict) to be called whenever the preset changes."""
    _preset_listeners.append(fn)


def set_preset(name):
    """Switch preset: rescales every glowing MID in place and notifies
    listeners (the sky)."""
    global PRESET
    if name not in PRESETS:
        return
    PRESET = name
    for rec in list(_glowing.values()):
        try:
            _set_params(rec[4], rec[2], rec[3])
        except Exception:
            pass
    for (color, strength), mid in list(_mid_cache.items()):
        _set_params(mid, strength, color)
    for mid, strength in list(_tex_mids):
        try:
            mid.set_material_scalar_parameter('Emissive Multiplier', float(strength) * glow_scale())
        except Exception:
            pass
    for fn in list(_preset_listeners):
        try:
            fn(PRESETS[name])
        except Exception as e:
            warn(f'preset listener: {e}')
    log(f"preset -> {name} ({PRESETS[name]['label']})")


def cycle_preset():
    names = list(PRESETS)
    set_preset(names[(names.index(PRESET) + 1) % len(names)])
    return PRESET


# Emissive strengths (base values; multiplied by the preset's glow_scale)
GLOW_TEXT   = 6.0
GLOW_LINE   = 10.0
GLOW_SOFT   = 3.0
GLOW_HOT    = 24.0

# Scale. The Cesium globe can't usefully go smaller than spawn_earth at
# EARTH_SCALE, so the whole wall is sized from it: the globe's radius in the
# NETWORK panel is GLOBE_R_PX reference-video pixels, which fixes how many
# Unreal units one video pixel is (S). Everything else is expressed in
# pixels (or in U, "UU at the original 2.5 UU/px scale"), so it all grows
# together and the camera simply sits further back.
EARTH_SCALE = 1e-5
EARTH_RADIUS_CM = 6.371e8
GLOBE_R_PX = 112.0
S = EARTH_RADIUS_CM * EARTH_SCALE / GLOBE_R_PX      # ~56.9 UU per video px
U = S / 2.5                                          # old-UU multiplier
# Text3D (BP_Cell) glyph height in UU at scale 1 (PyActorText3D.CHAR_HEIGHT)
TEXT_H = 50.0

GLOW_MATS = ('/Game/Materials/M_HackerGlow', '/Game/Materials/M_Color')
TEX_MATS = ('/Game/Materials/M_HackerGlowTex', '/Game/Materials/M_TextureUnlit',
            '/Game/Materials/M_TexturePicture')


def log(msg):
    ue.log(f'hacker_map: {msg}')


def warn(msg):
    ue.log_warning(f'hacker_map: {msg}')


def rot(pitch=0.0, yaw=0.0, roll=0.0):
    """FRotator with named args (the raw constructor is roll, pitch, yaw)."""
    return FRotator(roll, pitch, yaw)


# Materials

_mat_cache = {}


def load_material(paths):
    """First loadable material from *paths* -> (material, short_name)."""
    key = tuple(paths)
    if key in _mat_cache:
        return _mat_cache[key]
    from unreal_engine.classes import MaterialInterface
    for p in paths:
        name = p.split('/')[-1]
        for full in (f'{p}.{name}', p):
            try:
                m = ue.load_object(MaterialInterface, full)
            except Exception:
                m = None
            if m is not None:
                _mat_cache[key] = (m, name)
                return m, name
    _mat_cache[key] = (None, None)
    return None, None


_outer = None
_mid_cache = {}
_glowing = {}        # id(actor) -> [actor, kind, strength, color, mid, due_frames]
_tex_mids = []       # (mid, base strength) of Screen Cube faces
_frame = 0
_logged_mat = False


def set_outer(uobject):
    """Owner for material instances (the map controller actor)."""
    global _outer
    _outer = uobject
    _mid_cache.clear()


def reset():
    """Forget cached materials/MIDs (end_play) so a replay doesn't reuse
    objects from the previous world."""
    global _outer, _logged_mat
    _outer = None
    _mid_cache.clear()
    _mat_cache.clear()
    _glowing.clear()
    del _tex_mids[:]
    del _preset_listeners[:]
    _logged_mat = False
    global _mid_factory
    _mid_factory = None


def _glow_material():
    global _logged_mat
    mat, name = load_material(GLOW_MATS)
    if not _logged_mat:
        _logged_mat = True
        if mat is None:
            warn('no glow material found (run build_hacker_material.build())')
        else:
            log(f'glow material: {name}'
                + ('' if name == 'M_HackerGlow' else
                   '  (fallback - run build_hacker_material.build() for unlit glow)'))
    return mat


def _set_params(mid, strength, color):
    try:
        mid.set_material_vector_parameter('Color', FVector(*color[:3]))
    except Exception:
        pass
    try:
        mid.set_material_scalar_parameter('Emissive Multiplier', float(strength) * glow_scale())
    except Exception:
        pass


_mid_factory = None


def new_mid(mat):
    """Create a MaterialInstanceDynamic of *mat* without needing a mesh.

    MaterialInstanceDynamic.Create() does not work through UnrealEnginePython
    here (that is what left every Text3D that started out empty black), so:
      1. KismetMaterialLibrary.CreateDynamicMaterialInstance (engine API)
      2. a hidden helper StaticMeshActor's create_material_instance_dynamic
    """
    global _mid_factory
    try:
        from unreal_engine.classes import KismetMaterialLibrary
        mid = KismetMaterialLibrary.CreateDynamicMaterialInstance(_outer, mat)
        if mid is not None:
            return mid
    except Exception:
        pass
    try:
        if _mid_factory is None:
            from unreal_engine.classes import StaticMeshActor
            from unreal_engine_tools import get_world
            _mid_factory = get_world().actor_spawn(StaticMeshActor, FVector(0, 0, -1e6), FRotator(0, 0, 0))
            _mid_factory.SetActorHiddenInGame(True)
            _mid_factory.SetActorEnableCollision(False)
        return _mid_factory.StaticMeshComponent.create_material_instance_dynamic(mat)
    except Exception as e:
        warn(f'could not create a material instance: {e}')
        return None


def glow_mid(strength=GLOW_LINE, color=GREEN):
    """Shared emissive MID for (color, strength) — only for things that have
    no mesh component to create a MID from."""
    key = (tuple(round(c, 3) for c in color), round(float(strength), 2))
    mid = _mid_cache.get(key)
    if mid is not None:
        return mid
    mat = _glow_material()
    if mat is None:
        return None
    mid = new_mid(mat)
    if mid is None:
        return None
    _set_params(mid, strength, color)
    _mid_cache[key] = mid
    return mid


def _mesh_components(actor):
    """Every mesh component on *actor* (static meshes, BP cylinders and
    spheres, Text3D glyph meshes)."""
    out = []
    try:
        comps = actor.get_actor_components()
    except Exception:
        comps = []
    for c in comps or []:
        try:
            cname = c.get_class().get_name()
        except Exception:
            continue
        if 'MeshComponent' in cname and 'Skeletal' not in cname:
            out.append(c)
    if not out:
        try:
            smc = actor.StaticMeshComponent
            if smc is not None:
                out.append(smc)
        except Exception:
            pass
    return out


def _push(smc, mid):
    try:
        n = max(1, int(smc.GetNumMaterials()))
    except Exception:
        n = 4
    for i in range(n):
        try:
            smc.set_material(i, mid)
        except Exception:
            pass


def glow(actor, strength=GLOW_LINE, color=GREEN, all_components=True):
    """Make every mesh slot on *actor* glow *color* (one MID per actor,
    created from its own component — the same path apply_material uses)."""
    if actor is None:
        return None
    mat = _glow_material()
    if mat is None:
        return None
    comps = _mesh_components(actor) if all_components else [actor.StaticMeshComponent]
    mid = None
    for smc in comps:
        try:
            if mid is None:
                mid = smc.create_material_instance_dynamic(mat)
                _set_params(mid, strength, color)
            _push(smc, mid)
        except Exception as e:
            warn(f'glow on {actor.get_name()} failed: {e}')
    if mid is not None:
        _glowing[id(actor)] = [actor, 'mesh', strength, color, mid, []]
    return mid


_TEXT3D_PROPS = (('FrontMaterial', 0), ('BevelMaterial', 1),
                 ('ExtrudeMaterial', 2), ('BackMaterial', 3))


def glow_text(actor, strength=GLOW_TEXT, color=GREEN):
    """Green emissive on a BP_Cell's Text3D.

    Writes the Text3D material UPROPERTYs (so rebuilt glyphs pick it up) and
    pushes the MID onto every existing glyph mesh. Text3D (re)builds glyphs
    a frame or two after Text changes, so the actor is also queued for a
    re-push (see tick() / mark_dirty())."""
    if actor is None:
        return None
    rec = _glowing.get(id(actor))
    if rec is not None and rec[2] == strength and rec[3] == color and rec[4] is not None:
        mid = rec[4]
    else:
        mat = _glow_material()
        if mat is None:
            return None
        mid = new_mid(mat)
        if mid is None:
            for smc in _mesh_components(actor):
                try:
                    mid = smc.create_material_instance_dynamic(mat)
                    break
                except Exception:
                    continue
        if mid is None:
            warn(f'glow_text: no MID for {actor.get_name()}')
            return None
        _set_params(mid, strength, color)
    _apply_text(actor, mid)
    _glowing[id(actor)] = [actor, 'text', strength, color, mid, [_frame + 2, _frame + 15]]
    return mid


def _apply_text(actor, mid):
    try:
        t3d = actor.get_actor_component('Text3DComponent')
    except Exception:
        t3d = None
    if t3d is not None:
        # The Text3D setters store the material AND push it to the glyphs;
        # glyphs built later (text changes) read it back from there.
        for setter in ('SetFrontMaterial', 'SetBevelMaterial', 'SetExtrudeMaterial',
                       'SetBackMaterial'):
            try:
                getattr(t3d, setter)(mid)
            except Exception:
                pass
        for prop, slot in _TEXT3D_PROPS:
            try:
                setattr(t3d, prop, mid)
            except Exception:
                pass
        try:
            glyphs = list(t3d.CharacterMeshes or [])
        except Exception:
            glyphs = []
        for smc in glyphs:
            _push(smc, mid)
    for smc in _mesh_components(actor):
        _push(smc, mid)


def apply_now(actor):
    """Re-push an actor's glow immediately (Text3D rebuilds its glyphs
    synchronously when its text changes)."""
    rec = _glowing.get(id(actor)) if actor is not None else None
    if rec is None:
        return
    try:
        if rec[1] == 'text':
            _apply_text(actor, rec[4])
        else:
            for smc in _mesh_components(actor):
                _push(smc, rec[4])
    except Exception:
        pass


def mark_dirty(actor, frames=(2, 10)):
    """Text changed (or a Blueprint may have reset its materials): re-push
    the glow after the given numbers of frames."""
    rec = _glowing.get(id(actor)) if actor is not None else None
    if rec is not None:
        rec[5] = [_frame + f for f in frames]


SWEEP_PER_FRAME = 30
_sweep_i = 0


def tick():
    """Call once per frame: re-applies glow to Text3D actors whose glyphs
    were rebuilt (Text3D doesn't always carry the MID over), plus a slow
    round-robin sweep over every glowing Text3D so nothing stays unlit."""
    global _frame, _sweep_i
    _frame += 1
    recs = [r for r in _glowing.values() if r[1] == 'text']
    if recs:
        for k in range(min(SWEEP_PER_FRAME, len(recs))):
            r = recs[(_sweep_i + k) % len(recs)]
            try:
                _apply_text(r[0], r[4])
            except Exception:
                _glowing.pop(id(r[0]), None)
        _sweep_i = (_sweep_i + SWEEP_PER_FRAME) % max(1, len(recs))
    for rec in list(_glowing.values()):
        due = rec[5]
        if not due or due[0] > _frame:
            continue
        due.pop(0)
        actor, kind, mid = rec[0], rec[1], rec[4]
        try:
            if kind == 'text':
                _apply_text(actor, mid)
            else:
                for smc in _mesh_components(actor):
                    _push(smc, mid)
        except Exception:
            _glowing.pop(id(actor), None)


def set_glow(actor, strength, color=GREEN):
    """Change an already-glowing actor's brightness/colour in place (key
    highlights) without creating a new material instance."""
    rec = _glowing.get(id(actor)) if actor is not None else None
    if rec is None or rec[4] is None:
        return
    if rec[2] == strength and rec[3] == color:
        return
    rec[2], rec[3] = strength, color
    _set_params(rec[4], strength, color)


def forget(actor):
    _glowing.pop(id(actor), None)


def tex_mid(smc, texture, strength=GLOW_SOFT, tint=(1.0, 1.0, 1.0)):
    """Per-cube MID for a textured Screen Cube face."""
    mat, name = load_material(TEX_MATS)
    if mat is None:
        warn('no texture material for screen cubes')
        return None
    mid = smc.create_material_instance_dynamic(mat)
    try:
        mid.set_material_texture_parameter('Texture', texture)
    except Exception as e:
        warn(f'texture param failed: {e}')
    try:
        mid.set_material_scalar_parameter('Emissive Multiplier', float(strength) * glow_scale())
    except Exception:
        pass
    if strength > 0:
        _tex_mids.append((mid, strength))
    try:
        mid.set_material_vector_parameter('Tint', FVector(*tint))
    except Exception:
        pass
    smc.set_material(0, mid)
    return mid


# Fonts (PIL)

_font_cache = {}


def pil_font(size, bold=False):
    """Monospace PIL font: SourceCodePro Nerd Font from Content/Fonts, then
    Consolas, then PIL's default."""
    key = (int(size), bool(bold))
    if key in _font_cache:
        return _font_cache[key]
    from PIL import ImageFont
    names = []
    try:
        fonts = os.path.join(os.path.abspath(ue.get_content_dir()), 'Fonts')
        names.append(os.path.join(
            fonts, 'SourceCodeProNerdFontMono-Bold.ttf' if bold
            else 'SourceCodeProNerdFontMono-Regular.ttf'))
    except Exception:
        pass
    win = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')
    names += [os.path.join(win, 'consolab.ttf' if bold else 'consola.ttf'),
              os.path.join(win, 'lucon.ttf')]
    font = None
    for p in names:
        try:
            font = ImageFont.truetype(p, int(size))
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()
    _font_cache[key] = font
    return font
