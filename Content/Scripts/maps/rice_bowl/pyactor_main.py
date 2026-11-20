"""
pyactor_main.py — rice_bowl map controller (RiceMap level).

Port of an old Ursina "orbiting rings" sketch:

    * a bowl (bolDeRiz) sits at the centre, in place of the black sphere
    * N_RINGS rings of N_PER_RING rice grains (rice_grain) orbit it,
      in place of the white cubes
    * inner rings orbit faster than outer rings
    * every grain also tumbles on all three axes, at its ring's speed

The bowl spawns at this PyActor's location, so move the BP_PyActorEmpty
to move the whole scene.

Ursina -> UE mapping
    1 Ursina unit       = UNIT UU
    Ursina +Z (forward) = UE +X
    Ursina +X (right)   = UE +Y
    Ursina +Y (up)      = UE +Z
    rotation_y          = yaw (both clockwise seen from above)

In the original, ring 0 had scale 0, so its cubes were invisible. That
ring is skipped here (rings run 1..N_RINGS-1).

Usage:
    Place a BP_PyActorEmpty in the level, set
        PythonModule = maps.rice_bowl.pyactor_main
        PythonClass  = Main
"""

import math
import os
import unreal_engine as ue
from unreal_engine import FVector, FRotator, FTransform


BOWL_MESH  = '/Game/Maps/RiceMap/bolDeRiz.bolDeRiz'
GRAIN_MESH = '/Game/Maps/RiceMap/rice_grain.rice_grain'

# Size of one Ursina unit in Unreal units.
UNIT = 10000.0

# Each mesh is normalised so its longest side is 1 Ursina unit, which
# matches the Ursina sphere/cube. If the bounds can't be read, the
# *_FALLBACK_SCALE is used. The multipliers below are applied on top for
# tuning by eye.
BOWL_SIZE           = 1.0    # Ursina: sphere scale=1
GRAIN_SIZE_MULT     = 1.0    # Ursina: cube scale = .2 * ring
BOWL_FALLBACK_SCALE  = 100.0
GRAIN_FALLBACK_SCALE = 100.0

N_RINGS    = 5     # Ursina: range(5)
N_PER_RING = 10    # Ursina: n = 10

# Each grain gets a desktop icon on its material ('Texture' parameter). If
# there are fewer icons than grains, the icons repeat.
#
# The grain mesh has no UVs, so the material must make its own:
# M_RiceIcon (built by maps.rice_bowl.build_rice_material) projects the
# icon onto the grain's broad face. If it hasn't been built yet,
# M_Icon (spherical projection) is used instead.
ICON_FOLDER        = os.path.join(os.path.expanduser('~'), 'Desktop')
ICON_MATERIAL      = '/Game/Materials/M_RiceIcon.M_RiceIcon'
ICON_MATERIAL_FALLBACK = '/Game/Materials/M_Icon.M_Icon'
ICON_TEXTURE_PARAM = 'Texture'
# How the icon is laid on the grain (M_RiceIcon only):
#   'square' - undistorted square in the middle of the grain, ICON_COVER
#              of the grain's width
#   'fill'   - stretched over the grain's whole length and width
ICON_FIT           = 'square'
ICON_COVER         = 0.9
# What fills the icon's transparent background:
#   'dominant'      - the icon's main colour, so the whole grain is tinted
#                     (the icon's edge pixels are repeated outside the
#                     square, so they become this colour too)
#   (r, g, b)       - a fixed opaque colour
#   None            - keep transparency; M_RiceIcon shows rice colour
ICON_BACKGROUND    = 'dominant'

ORBIT_SPEED_MULT = 10.0   # Ursina: rotation_speed * time.dt * 10
SPIN_SPEED_MULT  = 20.0   # Ursina: rotation_speed * time.dt * 20

# Slow yaw spin for the bowl (not in the original). Degrees per second;
# negative spins the other way, 0 turns it off.
BOWL_SPIN_DEG_PER_SEC = 18.0


# BP_PyActor can fire BeginPlay twice when the editor reloads modules.
_begin_play_ran = False


def _ring_radius(ring):
    """Ursina: z=((z*z)+3)*.16"""
    return ((ring * ring) + 3) * 0.16


def _ring_speed(ring):
    """Ursina: pow(5 - ring_scale, 1.5)  (ring_scale == ring index)"""
    return math.pow(5 - ring, 1.5)


def _unit_scale(mesh, fallback):
    """Scale that makes *mesh*'s longest side exactly UNIT UU."""
    try:
        extent = mesh.GetBounds().BoxExtent       # half-size
        longest = 2.0 * max(extent.x, extent.y, extent.z)
        if longest > 0.0:
            return UNIT / longest
    except Exception as e:
        ue.log_warning(f'rice_bowl.Main: could not read bounds of '
                       f'{mesh.get_name()}: {e}')
    return fallback


