"""
hacker_explorer.py — the project's FileExplorer, dressed for HackerMap.

Subclasses actors.pyactor_file_explorer.FileExplorer (same os.scandir
listing and nd_table Name/Size/Date/Type table) and changes only the look
and the plumbing:

  * a '..' row on top for going up a folder
  * green PIL folder/file glyphs on Screen Cubes instead of the BP_Icon
    spheres (the video's folder grid look)
  * every Text3D cell glows green
  * the table is re-parented under a pivot and scaled to fit the
    FILESYSTEM panel, so it follows the panel through layout changes
  * click a row's icon (or name) to enter that folder / open that file;
    re-rendering destroys the previous table instead of stacking

Spawned by panels.FilesystemPanel, which sets proxy.panel / fit_rect /
on_path and calls _configure() right away (no first-tick wait).
"""

import os

import unreal_engine as ue
from unreal_engine import FVector

from actors.pyactor_file_explorer import FileExplorer
from maps.hacker_map import theme, ui
from maps.hacker_map.theme import S

_icon_cache = {}


def _icon_image(kind):
    """64x64 green folder / file glyph."""
    img = _icon_cache.get(kind)
    if img is not None:
        return img
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (64, 64), theme.PIL_CLEAR)
    d = ImageDraw.Draw(img)
    g, dim = theme.PIL_GREEN, theme.PIL_DIM
    if kind == 'folder':
        d.rectangle((6, 14, 28, 22), fill=dim)
        d.rectangle((6, 20, 58, 52), fill=g)
        d.rectangle((6, 20, 58, 24), fill=theme.PIL_HOT)
    elif kind == 'up':
        d.polygon([(32, 10), (54, 34), (40, 34), (40, 54), (24, 54), (24, 34), (10, 34)], fill=g)
    else:
        d.polygon([(14, 6), (40, 6), (52, 18), (52, 58), (14, 58)], outline=g, fill=None)
        d.line((14, 6, 40, 6, 52, 18, 52, 58, 14, 58, 14, 6), fill=g, width=3)
        d.line((40, 6, 40, 18, 52, 18), fill=g, width=3)
        for y in (28, 36, 44):
            d.line((20, y, 46, y), fill=dim, width=3)
    _icon_cache[kind] = img
    return img


