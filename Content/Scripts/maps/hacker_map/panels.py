"""
panels.py — the SYSTEM, NETWORK and FILESYSTEM panels.

Positions are panel pixels measured from the reference video (see
layout.PANELS for each panel's rectangle). Every panel exposes:

    build_steps()   list of callables; the boot sequence runs one per tick
                    so building never stalls a frame for long
    update(data)    refresh from SysData (called when a snapshot arrives)
    tick(dt)        per-frame animation (graphs, globe spin)
"""

import datetime
import math
import os
import random

import unreal_engine as ue
from unreal_engine import FVector

from maps.hacker_map import theme, ui, graphs, layout
from maps.hacker_map.theme import S, U, rot
from maps.hacker_map.sysdata import human_bytes, fmt_uptime


def backdrop_image(w=8, h=8):
    """Solid black panel face (everything is black; only text and lines
    glow)."""
    from PIL import Image
    return Image.new('RGBA', (8, 8), (0, 0, 0, 255))


class BasePanel(ui.Panel):
    LEFT = 'PANEL'
    RIGHT = ''
    # how far behind the panel plane its black face sits (UU). Panels with
    # things set back in depth (globe, logo) push it back so it doesn't
    # hide them; it's scaled up to cover the same area on screen.
    BACKDROP_BACK = 0.0

    def __init__(self, key):
        super().__init__(key, layout.PANELS[key], self.LEFT, self.RIGHT)
        self.graphs = []

    def build_steps(self):
        return [self._build_base]

    def _build_base(self):
        self.backdrop_sc = self.backdrop()
        self.chrome()

    def backdrop(self):
        back = max(4.0 * U, self.BACKDROP_BACK)
        centre = self.at(self.w / 2.0, (self.h - 16) / 2.0, depth=0.0)
        p, k = layout.push_back(centre, back)
        # collidable: the mouse-wheel trace uses it to know which panel
        # the cursor is over
        sc = ui.ScreenCube(backdrop_image(), p, (self.w + 4) * S * k,
                           (self.h + 20) * S * k, strength=0.0, collision=True)
        self.add(sc.actor)
        return sc

    def tick(self, dt):
        for g in self.graphs:
            g.tick(dt)

    def update(self, data):
        pass


# Text3D (BP_Cell) at scale 1: glyph advance / row pitch used for fixed
# table column widths
CHAR_UU = 34.0
ROW_UU = 64.0
PROC_COLS = (7, 15, 8, 6)      # PID, NAME, CPU, MEM (characters)


# SYSTEM

