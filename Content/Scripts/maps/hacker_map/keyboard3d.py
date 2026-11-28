"""
keyboard3d.py — the on-screen keyboard: keyboard image generator + 2D tables.

  backplate   input_devices.generate_keyboard_guide_image(...) renders the
              key caps (green palette, keyboard only, no legends) to a PNG,
              shown on a Screen Cube.
  legends     one nd_table row-table per keyboard row (shape (keys, 1)),
              column widths set with set_user_size from the same key widths
              the generator uses (_guide_layout_rows), so each legend lands
              on its key cap. Rendered by UnrealTableRenderer, glowing green.
  highlight   a hidden glowing slab per key; while a physical key is held
              (Win32 GetAsyncKeyState) its slab shows and its legend burns
              brighter — the video's live keyboard.
  usage       clicking a key lights it and shows what it does in Starcel
              (input_devices.collect_keyboard_guide_entries: every hotkey
              bound in Scripts/ plus the project's input mappings).

Layout: the Wooting Two HE (Keyboard().keyboard_wootingtwohe).
"""

import os

import unreal_engine as ue
from unreal_engine import FVector

from maps.hacker_map import theme, ui, layout
from maps.hacker_map.panels import BasePanel
from maps.hacker_map.theme import S, U, rot

LAYOUT = 'wootingtwohe'     # any saved Keyboard().keyboard_<name> layout


def keyboard_rows():
    from input_devices import Keyboard
    return [list(r) for r in getattr(Keyboard(), f'keyboard_{LAYOUT}')]


