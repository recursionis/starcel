"""
graphs.py — live sysmon graphs in two flavours (F4 switches all of them).

    '3d'             MathPlotter lines: ue_math_plotter.create_plotter with
                     the 'wall_graph' orientation spawns the gridlines and a
                     pool of cylinder segments once; every update only
                     re-poses the pooled segments (no spawn/destroy), so a
                     4 Hz refresh stays cheap.
    '2d'  (default)  Screen Cube: the same series drawn with PIL onto a
                     textured cube, updated in place.

Graph(panel, u, v, w, h, series, ...) places a graph in panel pixel space.
Each series is (callable -> sequence of floats, sign): with symmetric=True,
sign -1 mirrors it below the centre line. y_range=None auto-scales from 0
to the largest visible value.
"""

import math

from unreal_engine import FVector

from maps.hacker_map import theme, ui
from maps.hacker_map.theme import S, U, rot

ALL = []
MODE = '2d'      # Screen Cube by default; F4 switches to 3D MathPlotter lines
UPDATE_INTERVAL = 0.25


def set_mode_all(mode):
    global MODE
    MODE = mode
    for g in ALL:
        g.set_mode(mode)


def toggle_all():
    set_mode_all('2d' if MODE == '3d' else '3d')
    return MODE


def clear_registry():
    del ALL[:]