class SystemPanel(BasePanel):
    LEFT, RIGHT = 'PANEL', 'SYSTEM'

    def build_steps(self):
        return [self._build_base, self._build_clock, self._build_cpu,
                self._build_memory, self._build_processes, self._build_clipboard]

    def _build_clock(self):
        self.clock = self.text('00:00:00', 40, 18, 44, theme.GLOW_TEXT * 1.4)
        self.bar(0, 76, self.w, 76, 0.8, theme.GLOW_SOFT)
        cols = [(8, 'YEAR'), (84, 'UPTIME'), (166, 'TYPE'), (230, 'POWER')]
        self.info = {}
        for u, label in cols:
            self.text(label, u, 88, 9, theme.GLOW_SOFT)
            self.info[label] = self.text('--', u, 104, 12)
        self.date = self.text('', 8, 122, 9, theme.GLOW_SOFT)
        self.bar(0, 146, self.w, 146, 0.8, theme.GLOW_SOFT)

    def _build_cpu(self):
        self.text('CPU USAGE', 4, 156, 12)
        self.cpu_name = self.text('', 112, 159, 7.5, theme.GLOW_SOFT)
        self.cpu_lbl = []
        for i, (lbl, v) in enumerate((('#1-2', 186), ('#3-4', 246))):
            self.text(lbl, 4, v, 11)
            self.cpu_lbl.append(self.text('Avg. 0%', 4, v + 17, 8, theme.GLOW_SOFT))
        self.graphs.append(graphs.Graph(self, 72, 180, 224, 46,
                                        [(lambda: self.data.cpu_a, 1)]))
        self.graphs.append(graphs.Graph(self, 72, 240, 224, 46,
                                        [(lambda: self.data.cpu_b, 1)]))
        self.temp = {}
        for u, label in ((8, 'TEMP'), (84, 'MIN'), (160, 'MAX'), (232, 'TASKS')):
            self.text(label, u, 300, 9, theme.GLOW_SOFT)
            self.temp[label] = self.text('--', u, 315, 10)
        self.bar(0, 338, self.w, 338, 0.8, theme.GLOW_SOFT)

    def _build_memory(self):
        self.text('MEMORY', 4, 348, 12)
        self.mem_lbl = self.text('USING 0 OUT OF 0 GiB', 132, 351, 7.5, theme.GLOW_SOFT)
        self.mem_grid = self.screen(self._mem_image(0.0), 4, 370, 292, 58,
                                    strength=theme.GLOW_LINE * 0.6)
        self.bar(0, 440, self.w, 440, 0.8, theme.GLOW_SOFT)

    def _mem_image(self, pct):
        from PIL import Image, ImageDraw
        cols, rows = 46, 8
        W, H = 292 * 2, 58 * 2
        img = Image.new('RGBA', (W, H), theme.PIL_CLEAR)
        d = ImageDraw.Draw(img)
        lit = int(cols * rows * pct / 100.0)
        rnd = random.Random(int(pct * 10))
        order = list(range(cols * rows))
        rnd.shuffle(order)
        on = set(order[:lit])
        cw, ch = W / cols, H / rows
        for i in range(cols * rows):
            cx = (i % cols) * cw + cw / 2
            cy = (i // cols) * ch + ch / 2
            r = 2.2 if i in on else 1.3
            d.ellipse((cx - r, cy - r, cx + r, cy + r),
                      fill=theme.PIL_GREEN if i in on else theme.PIL_FAINT)
        return img

    def _build_processes(self):
        self.text('TOP PROCESSES', 4, 450, 12)
        self.text('PID | NAME | CPU | MEM', 164, 453, 7.5, theme.GLOW_SOFT)
        from nd_table.ndtable import Table
        from nd_table.unreal_integration import UnrealTableRenderer
        rows = 5
        t = Table(shape=(4, rows))
        for r in range(rows):
            t[(0, r)] = '00000'
            t[(1, r)] = 'process-name'
            t[(2, r)] = '00.0%'
            t[(3, r)] = '0.0%'
        self.proc_renderer = UnrealTableRenderer(
            world=ui.get_world(), cell_spacing=60.0, orientation_preset='wall_table',
            text_mode='3d', enable_resize=False, auto_size=False,
            padding_y_pos=14.0, padding_y_neg=0.0, padding_z_pos=4.0, padding_z_neg=4.0)
        # Fixed column widths (in characters): measuring Text3D bounds right
        # after spawning gives ~0 (glyphs aren't built yet), which collapsed
        # the columns on top of each other.
        for c, chars in enumerate(PROC_COLS):
            self.proc_renderer.set_user_size(0, c, chars * CHAR_UU)
        for r in range(rows):
            self.proc_renderer.set_user_size(1, r, ROW_UU)
        self.proc_cells = ui.adopt_table(self, self.proc_renderer, t, 6, 472, 288, 104)

    def _build_clipboard(self):
        self.bar(0, 588, self.w, 588, 0.8, theme.GLOW_SOFT)
        self.text('CLIPBOARD ACCESS', 4, 598, 12)
        self.copy_btn = self.button('COPY', 14, 624, 124, 34, 12)
        self.paste_btn = self.button('PASTE', 162, 624, 124, 34, 12)

    def update(self, data):
        now = datetime.datetime.now()
        if hasattr(self, 'clock'):
            ui.set_text(self.clock, now.strftime('%H:%M:%S'))
            ui.set_text(self.info['YEAR'], now.strftime('%Y'))
            ui.set_text(self.info['UPTIME'], fmt_uptime(data.get('uptime_sec', default=0)))
            ui.set_text(self.info['TYPE'], (data.static.get('os') or 'WIN').split()[0].upper()[:7])
            b = data.get('battery')
            power = 'WIRED' if not b or b.get('plugged') else f"{int(b.get('pct', 0))}%"
            ui.set_text(self.info['POWER'], power)
            ui.set_text(self.date, now.strftime('%a %d %b').upper())
        if hasattr(self, 'cpu_lbl'):
            ui.set_text(self.cpu_name, (data.static.get('cpu_name') or '')[:30])
            ui.set_text(self.cpu_lbl[0], f'Avg. {data.cpu_a[-1]:.0f}%')
            ui.set_text(self.cpu_lbl[1], f'Avg. {data.cpu_b[-1]:.0f}%')
            temp = data.get('cpu_temp_c')
            ui.set_text(self.temp['TEMP'], f'{temp:.0f}C' if temp else 'N/A')
            ui.set_text(self.temp['MIN'], f'{data.cpu_min:.2f}GHz' if data.cpu_min else '--')
            ui.set_text(self.temp['MAX'], f'{data.cpu_max:.2f}GHz' if data.cpu_max else '--')
            ui.set_text(self.temp['TASKS'], str(data.get('tasks', default='--')))
        if hasattr(self, 'mem_grid'):
            m = data.get('mem', default={}) or {}
            used = (m.get('used') or 0) / 1024 ** 3
            total = (m.get('total') or 0) / 1024 ** 3
            ui.set_text(self.mem_lbl, f'USING {used:.1f} OUT OF {total:.1f} GiB')
            if data.version % 4 == 0:
                self.mem_grid.update(self._mem_image(m.get('pct', 0.0)))
        if hasattr(self, 'proc_cells') and data.version % 4 == 0:
            procs = data.get('processes', default=[]) or []
            for r in range(5):
                p = procs[r] if r < len(procs) else {}
                vals = (str(p.get('pid', '')), str(p.get('name', ''))[:PROC_COLS[1] - 1],
                        f"{p.get('cpu', 0):.1f}%" if p else '', f"{p.get('mem', 0):.1f}%" if p else '')
                for c, v in enumerate(vals):
                    ui.set_text(self.proc_cells.get((c, r)), v or ' ')


# NETWORK

class NetworkPanel(BasePanel):
    """NETWORK panel. The globe is filmed, not placed on the wall.

    spawn_earth puts the Cesium globe (exactly like test_spawn.test_earth:
    scale 1e-5, never moved or scaled afterwards) on a private stage far
    below the scene, with its own light and the green wire shell. A
    SceneCapture2D that sees only those actors renders it into a render
    target shown on a Screen Cube in the panel, which:
      * clips it to the panel's globe window,
      * lets the mouse wheel zoom (capture field of view),
      * spins it by orbiting the capture camera (Cesium never moves).
    """
    LEFT, RIGHT = 'PANEL', 'NETWORK'

    # globe window in panel px (u, v, w, h) — square, like the render target,
    # or the globe gets stretched
    VIEW = (8, 128, 284, 284)
    STAGE = FVector(0.0, 0.0, -2.0e6)          # far below anything visible
    GLOBE_R_UU = theme.EARTH_RADIUS_CM * theme.EARTH_SCALE   # ~6371
    RT_SIZE = 512
    FOV_DEFAULT = 55.0
    FOV_MIN, FOV_MAX = 4.0, 80.0
    LIGHT_LUX = 6.0                            # raise if the globe is too dark
    SPIN_DEG_PER_S = 9.0
    DRAG_DEG_PER_PX = 0.35         # click-and-drag orbit speed
    RESUME_SPIN_AFTER = 3.0        # s after a drag before auto-spin resumes
    CAPTURE_MATS = ('/Game/Materials/M_HackerGlowRT', '/Game/Materials/M_SkyBoxImage',
                    '/Game/Materials/M_TextureUnlit')

    def build_steps(self):
        return [self._build_base, self._build_status, self._build_globe,
                self._build_globe_shell, self._build_capture, self._build_traffic]

    def _build_status(self):
        self.text('NETWORK STATUS', 4, 6, 12)
        for u, label in ((8, 'STATE'), (84, 'IPv4'), (236, 'PING')):
            self.text(label, u, 32, 10, theme.GLOW_SOFT)
        self.state = self.text('--', 8, 48, 13)
        self.ip = self.text('--', 84, 48, 13)
        self.ping = self.text('--', 236, 48, 13)
        self.bar(0, 76, self.w, 76, 0.8, theme.GLOW_SOFT)
        self.text('WORLD VIEW', 4, 86, 12)
        self.text('GLOBAL NETWORK MAP', 168, 89, 7.5, theme.GLOW_SOFT)
        self.text('ENDPOINT LAT/LON', 4, 104, 8, theme.GLOW_SOFT)
        self.latlon = self.text('0.0000, 0.0000', 200, 104, 7.5, theme.GLOW_SOFT)

    # stage

    def _build_globe(self):
        from ue_spawn import spawn_earth
        c = self.STAGE
        s = theme.EARTH_SCALE
        self.earth = None
        self._recenter_tries = 0
        self.spin = 0.0
        self.pitch = 15.0             # orbit elevation (deg), drag up/down
        self._idle = 99.0             # seconds since the last drag
        self.fov = self.FOV_DEFAULT
        try:
            # identical to test_spawn.test_earth (preset changed so it's lit
            # daylight imagery you can actually see)
            self.earth = spawn_earth(location=c, preset='satellite', scale=FVector(s, s, s))
        except Exception as e:
            theme.warn(f'spawn_earth failed: {e}')
        if self.earth is not None:
            self._centre_on_actor(self.earth)
            for prop in ('EnableFrustumCulling', 'EnableFogCulling'):
                # the main camera never looks at the stage; without this
                # Cesium would cull every tile
                try:
                    setattr(self.earth, prop, False)
                except Exception:
                    pass
        self._spawn_light()

    def _spawn_light(self):
        """A directional light so the (lit) Cesium tiles aren't black. Our
        own materials are unlit, so it doesn't change the rest of the map."""
        self.light = None
        try:
            from unreal_engine.classes import DirectionalLight
            from unreal_engine.enums import EComponentMobility
            from unreal_engine import FLinearColor
            a = ui.get_world().actor_spawn(DirectionalLight, self.STAGE, rot(pitch=-25.0, yaw=25.0))
            comp = a.get_actor_component_by_type(ue.find_class('DirectionalLightComponent'))
            if comp is not None:
                try:
                    comp.SetMobility(EComponentMobility.Movable)
                except Exception:
                    pass
                comp.SetIntensity(self.LIGHT_LUX)
                try:
                    comp.SetLightColor(FLinearColor(0.75, 1.0, 0.8, 1.0))
                except Exception:
                    pass
            self.light = a
        except Exception as e:
            theme.warn(f'globe light: {e}')

    @staticmethod
    def _centre_on_actor(earth):
        """By default Cesium puts a point on the Earth's SURFACE (the
        georeference origin, Boulder CO) at the actor location. 'True
        origin' puts the Earth's CENTRE there. UpdateGeoreference isn't
        exposed to Python, so re-set the (unused) origin to trigger it."""
        try:
            geo = earth.ResolveGeoreference()
        except Exception:
            geo = getattr(earth, 'Georeference', None)
        if geo is None:
            theme.warn('globe: no CesiumGeoreference found; using measured re-centring')
            return
        try:
            geo.OriginPlacement = 0                       # EOriginPlacement::TrueOrigin
            geo.KeepWorldOriginNearCamera = False
            geo.InaccurateSetGeoreferenceOriginLongitudeLatitudeHeight(
                FVector(geo.OriginLongitude, geo.OriginLatitude, geo.OriginHeight))
            theme.log('globe: georeference set to true origin (centre at actor)')
        except Exception as e:
            theme.warn(f'globe: could not switch georeference to true origin ({e})')

    def _recenter_globe(self):
        """Safety net: once tiles load, slide the globe so its bounds are
        centred on the stage (translation only)."""
        if self.earth is None or self._recenter_tries > 8:
            return
        self._recenter_tries += 1
        try:
            origin, extent = self.earth.GetActorBounds()
        except Exception:
            return
        big = max(extent.x, extent.y, extent.z)
        if big <= 1.0:
            return
        c = self.STAGE
        delta = FVector(c.x - origin.x, c.y - origin.y, c.z - origin.z)
        if abs(delta.x) + abs(delta.y) + abs(delta.z) < big * 0.05:
            self._recenter_tries = 99
            theme.log(f'globe: radius {big:.0f} UU (expected {self.GLOBE_R_UU:.0f})')
            return
        loc = self.earth.get_actor_location()
        self.earth.set_actor_location(FVector(loc.x + delta.x, loc.y + delta.y, loc.z + delta.z))

    def _build_globe_shell(self):
        """Green wireframe lat/long shell + 'ping' spikes (MathPlotter lines)
        around the staged globe."""
        from ue_math_plotter import create_plotter
        c = self.STAGE
        R = self.GLOBE_R_UU * 1.04
        p = create_plotter(world=ui.get_world(), origin=c, units_per_uu=1.0)
        f = p.factory
        b = p.bounds
        r_line = R * 0.004
        seg = 36

        def sph(lat, lon, rad=R):
            la, lo = math.radians(lat), math.radians(lon)
            return b.to_uu(rad * math.cos(la) * math.cos(lo),
                           rad * math.cos(la) * math.sin(lo),
                           rad * math.sin(la))

        for lat in (-60, -30, 0, 30, 60):
            for k in range(seg):
                f.spawn_cylinder(sph(lat, 360 * k / seg), sph(lat, 360 * (k + 1) / seg),
                                 r_line, theme.GREEN_DIM + (1.0,))
        for lon in range(0, 180, 30):
            for k in range(seg):
                a0, a1 = 360 * k / seg, 360 * (k + 1) / seg
                f.spawn_cylinder(sph(a0, lon), sph(a1, lon), r_line, theme.GREEN_DIM + (1.0,))
        for a in list(f._spawned):
            theme.glow(a, theme.GLOW_SOFT, theme.GREEN_DIM)
        rnd = random.Random(7)
        for _ in range(7):
            lat, lon = rnd.uniform(-55, 65), rnd.uniform(0, 360)
            a = f.spawn_cylinder(sph(lat, lon, R * 0.98), sph(lat, lon, R * 1.25),
                                 r_line * 1.6, theme.GREEN + (1.0,))
            dot = f.spawn_sphere(sph(lat, lon, R * 1.25), r_line * 4, theme.GREEN + (1.0,))
            for x in (a, dot):
                if x is not None:
                    theme.glow(x, theme.GLOW_HOT)
        self.shell = list(f._spawned)
        for a in self.shell:
            try:
                a.SetActorEnableCollision(False)
            except Exception:
                pass

    # capture

    def _build_capture(self):
        """SceneCapture2D -> render target -> Screen Cube in the panel."""
        self.capture = None
        self.view = None
        try:
            from unreal_engine.classes import SceneCapture2D, KismetRenderingLibrary
            world = ui.get_world()
            rt = KismetRenderingLibrary.CreateRenderTarget2D(world, self.RT_SIZE, self.RT_SIZE)
            cap = world.actor_spawn(SceneCapture2D, self.STAGE, rot())
            comp = cap.get_actor_component_by_type(ue.find_class('SceneCaptureComponent2D'))
            comp.TextureTarget = rt
            comp.CaptureSource = 2              # SCS_FinalColorLDR
            comp.PrimitiveRenderMode = 2        # PRM_UseShowOnlyList
            comp.bCaptureEveryFrame = True
            comp.FOVAngle = self.fov
            show = [x for x in ([self.earth] + list(getattr(self, 'shell', []))) if x is not None]
            comp.ShowOnlyActors = show
            self.capture, self.capture_comp, self.rt = cap, comp, rt
            self._place_camera()
        except Exception as e:
            theme.warn(f'globe capture failed: {e}')
            return
        # the panel window: opaque unlit image of the render target
        u, v, w, h = self.VIEW
        c = self.at(u + w / 2.0, v + h / 2.0)
        self.view = ui.spawn_mesh(ui.CUBE, c, rot(yaw=90),
                                  FVector(w * S / 100.0, 0.01 * U, h * S / 100.0),
                                  collision=True)
        self._view_scale = FVector(w * S / 100.0, 0.01 * U, h * S / 100.0)
        mat, name = theme.load_material(self.CAPTURE_MATS)
        if mat is not None:
            smc = self.view.StaticMeshComponent
            mid = smc.create_material_instance_dynamic(mat)
            mid.set_material_texture_parameter('Texture', rt)
            try:
                mid.set_material_vector_parameter('Tint', FVector(0.55, 1.0, 0.65))
            except Exception:
                pass
            try:
                mid.set_material_scalar_parameter('Emissive Multiplier', 1.0)
            except Exception:
                pass
            smc.set_material(0, mid)
        self.add(self.view)
        # glowing frame around the window
        self.frame(u, v, w, h, 0.8, theme.GLOW_SOFT, theme.GREEN_DIM)

    def _place_camera(self):
        """Orbit the capture camera around the stage (the globe never moves)."""
        if self.capture is None:
            return
        dist = self.GLOBE_R_UU * 3.2
        a = math.radians(self.spin)
        p = math.radians(self.pitch)
        c = self.STAGE
        fwd = (math.cos(p) * math.cos(a), math.cos(p) * math.sin(a), math.sin(p))
        loc = FVector(c.x - dist * fwd[0], c.y - dist * fwd[1], c.z - dist * fwd[2])
        self.capture.set_actor_location(loc)
        self.capture.set_actor_rotation(rot(pitch=self.pitch, yaw=self.spin))
        try:
            self.capture_comp.FOVAngle = self.fov
        except Exception:
            pass

    def is_view(self, actor):
        v = getattr(self, 'view', None)
        if v is None or actor is None:
            return False
        if v is actor:
            return True
        try:
            return v.get_name() == actor.get_name()
        except Exception:
            return False

    def drag(self, dx_px, dy_px):
        """Click-and-drag on the globe: orbit around it (screen pixels).
        Smaller steps when zoomed in."""
        k = self.DRAG_DEG_PER_PX * (self.fov / self.FOV_DEFAULT)
        self.spin = (self.spin - dx_px * k) % 360.0
        self.pitch = max(-85.0, min(85.0, self.pitch + dy_px * k))
        self._idle = 0.0
        self._place_camera()

    def zoom(self, steps):
        """Mouse wheel over the globe: +1 = zoom in, -1 = zoom out."""
        self.fov = max(self.FOV_MIN, min(self.FOV_MAX, self.fov * (0.85 ** steps)))
        self._place_camera()

    def grow(self, k):
        """Boot animation: the globe window opens from a line."""
        if self.view is not None:
            s = self._view_scale
            ui.set_rel(self.view, scale=FVector(s.x, s.y, max(0.001, s.z * k)))

    def set_visible(self, visible):
        super().set_visible(visible)
        if getattr(self, 'capture_comp', None) is not None:
            try:
                self.capture_comp.bCaptureEveryFrame = bool(visible)
            except Exception:
                pass

    # traffic

    def _build_traffic(self):
        self.bar(0, 432, self.w, 432, 0.8, theme.GLOW_SOFT)
        self.text('NETWORK TRAFFIC', 4, 442, 12)
        self.text('UP / DOWN, MB/S', 196, 445, 7.5, theme.GLOW_SOFT)
        self.text('TOTAL', 4, 460, 9, theme.GLOW_SOFT)
        self.totals = self.text('0 OUT, 0 IN', 150, 461, 7.5, theme.GLOW_SOFT)
        self.peak = self.text('0', 270, 482, 7.5, theme.GLOW_SOFT)
        # up and down drawn over each other from the bottom (not mirrored)
        self.graphs.append(graphs.Graph(
            self, 4, 478, 292, 192,
            [(lambda: self._data.net_up, 1), (lambda: self._data.net_down, 1)],
            y_range=None, grid=(6, 6)))

    def tick(self, dt):
        super().tick(dt)
        if getattr(self, 'capture', None) is not None and self.revealed:
            self._idle += dt
            if self._idle > self.RESUME_SPIN_AFTER:
                self.spin = (self.spin + dt * self.SPIN_DEG_PER_S) % 360.0
                self._place_camera()
        if getattr(self, 'earth', None) is not None and self._recenter_tries <= 8:
            self._recenter_acc = getattr(self, '_recenter_acc', 0.0) + dt
            if self._recenter_acc > 1.0:
                self._recenter_acc = 0.0
                self._recenter_globe()

    def update(self, data):
        net = data.get('net', default={}) or {}
        if hasattr(self, 'state'):
            ui.set_text(self.state, 'ONLINE' if net.get('online') else 'OFFLINE')
            ui.set_text(self.ip, str(net.get('ip') or '--'))
            ping = net.get('ping_ms')
            ui.set_text(self.ping, f'{ping:.0f}ms' if ping else '--')
            ui.set_text(self.latlon, f'{37.7749 + math.sin(data.version * 0.1):.4f}, '
                                     f'{-122.4194 + math.cos(data.version * 0.07):.4f}')
        if hasattr(self, 'totals'):
            ui.set_text(self.totals, f"{human_bytes(net.get('sent'))} OUT, "
                                     f"{human_bytes(net.get('recv'))} IN")
            g = self.graphs[-1] if self.graphs else None
            if g is not None and hasattr(g, 'peak'):
                ui.set_text(self.peak, f'{g.peak / 1e6:.2f}')


# FILESYSTEM

class FilesystemPanel(BasePanel):
    LEFT, RIGHT = 'FILESYSTEM', ''

    def build_steps(self):
        return [self._build_base, self._build_explorer, self._build_disk]

    def _build_explorer(self):
        from ue_spawn import spawn_pyactor
        self.path_lbl = self.text(os.path.expanduser('~'), self.w - 260, -12, 7.5, theme.GLOW_SOFT)
        self.explorer = spawn_pyactor('maps.hacker_map.hacker_explorer', 'HackerFileExplorer',
                                      location=self.at(8, 6), name='HM_FileExplorer')
        proxy = None
        try:
            proxy = self.explorer.get_py_proxy()
        except Exception as e:
            theme.warn(f'explorer proxy: {e}')
        self.explorer_proxy = proxy
        if proxy is not None:
            proxy.panel = self
            # starts 40 px in so the icon column sits inside the panel box
            proxy.fit_rect = (40, 8, self.w - 56, self.h - 44)
            proxy.on_path = lambda p: ui.set_text(self.path_lbl, p[-40:])
            self.explorer.initial_path = os.path.expanduser('~')
            try:
                proxy._configure()
            except Exception as e:
                theme.warn(f'explorer configure failed: {e}')

    def _build_disk(self):
        self.disk_lbl = self.text('Mount C: used 0%', 4, self.h - 26, 9)
        self.disk_bar = self.screen(self._disk_image(0.0), 210, self.h - 24, self.w - 216, 12,
                                    strength=theme.GLOW_LINE * 0.6)

    def _disk_image(self, pct):
        from PIL import Image, ImageDraw
        W, H = 600, 24
        img = Image.new('RGBA', (W, H), theme.PIL_CLEAR)
        d = ImageDraw.Draw(img)
        d.rectangle((0, 6, W - 1, H - 7), fill=theme.PIL_FAINT)
        d.rectangle((0, 4, int((W - 1) * pct / 100.0), H - 5), fill=theme.PIL_GREEN)
        return img

    def update(self, data):
        disk = data.get('disk', default={}) or {}
        if hasattr(self, 'disk_lbl') and disk:
            pct = float(disk.get('pct', 0.0))
            ui.set_text(self.disk_lbl, f"Mount {disk.get('path', '')} used {pct:.0f}%")
            if data.version % 10 == 1:
                self.disk_bar.update(self._disk_image(pct))

    def click(self, actor):
        p = self.explorer_proxy
        if p is not None and hasattr(p, 'handle_click'):
            return p.handle_click(actor)
        return False