FACE = {
    'Esc': 'ESC', 'Backspace': 'BACK', 'Tab': 'TAB', 'Enter': 'ENTER', 'Caps': 'CAPS',
    'LeftShift': 'SHIFT', 'RightShift': 'SHIFT', 'LeftCtrl': 'CTRL', 'RightCtrl': 'CTRL',
    'Fn': 'FN', 'Space': ' ', 'RightAlt': 'ALT GR', 'Up': '^', 'Down': 'v',
    'Left': '<', 'Right': '>', 'LeftAlt': 'ALT', 'Win': 'WIN', 'Menu': 'MENU',
    'Delete': 'DEL', 'Del': 'DEL', 'Ins': 'INS', 'Home': 'HOME', 'End': 'END',
    'PgUp': 'PGUP', 'PgDn': 'PGDN', 'PrtSc': 'PRT', 'Pause': 'PAUS', 'ScrLk': 'SCRL',
    'Num': 'NUM',
    **{f'NumPad{w}': str(i) for i, w in enumerate(
        ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'])},
}

VK = {
    'Esc': 0x1B, 'Backspace': 0x08, 'Tab': 0x09, 'Enter': 0x0D, 'Caps': 0x14,
    'LeftShift': 0xA0, 'RightShift': 0xA1, 'LeftCtrl': 0xA2, 'RightCtrl': 0xA3,
    'RightAlt': 0xA5, 'Space': 0x20, 'Up': 0x26, 'Down': 0x28, 'Left': 0x25, 'Right': 0x27,
    '`': 0xC0, '-': 0xBD, '=': 0xBB, '[': 0xDB, ']': 0xDD, '\\': 0xDC, ';': 0xBA,
    "'": 0xDE, ',': 0xBC, '.': 0xBE, '/': 0xBF,
    'LeftAlt': 0xA4, 'Win': 0x5B, 'Menu': 0x5D, 'Delete': 0x2E, 'Del': 0x2E,
    'Ins': 0x2D, 'Home': 0x24, 'End': 0x23, 'PgUp': 0x21, 'PgDn': 0x22,
    'PrtSc': 0x2C, 'Pause': 0x13, 'ScrLk': 0x91, 'Num': 0x90,
    '*': 0x6A, '+': 0x6B,
    **{f'F{i}': 0x6F + i for i in range(1, 13)},
    **{f'NumPad{w}': 0x60 + i for i, w in enumerate(
        ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'])},
}

GREEN_KEYS = {
    'BG': (0, 0, 0, 0),
    'KEY': (0, 0, 0, 255),
    'ACCENT': (0, 0, 0, 255),
    'KEY_TEXT': theme.PIL_GREEN, 'WHITE': theme.PIL_HOT, 'DESC': theme.PIL_GREEN,
    'HEAD': theme.PIL_GREEN, 'MUTED': theme.PIL_DIM, 'CAP_TEXT': theme.PIL_GREEN,
}

UNIT_PX = 64          # backplate px per key unit
K = 100.0             # legend-table UU per key unit (before panel fit)


def _vk(legend):
    if legend in VK:
        return VK[legend]
    if len(legend) == 1 and legend.isalnum():
        return ord(legend.upper())
    return None


class KeyboardPanel(BasePanel):
    LEFT, RIGHT = '', ''

    def build_steps(self):
        return [self._build_base, self._build_backplate, self._build_legends,
                self._build_highlights]

    def _build_base(self):
        # plain black face (no chrome on the keyboard in the video)
        from maps.hacker_map.panels import backdrop_image
        self.screen(backdrop_image(), 0, 0, self.w, self.h, strength=0.0, depth=-4.0 * U,
                    collision=True)

    INFO_H = 30          # px reserved above the keys for the usage line

    def _layout(self):
        from input_devices import _guide_layout_rows
        self.src_rows = keyboard_rows()
        rows, units = _guide_layout_rows(self.src_rows)
        self.rows, self.units = rows, units
        # fit units x len(rows) into the panel under the info line, centred
        margin = 8
        avail_h = self.h - self.INFO_H - 2 * margin
        self.key_px = min((self.w - 2 * margin) / units, avail_h / len(rows))
        self.kb_w = self.key_px * units
        self.kb_h = self.key_px * len(rows)
        self.kb_u = (self.w - self.kb_w) / 2.0
        self.kb_v = self.INFO_H + margin + (avail_h - self.kb_h) / 2.0
        self.info = self.text('click a key to see what it does in Starcel',
                              self.kb_u, 6, 10, theme.GLOW_TEXT)
        self._usage = None
        self.last_usage = None

    def _build_backplate(self):
        self._layout()
        from PIL import Image
        img = None
        try:
            from input_devices import generate_keyboard_guide_image
            import tempfile
            out = os.path.join(tempfile.gettempdir(), 'starcel_hackermap_keyboard.png')
            path = generate_keyboard_guide_image(
                layout=self.src_rows, output_path=out, unit=UNIT_PX,
                colors=GREEN_KEYS, keyboard_only=True, draw_legends=False)
            img = self._outline_caps(Image.open(path).convert('RGBA'))
        except Exception as e:
            theme.warn(f'keyboard image generator failed ({e}); drawing plain caps')
        if img is None:
            img = self._fallback_plate()
        self.plate = self.screen(img, self.kb_u, self.kb_v, self.kb_w, self.kb_h,
                                 strength=theme.GLOW_LINE * 0.5)

    def _outline_caps(self, img):
        """Black caps with thin glowing green outlines, drawn over the
        generator's image using the same key widths, so they line up."""
        from PIL import ImageDraw
        sx = img.width / float(self.units * UNIT_PX)
        sy = img.height / float(len(self.rows) * UNIT_PX)
        d = ImageDraw.Draw(img)
        g = max(4, UNIT_PX // 11)
        for r, row in enumerate(self.rows):
            x = 0.0
            for legend, wu in row:
                w = wu * UNIT_PX
                box = ((x + g / 2) * sx, (r * UNIT_PX + g / 2) * sy,
                       (x + w - g / 2) * sx, ((r + 1) * UNIT_PX - g / 2) * sy)
                d.rounded_rectangle(box, max(4, UNIT_PX // 10), fill=(0, 0, 0, 255),
                                    outline=theme.PIL_DIM, width=2)
                x += w
        return img

    def _fallback_plate(self):
        from PIL import Image
        W, H = int(self.units * UNIT_PX), len(self.rows) * UNIT_PX
        return self._outline_caps(Image.new('RGBA', (W, H), theme.PIL_CLEAR))

    def _build_legends(self):
        """One nd_table per keyboard row, fitted onto the key caps."""
        from nd_table.ndtable import Table
        from nd_table.unreal_integration import UnrealTableRenderer
        self.keys = []      # (legend, vk, legend_actor, u, v, w_px)
        s = self.key_px * S / K
        for r, row in enumerate(self.rows):
            t = Table(shape=(len(row), 1))
            for c, (legend, wu) in enumerate(row):
                face = FACE.get(legend, legend.upper())
                t[(c, 0)] = face
            rend = UnrealTableRenderer(
                world=ui.get_world(), cell_spacing=K, orientation_preset='wall_table',
                text_mode='3d', enable_resize=False, auto_size=False,
                padding_y_pos=0.0, padding_y_neg=0.0, padding_z_pos=0.0, padding_z_neg=0.0)
            for c, (legend, wu) in enumerate(row):
                rend.set_user_size(0, c, wu * K)
            rend.set_user_size(1, 0, K)
            src = self.at(self.kb_u, self.kb_v + r * self.key_px)
            try:
                rend.render_table(t, world_location=src, render_gridlines=False)
            except Exception as e:
                theme.warn(f'keyboard row {r} render failed: {e}')
                continue
            cells = dict(rend.cell_actors)
            for a in cells.values():
                theme.glow_text(a, theme.GLOW_TEXT)
                try:
                    a.SetActorEnableCollision(False)
                except Exception:
                    pass
            ui.adopt_actors(self, list(cells.values()), src, self.kb_u,
                            self.kb_v + r * self.key_px, s, depth=ui.Panel.DEPTH + 2.0 * U)
            # legends: smaller than a key, nudged in from the cap's corner
            x_units = 0.0
            for c, (legend, wu) in enumerate(row):
                a = cells.get((c, 0))
                if a is not None:
                    ui.set_rel(a, FVector(0.0, x_units * K + K * 0.2, -K * 0.3),
                               rot(), FVector(0.42, 0.42, 0.42))
                u = self.kb_u + x_units * self.key_px
                v = self.kb_v + r * self.key_px
                self.keys.append((legend, _vk(legend), a, u, v, wu * self.key_px))
                x_units += wu

    def _build_highlights(self):
        """Per key: a dim filled slab + a bright outline, hidden until the
        key is pressed (physical keyboard) or clicked (mouse)."""
        self.slabs = {}          # vk -> [(parts, legend_actor)]
        self.by_actor = {}       # id(slab) -> (legend, vk)
        self._flash = {}         # vk -> seconds left (mouse clicks)
        pad = self.key_px * 0.06
        for legend, vk, a, u, v, w in self.keys:
            key_id = vk if vk is not None else f'legend:{legend}'
            c = self.at(u + w / 2.0, v + self.key_px / 2.0, depth=ui.Panel.DEPTH + 1.0 * U)
            slab = ui.spawn_mesh(ui.CUBE, c, rot(yaw=90),
                                 FVector((w - 2 * pad) * S / 100.0, 0.01 * U,
                                         (self.key_px - 2 * pad) * S / 100.0),
                                 collision=True)
            theme.glow(slab, theme.GLOW_SOFT, theme.GREEN_DIM)
            self.add(slab)
            parts = [slab] + self.frame(u + pad, v + pad, w - 2 * pad, self.key_px - 2 * pad,
                                        thick_px=1.6, strength=theme.GLOW_HOT,
                                        color=theme.GREEN_HOT)
            for x in parts:
                self.suppress(x, True)
            self.slabs.setdefault(key_id, []).append((parts, a))
            self.by_actor[id(slab)] = (legend, key_id)
        self._down = {}
        try:
            import ctypes
            self._user32 = ctypes.WinDLL('user32')
            self._user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
            self._user32.GetAsyncKeyState.restype = ctypes.c_short
        except Exception:
            self._user32 = None

    def _set_lit(self, key_id, lit):
        for parts, legend_actor in self.slabs.get(key_id, ()):
            for x in parts:
                self.suppress(x, not lit)
            if legend_actor is not None:
                if lit:
                    theme.set_glow(legend_actor, theme.GLOW_HOT, theme.GREEN_HOT)
                else:
                    theme.set_glow(legend_actor, theme.GLOW_TEXT, theme.GREEN)

    def click(self, actor):
        """Mouse click on a key: light it briefly and report the legend."""
        hit = self.by_actor.get(id(actor)) if actor is not None else None
        if hit is None:
            for parts_list in self.slabs.values():
                for parts, _ in parts_list:
                    if actor is not None and _same(parts[0], actor):
                        hit = self.by_actor.get(id(parts[0]))
        if hit is None:
            return None
        legend, key_id = hit
        self._flash[key_id] = 0.35
        self._set_lit(key_id, True)
        self._show_usage(legend)
        return legend

    # what a key does in Starcel

    def _usage_map(self):
        """UE key name -> ['Context: chord - description', ...]"""
        if self._usage is not None:
            return self._usage
        self._usage = {}
        try:
            from input_devices import Keyboard, collect_keyboard_guide_entries, _guide_canon
            kb = Keyboard()
            scripts = os.path.join(os.path.abspath(ue.get_content_dir()), 'Scripts')
            for e in collect_keyboard_guide_entries(scripts, kb):
                seq = e.get('sequence')
                for chord in e.get('chords', []):
                    keys = chord if seq else chord[-1:]
                    label = (' -> ' if seq else '+').join(str(t) for t in chord)
                    line = f"{e.get('context', '')}: {label} - {e.get('desc', '')}"
                    for tok in keys:
                        for k in _guide_canon(kb, tok):
                            lst = self._usage.setdefault(k, [])
                            if line not in lst:
                                lst.append(line)
        except Exception as ex:
            theme.warn(f'keyboard usage scan failed: {ex}')
        return self._usage

    def usages(self, legend):
        try:
            from input_devices import Keyboard, _guide_canon
            keys = _guide_canon(Keyboard(), legend) or ()
        except Exception:
            keys = ()
        m = self._usage_map()
        out = []
        for k in keys:
            for line in m.get(k, []):
                if line not in out:
                    out.append(line)
        return out

    def _show_usage(self, legend):
        face = FACE.get(legend, legend.upper()).strip() or legend
        uses = self.usages(legend)
        if uses:
            more = f'  (+{len(uses) - 1} more in the terminal)' if len(uses) > 1 else ''
            ui.set_text(self.info, f'{face}: {uses[0]}{more}'[:120])
        else:
            ui.set_text(self.info, f'{face}: not bound to anything in Starcel')
        self.last_usage = (face, uses)

    def tick(self, dt):
        super().tick(dt)
        if not getattr(self, 'slabs', None) or not self.revealed:
            return
        for key_id in list(self._flash):
            self._flash[key_id] -= dt
            if self._flash[key_id] <= 0:
                del self._flash[key_id]
                if not self._down.get(key_id):
                    self._set_lit(key_id, False)
        if self._user32 is None:
            return
        for key_id in self.slabs:
            if not isinstance(key_id, int):
                continue
            down = bool(self._user32.GetAsyncKeyState(key_id) & 0x8000)
            if down == self._down.get(key_id, False):
                continue
            self._down[key_id] = down
            if down or key_id not in self._flash:
                self._set_lit(key_id, down)


def _same(a, b):
    try:
        return a.get_name() == b.get_name()
    except Exception:
        return False