class Graph:
    def __init__(self, panel, u, v, w, h, series, y_range=(0.0, 100.0),
                 symmetric=False, grid=(5, 4), npts=40, line_px=2.2):
        self.panel = panel
        self.u, self.v, self.w, self.h = u, v, w, h
        self.series = series
        self.y_range = y_range
        self.symmetric = symmetric
        self.grid = grid
        self.npts = npts
        self.line_px = line_px
        self.mode = None
        self._acc = 0.0
        self._3d_actors = []          # grid + segments (for show/hide)
        self._segments = []           # per series: [cylinder actors]
        self._screen = None
        self._build_3d()
        self._build_2d()
        ALL.append(self)
        self.set_mode(MODE)
        self.update(force=True)

    # building

    def _origin_world(self):
        """World point of the graph's bottom-left (flat build frame)."""
        return self.panel.at(self.u, self.v + self.h, depth=ui.Panel.DEPTH + 2.0 * U)

    def _build_3d(self):
        from ue_math_plotter import create_plotter
        W, H = self.w * S, self.h * S
        self.plotter = create_plotter(
            world=ui.get_world(), origin=self._origin_world(),
            x_range=(0.0, W), y_range=(0.0, H), z_range=(0.0, 1.0),
            units_per_uu=1.0, orientation='wall_graph')
        f = self.plotter.factory
        b = self.plotter.bounds
        gx, gy = self.grid
        r_grid = 0.35 * S
        for i in range(gx + 1):
            x = W * i / gx
            f.spawn_cylinder(b.to_uu(x, 0.0), b.to_uu(x, H), r_grid, theme.GREEN_DIM + (1.0,))
        for j in range(gy + 1):
            y = H * j / gy
            f.spawn_cylinder(b.to_uu(0.0, y), b.to_uu(W, y), r_grid, theme.GREEN_DIM + (1.0,))
        grid_actors = list(f._spawned)
        for a in grid_actors:
            theme.glow(a, theme.GLOW_SOFT, theme.GREEN_DIM)
        r = self.line_px * S * 0.5
        self._r = r
        for _ in self.series:
            segs = []
            for k in range(self.npts - 1):
                x0 = W * k / (self.npts - 1)
                x1 = W * (k + 1) / (self.npts - 1)
                a = f.spawn_cylinder(b.to_uu(x0, H / 2), b.to_uu(x1, H / 2), r,
                                     theme.GREEN + (1.0,))
                if a is not None:
                    theme.glow(a, theme.GLOW_LINE)
                    segs.append(a)
            self._segments.append(segs)
        for a in f._spawned:
            self.panel.add(a)
            self._3d_actors.append(a)
            try:
                a.SetActorEnableCollision(False)
            except Exception:
                pass

    def _build_2d(self):
        self._px_scale = 2
        self._screen = self.panel.screen(self._draw(), self.u, self.v, self.w, self.h,
                                         strength=theme.GLOW_LINE * 0.6,
                                         depth=ui.Panel.DEPTH + 1.0 * U)

    # data

    def _values(self):
        """Per series: list of npts values normalised to 0..1 of the height."""
        raw = []
        for fn, sign in self.series:
            try:
                vals = list(fn())[-self.npts:]
            except Exception:
                vals = []
            if len(vals) < self.npts:
                vals = [0.0] * (self.npts - len(vals)) + vals
            raw.append((vals, sign))
        if self.symmetric:
            top = max([abs(x) for vals, _ in raw for x in vals] + [1.0]) * 1.25
            out = []
            for vals, sign in raw:
                out.append([0.5 + 0.5 * sign * max(-1.0, min(1.0, x / top)) for x in vals])
            self.peak = top
            return out
        if self.y_range is None:
            # auto: 0 .. 125% of the largest value on screen (network bytes/s)
            top = max([x for vals, _ in raw for x in vals] + [1.0]) * 1.25
            self.peak = top
            lo, hi = 0.0, top
        else:
            lo, hi = self.y_range
        span = max(1e-6, hi - lo)
        return [[max(0.0, min(1.0, (x - lo) / span)) for x in vals] for vals, _ in raw]

    # update

    def tick(self, dt):
        self._acc += dt
        if self._acc >= UPDATE_INTERVAL:
            self._acc = 0.0
            self.update()

    def update(self, force=False):
        vals = self._values()
        if self.mode == '3d' or force:
            self._update_3d(vals)
        if self.mode == '2d' or force:
            self._screen.update(self._draw(vals))

    def _update_3d(self, vals):
        W, H = self.w * S, self.h * S
        base = ui.rel(self.u, self.v + self.h, depth=ui.Panel.DEPTH + 2.0 * U)
        for segs, ys in zip(self._segments, vals):
            n = len(ys)
            for k, a in enumerate(segs):
                if k + 1 >= n:
                    break
                x0, x1 = W * k / (n - 1), W * (k + 1) / (n - 1)
                y0, y1 = H * ys[k], H * ys[k + 1]
                dy, dz = x1 - x0, y1 - y0
                length = max(0.5 * U, math.hypot(dy, dz))
                elev = math.degrees(math.atan2(dz, dy))
                mid = FVector(base.x, base.y + (x0 + x1) / 2.0, base.z + (y0 + y1) / 2.0)
                ui.set_rel(a, mid, rot(pitch=elev - 90.0, yaw=90.0),
                           FVector(self._r / 50.0, self._r / 50.0, length / 100.0))

    def _draw(self, vals=None):
        from PIL import Image, ImageDraw
        k = self._px_scale
        W, H = int(self.w * k), int(self.h * k)
        img = Image.new('RGBA', (W, H), theme.PIL_CLEAR)
        d = ImageDraw.Draw(img)
        gx, gy = self.grid
        for i in range(gx + 1):
            x = min(W - 1, int(W * i / gx))
            d.line((x, 0, x, H), fill=theme.PIL_FAINT, width=1)
        for j in range(gy + 1):
            y = min(H - 1, int(H * j / gy))
            d.line((0, y, W, y), fill=theme.PIL_FAINT, width=1)
        if vals:
            for ys in vals:
                n = len(ys)
                pts = [(W * i / (n - 1), (H - 1) * (1.0 - y)) for i, y in enumerate(ys)]
                d.line(pts, fill=theme.PIL_GREEN, width=max(2, int(self.line_px * k)))
        return img

    # mode switching

    def set_mode(self, mode):
        self.mode = mode
        show3d = mode == '3d'
        for a in self._3d_actors:
            self.panel.suppress(a, not show3d)
        self.panel.suppress(self._screen.actor, show3d)
        self.update(force=False)