class HackerFileExplorer(FileExplorer):
    MAX_FILES = 500          # listed (scroll through them with the wheel)
    ICON_COL_WIDTH = 60.0
    FONT_PX = 11.0           # glyph height on screen, reference-video px
    ICON_FILL = 0.2          # icon size vs. row height (was 0.8, then 0.4)

    def begin_play(self):
        super().begin_play()
        self.panel = None
        self.fit_rect = None
        self.on_path = None
        self._pivot = None
        self._row_targets = []      # (actor, full_path, is_folder)
        self._cells = []
        self._all = []
        self._up = None
        self.offset = 0

    def _configure(self):
        if self._configured:
            return
        self._configured = True
        self.current_folder = getattr(self.uobject, 'initial_path', None) or self.DEFAULT_FOLDER
        from nd_table.unreal_integration import UnrealTableRenderer
        self.renderer = UnrealTableRenderer(
            world=ui.get_world(), cell_spacing=90.0, orientation_preset='wall_table',
            text_mode='3d', enable_resize=False, auto_size=False,
            padding_y_pos=24.0, padding_y_neg=6.0, padding_z_pos=6.0, padding_z_neg=6.0)
        self.refresh()

    def tick(self, dt):
        if not self._configured:
            self._configure()

    # listing

    def _query_folder(self, folder):
        results = super()._query_folder(folder)
        width = self.COL_CHARS[0] - 1
        for item in results:          # display name only; full_path is kept
            n = item.get('name', '')
            if len(n) > width:
                item['name'] = n[:width - 2] + '..'
        return results

    def _parent_row(self, folder):
        parent = os.path.dirname(os.path.abspath(folder).rstrip('\\/'))
        if parent and os.path.abspath(parent) != os.path.abspath(folder):
            return {'name': '..', 'full_path': parent, 'size': 0,
                    'is_folder': True, 'is_up': True}
        return None

    # scrolling

    def _scale(self):
        return self.FONT_PX * S / theme.TEXT_H

    def visible_rows(self):
        """How many file rows fit the panel at FONT_PX."""
        from maps.hacker_map.panels import ROW_UU
        if self.panel is None or not self.fit_rect:
            return 9
        u, v, w, h = self.fit_rect
        return max(3, int(h * S / (ROW_UU * self._scale())) - 2)   # minus header + '..'

    def refresh(self):
        """Rescan the current folder and show it from the top."""
        self._all = self._query_folder(self.current_folder)
        self._up = self._parent_row(self.current_folder)
        self.offset = 0
        self._show()

    def scroll(self, steps):
        """Mouse wheel: +steps scrolls up, -steps scrolls down (3 rows each)."""
        n = self.visible_rows()
        top = max(0, len(self._all) - n)
        new = max(0, min(top, self.offset - steps * 3))
        if new != self.offset:
            self.offset = new
            self._show()

    def _show(self):
        n = self.visible_rows()
        rows = self._all[self.offset:self.offset + n]
        if self._up is not None:
            rows = [self._up] + rows
        self._render(rows)

    # rendering

    def _clear(self):
        dead = {id(a) for a in self._cells}
        dead |= {id(a) for a, _, _ in self._row_targets}
        if self.panel is not None and dead:
            self.panel.parts = [p for p in self.panel.parts if id(p) not in dead]
        for a in self._cells:
            ui.destroy(a)
        self._cells = []
        self._row_targets = []
        if self.renderer is not None:
            self.renderer.cell_actors = {}
            self.renderer.gridline_actors = []
            self.renderer.cell_width_per_row.clear()
            self.renderer.cell_height_per_column.clear()
            self.renderer.user_cell_width_per_row.clear()
            self.renderer.user_cell_height_per_column.clear()
        if self._pivot is not None and self.panel is not None:
            try:
                self.panel.parts.remove(self._pivot)
            except ValueError:
                pass
            ui.destroy(self._pivot)
        self._pivot = None

    # fixed column widths in characters (Name, Size, Date, Type); see
    # panels.CHAR_UU for why the table isn't auto-measured
    COL_CHARS = (22, 9, 11, 8)

    def _render(self, results):
        from maps.hacker_map.panels import CHAR_UU, ROW_UU
        self._clear()
        self._results = results
        for c, chars in enumerate(self.COL_CHARS):
            self.renderer.set_user_size(0, c + 1, chars * CHAR_UU)
        for r in range(len(results) + 1):
            self.renderer.set_user_size(1, r, ROW_UU)
        super()._render(results)      # table + _spawn_icon_column below
        if self.on_path:
            try:
                self.on_path(self.current_folder)
            except Exception:
                pass

    def _spawn_icon_column(self, results):
        """Green Screen Cube icons at each row's icon cell, then glow +
        fit the whole table into the panel."""
        r = self.renderer
        cells = dict(r.cell_actors)
        for a in cells.values():
            theme.glow_text(a, theme.GLOW_TEXT)
        src = self.location
        icons = []
        for ri, item in enumerate(results):
            cell = cells.get((self.ICON_COL, ri + 1))
            if cell is None:
                continue
            loc = cell.get_actor_location()
            row_h = r.get_effective_size(1, ri + 1)
            col_w = r.get_effective_size(0, self.ICON_COL)
            size = max(6.0, min(row_h, col_w) * self.ICON_FILL)
            kind = 'up' if item.get('is_up') else ('folder' if item.get('is_folder') else 'file')
            center = FVector(loc.x - 2.0, loc.y + col_w / 2.0, loc.z - row_h / 2.0)
            sc = ui.ScreenCube(_icon_image(kind), center, size, size,
                               strength=theme.GLOW_LINE * 0.5, collision=True)
            icons.append(sc.actor)
            self._row_targets.append((sc.actor, item.get('full_path'), item.get('is_folder')))
            name_cell = cells.get((1, ri + 1))
            if name_cell is not None:
                try:
                    name_cell.SetActorEnableCollision(True)
                except Exception:
                    pass
                self._row_targets.append((name_cell, item.get('full_path'), item.get('is_folder')))
        self._cells = list(cells.values())
        if self.panel is None:
            return
        u, v, w, h = self.fit_rect or (0, 0, self.panel.w, self.panel.h)
        tw, th = ui.table_extent(r)
        # fixed font size (not stretched to fill); only shrink if too wide
        s = min(self._scale(), w * S / max(1.0, tw))
        self._pivot = ui.adopt_actors(self.panel, self._cells + icons, src, u, v, s)
        self._cells += icons
        if not self.panel.revealed:
            for a in self._cells:
                ui.set_hidden(a, True)

    # clicks (routed from pyactor_main)

    def handle_click(self, actor):
        for a, path, is_folder in self._row_targets:
            if a is actor or (a is not None and actor is not None and _same(a, actor)):
                if is_folder:
                    self.current_folder = path
                    self.refresh()
                else:
                    try:
                        os.startfile(path)
                    except Exception as e:
                        ue.log_warning(f'HackerFileExplorer: open failed: {e}')
                return True
        return False

    def end_play(self, reason):
        self._clear()


def _same(a, b):
    try:
        return a.get_name() == b.get_name()
    except Exception:
        return False