def _dominant_color(rgba):
    """Main colour of an RGBA icon: the most common colour among its
    opaque pixels, favouring saturated colours over white/grey/black so
    e.g. a red badge with a white letter gives red."""
    import colorsys
    small = rgba.resize((32, 32))
    counts = {}
    for r, g, b, a in small.getdata():
        if a < 128:
            continue
        key = (r // 32, g // 32, b // 32)     # 8 levels per channel
        c = counts.setdefault(key, [0, 0, 0, 0])
        c[0] += 1; c[1] += r; c[2] += g; c[3] += b
    if not counts:
        return (235, 232, 214)                # nothing opaque: rice white

    def score(c):
        n, r, g, b = c
        _, s, v = colorsys.rgb_to_hsv(r / n / 255, g / n / 255, b / n / 255)
        return n * (0.2 + s) * (0.3 + v)

    n, r, g, b = max(counts.values(), key=score)
    return (r // n, g // n, b // n)


def _icon_projection(mesh):
    """M_RiceIcon params placing a square icon on *mesh*'s broad face.

    U runs along the longest local axis, V along the second longest.
    Both use the same scale (ICON_COVER of the grain's width) so the icon
    stays square; it is centred on the bounds origin.
    """
    try:
        b = mesh.GetBounds()
        ext = (b.BoxExtent.x, b.BoxExtent.y, b.BoxExtent.z)
        org = (b.Origin.x, b.Origin.y, b.Origin.z)
    except Exception as e:
        ue.log_warning(f'rice_bowl.Main: icon projection from bounds '
                       f'failed: {e}')
        return None
    order = sorted(range(3), key=lambda i: ext[i], reverse=True)
    long_ax, wide_ax = order[0], order[1]
    if ICON_FIT == 'fill':
        size_u, size_v = 2.0 * ext[long_ax], 2.0 * ext[wide_ax]
    else:
        size_u = size_v = 2.0 * ext[wide_ax] * ICON_COVER
    if size_u <= 0.0 or size_v <= 0.0:
        return None
    u = [0.0, 0.0, 0.0]
    v = [0.0, 0.0, 0.0]
    u[long_ax] = 1.0 / size_u
    v[wide_ax] = -1.0 / size_v  # texture V runs downwards
    return {
        'IconU': FVector(*u),
        'IconV': FVector(*v),
        'IconUOffset': 0.5 - org[long_ax] * u[long_ax],
        'IconVOffset': 0.5 - org[wide_ax] * v[wide_ax],
    }


class Main:
    """PyActor for rice_bowl — spawns the bowl + grain rings, animates them."""

    def begin_play(self):
        global _begin_play_ran
        self.grains = []   # [actor, ring, slot, pitch, yaw, roll, scale]
        self.ring_yaw = [0.0] * N_RINGS
        self.bowl = None
        self.bowl_scale = 1.0
        self.bowl_yaw = 0.0

        if _begin_play_ran:
            ue.log('rice_bowl.Main.begin_play: already ran — skipping')
            return
        _begin_play_ran = True

        ue.log('rice_bowl.Main: begin_play')
        try:
            self._spawn_scene()
        except Exception as e:
            ue.log_warning(f'rice_bowl.Main: spawn failed: {e}')

    def end_play(self, reason):
        global _begin_play_ran
        _begin_play_ran = False
        ue.log('rice_bowl.Main: end_play')

    def _spawn_mesh(self, world, mesh, location, scale):
        from unreal_engine.classes import StaticMeshActor
        from unreal_engine.enums import EComponentMobility

        actor = world.actor_spawn(StaticMeshActor)
        smc = actor.StaticMeshComponent
        # Mobility must be Movable before SetStaticMesh (see ue_spawn).
        smc.Mobility = EComponentMobility.Movable
        smc.SetStaticMesh(mesh)
        actor.set_actor_transform(
            FTransform(location, FRotator(0, 0, 0),
                       FVector(scale, scale, scale)))
        return actor

    def _spawn_scene(self):
        from unreal_engine.classes import StaticMesh, Material

        world = self.uobject.get_world()
        self.center = self.uobject.get_actor_location()

        bowl_mesh = ue.load_object(StaticMesh, BOWL_MESH)
        grain_mesh = ue.load_object(StaticMesh, GRAIN_MESH)
        if bowl_mesh is None or grain_mesh is None:
            ue.log_warning('rice_bowl.Main: could not load bowl/grain mesh')
            return

        bowl_scale = _unit_scale(bowl_mesh, BOWL_FALLBACK_SCALE) * BOWL_SIZE
        grain_unit = _unit_scale(grain_mesh, GRAIN_FALLBACK_SCALE)

        self.bowl = self._spawn_mesh(world, bowl_mesh, self.center,
                                     bowl_scale)
        self.bowl_scale = bowl_scale

        icons = self._load_icons()
        icon_mat = None
        for mat_path in (ICON_MATERIAL, ICON_MATERIAL_FALLBACK):
            try:
                icon_mat = ue.load_object(Material, mat_path)
            except Exception:
                icon_mat = None
            if icon_mat is not None:
                ue.log(f'rice_bowl.Main: grain material {mat_path}')
                break
            ue.log_warning(f'rice_bowl.Main: material not found: {mat_path}'
                           + (' (run maps.rice_bowl.build_rice_material'
                              '.build() in the editor)'
                              if mat_path == ICON_MATERIAL else ''))
        # Projection params only matter for M_RiceIcon; other materials
        # ignore parameters they don't have.
        self.icon_params = _icon_projection(grain_mesh)
        textures = {}   # icon path -> texture, so repeats share one
        textured = 0

        # Ring 0 has scale 0 in the original -> nothing visible; skip it.
        for ring in range(1, N_RINGS):
            grain_scale = 0.2 * ring * grain_unit * GRAIN_SIZE_MULT
            for slot in range(N_PER_RING):
                actor = self._spawn_mesh(world, grain_mesh, self.center,
                                         grain_scale)
                if icons and icon_mat is not None:
                    path, pil_img = icons[len(self.grains) % len(icons)]
                    if self._apply_icon(actor, icon_mat, path, pil_img,
                                        textures):
                        textured += 1
                self.grains.append(
                    [actor, ring, slot, 0.0, 0.0, 0.0, grain_scale])

        self._update_grains()
        ue.log(f'rice_bowl.Main: spawned bowl + {len(self.grains)} grains '
               f'({textured} with icon materials)')

    def _load_icons(self):
        """[(path, PIL image), ...] for the icons in ICON_FOLDER."""
        from icon_to_image import get_folder_icons
        try:
            icons = list(get_folder_icons(ICON_FOLDER).items())
        except Exception as e:
            ue.log_warning(
                f'rice_bowl.Main: scan "{ICON_FOLDER}" failed: {e}')
            return []
        if not icons:
            ue.log_warning(f'rice_bowl.Main: no icons in "{ICON_FOLDER}"')
        return icons

    def _apply_icon(self, actor, icon_mat, path, pil_img, textures):
        """Give *actor* its own ICON_MATERIAL instance showing *pil_img*."""
        from unreal_engine_tools import pil_image_to_texture
        try:
            tex = textures.get(path)
            if tex is None:
                if ICON_BACKGROUND is not None:
                    from PIL import Image
                    rgba = pil_img.convert('RGBA')
                    bg = (_dominant_color(rgba)
                          if ICON_BACKGROUND == 'dominant'
                          else tuple(ICON_BACKGROUND))
                    flat = Image.new('RGBA', rgba.size, bg + (255,))
                    flat.alpha_composite(rgba)
                    pil_img = flat
                tex = pil_image_to_texture(pil_img)
                textures[path] = tex
            smc = actor.StaticMeshComponent
            mid = smc.create_material_instance_dynamic(icon_mat)
            mid.set_material_texture_parameter(ICON_TEXTURE_PARAM, tex)
            for name, value in (self.icon_params or {}).items():
                if isinstance(value, FVector):
                    mid.set_material_vector_parameter(name, value)
                else:
                    mid.set_material_scalar_parameter(name, float(value))
            smc.set_material(0, mid)
            actor.source_path = path
            return True
        except Exception as e:
            ue.log_warning(
                f'rice_bowl.Main: icon material failed for "{path}": {e}')
            return False

    def tick(self, delta_time):
        if self.bowl is not None and BOWL_SPIN_DEG_PER_SEC:
            self.bowl_yaw = (self.bowl_yaw
                             + BOWL_SPIN_DEG_PER_SEC * delta_time) % 360.0
            s = self.bowl_scale
            try:
                self.bowl.set_actor_transform(
                    # UEPython FRotator order is (roll, pitch, yaw).
                    FTransform(self.center, FRotator(0, 0, self.bowl_yaw),
                               FVector(s, s, s)))
            except Exception as e:
                ue.log_warning(f'rice_bowl.Main: bowl spin failed: {e}')
                self.bowl = None   # stop retrying every frame

        if not self.grains:
            return

        for ring in range(1, N_RINGS):
            self.ring_yaw[ring] = (self.ring_yaw[ring]
                                   + _ring_speed(ring) * delta_time
                                   * ORBIT_SPEED_MULT) % 360.0

        for g in self.grains:
            spin = _ring_speed(g[1]) * delta_time * SPIN_SPEED_MULT
            g[3] = (g[3] + spin) % 360.0
            g[4] = (g[4] + spin) % 360.0
            g[5] = (g[5] + spin) % 360.0

        self._update_grains()

    def _update_grains(self):
        for actor, ring, slot, pitch, yaw, roll, scale in self.grains:
            # Ursina: pivot.rotation_y = i * 360//n, then the ring spins.
            orbit = self.ring_yaw[ring] + slot * (360 // N_PER_RING)
            a = math.radians(orbit)
            r = _ring_radius(ring) * UNIT
            loc = FVector(self.center.x + r * math.cos(a),
                          self.center.y + r * math.sin(a),
                          self.center.z)
            # The grain's spin is relative to its ring, so add the orbit
            # to yaw. UEPython FRotator order is (roll, pitch, yaw).
            rot = FRotator(roll, pitch, yaw + orbit)
            try:
                actor.set_actor_transform(
                    FTransform(loc, rot, FVector(scale, scale, scale)))
            except Exception as e:
                ue.log_warning(f'rice_bowl.Main: transform failed: {e}')
