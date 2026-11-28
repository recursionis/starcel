import unreal_engine as ue
from unreal_engine import FVector, FRotator, FTransform
from unreal_engine.enums import ECollisionChannel, EInputEvent
from unreal_engine_tools import find_component, get_world
from actors.pyactor_global_click import PyActorGlobalClick

# Python component: click + hover + typing for any actor with a Text3DComponent
#
# Per-instance behaviour (one PyActorText3D per actor):
#   - hover-scale animation
#   - tick-based cursor poll for click detection (Text3DComponent has no
#     OnClicked event; OnBeginCursorOver / OnEndCursorOver are tried first
#     and fall back to tick-based polling)
#   - logs the clicked character (column/row + flat index when
#     CharacterMeshes is available)
#
# Class-level "typing system" (one set of state for the whole scene,
# absorbed from the previous test_text3d_click closure-based prototype):
#   - tracks every PyActorText3D-bearing actor in the world via _watched
#     (begin_play auto-registers itself; external callers can also use
#     PyActorText3D.register_actor for non-PyActorText3D actors).
#   - owns the singleton PyActorCursor (insertion caret) and the highlight-
#     box pool used to render multi-line selections.
#   - drives a Win32 keyboard poll (GetAsyncKeyState + ToUnicode) so the
#     focused actor types like notepad: layout-correct characters, Shift
#     selection, Ctrl shortcuts (A/C/X/V/Tab, arrows, Home/End), and
#     Ctrl+V image paste via PIL ImageGrab.
#   - mouse polling is also Win32 (VK_LBUTTON) so callers don't have to
#     thread an input_manager / HotkeyManager through.
#   - mirrors focus to PyActorGlobalClick.set_focused_actor so other
#     systems (PyPawnDrone WASD, PyActorText3DExecutor) can read it.
#
# Bootstrap is lazy: the FIRST actor whose begin_play runs spawns the
# PyActorGlobalClick singleton, attaches the global tick, and initialises
# ctypes. Subsequent PyActorText3D.begin_plays just register themselves.
#
# Blueprint requirements:
#   - A Text3DComponent (any name; first one found is used)
#   - A Python component pointing to pyactor_text3d.PyActorText3D
#
# Project Settings -> Input:
#   - Enable Mouse Over Events = ON
#   - Enable Click Events      = ON
#
# Character coordinate system (default font size / wall_table orientation):
#   Y axis = character advance (left -> right), col = local_y / CHAR_WIDTH
#   Z axis = line descent      (up  ->  down),  row = -local_z / CHAR_HEIGHT
#
# Insertion cursor architecture
# ------------------------------
# A single PyActorCursor is spawned lazily on first use and shared across
# all Text3D actors in the scene (only one caret is ever visible).  This
# class owns it and exposes class methods for callers to position / show /
# hide it.  Sizing/placement tunables live here as class constants — see
# CURSOR_WIDTH_FRAC / CURSOR_VERTICAL_OFFSET_FRAC / CURSOR_DIACRITIC_HEADROOM_FRAC.

class PyActorText3D:
    """
    Hover + click + scene-global typing for a Text3DComponent-based actor.

    Click detection is tick-based (Text3DComponent has no OnClicked event).
    Hover detection tries component events first, falls back to tick polling.

    Class-level cursor singleton: see show_cursor_at / hide_cursor /
    compute_placement.  Class-level typing system: see register_actor /
    _ensure_global_typing / _global_tick.
    """

    HOVER_DELTA = 0.3
    LERP_SPEED = 8.0

    # Approximate UE units per character at the default Text3D font size (100).
    # Tune to match the actual font size in your Blueprint.
    CHAR_WIDTH = 50.0
    CHAR_HEIGHT = 50.0

    TEXT_COMPONENT_NAME = 'Text3DComponent'

    # Cursor visual tunables (used by compute_placement)
    # CURSOR_WIDTH_FRAC      — caret bar thickness as fraction of glyph width.
    # CURSOR_VERTICAL_OFFSET_FRAC — how far the caret is shifted DOWN from the
    #     bounds-vertical-center, expressed as a fraction of glyph height.
    #     1.0 drops the caret by one full row (corrects for Text3D bounds
    #     reporting the top of the line, not its center).
    # CURSOR_DIACRITIC_HEADROOM_FRAC — extra height added above the bounds top
    #     (fraction of tight bounds) so accents/^ aren't clipped.
    CURSOR_WIDTH_FRAC = 0.068
    CURSOR_VERTICAL_OFFSET_FRAC = .9
    CURSOR_DIACRITIC_HEADROOM_FRAC = 0.50
    CURSOR_HEIGHT_MULTIPLIER = 1.2

    # ---- Class-level typing-system state ----
    # Set of all actors participating in the typing system.  begin_play
    # auto-adds self.uobject; external code can call register_actor for
    # other actors (e.g. table cells without a PyActorText3D component).
    _watched = set()
    # Optional table renderer per actor for refit-on-unfocus.  Populated
    # only by callers that pass renderer= to register_actor.
    _watched_renderer = {}
    # Caret state (caret==anchor means no selection, anchor!=caret = range).
    _string_idx = 0
    _anchor = 0
    # Pool of translucent boxes used to render multi-segment selection
    # highlights — grown lazily, hidden between uses.
    _highlight_actors = []
    # Inline image actors pasted via Ctrl+V; tuples of
    # (host_actor, image_actor, placeholder_start, placeholder_len, w_uu, h_uu).
    _inline_images = []
    # Win32 ctypes handles + state, populated by _ensure_global_typing.
    _ctypes = None
    _user32 = None
    _kernel32 = None
    _WIN32_TYPING_OK = False
    # 256-byte rising-edge tracker for the keyboard poll.
    _prev_vk_down = bytearray(256)
    # Rising-edge tracker for the LMB poll (replaces input_manager).
    _prev_lbutton_down = False
    # Mouse selection state: actor being drag-selected (LMB held after a
    # click on it), per-line caret Z cached for the drag, the word range a
    # double-click-drag grows from, and double/triple-click tracking.
    _drag_actor = None
    _drag_rows = None
    _drag_word = None
    _click_count = 0
    _last_click_time = 0.0
    _last_click_actor = None
    # The PyActorGlobalClick singleton holding the global tick.
    _global_actor = None
    # _ensure_global_typing idempotency flag.
    _typing_initialized = False

    _CF_UNICODETEXT = 13   # standard Windows clipboard format ID

    # Lifecycle

    def begin_play(self):
        self.uobject.enable_input()
        self.player_controller = self.uobject.get_player_controller()
        self.player_controller.bEnableMouseOverEvents = True
        self.player_controller.bEnableClickEvents = True
        self.player_controller.CurrentClickTraceChannel = ECollisionChannel.ECC_WorldDynamic

        self.base_scale = self.uobject.get_actor_scale()
        self.target_scale = self.base_scale

        self._was_mouse_down = False
        self._hovered = False

        # Find Text3DComponent
        self.text3d = None
        try:
            self.text3d = find_component(self.uobject, self.TEXT_COMPONENT_NAME)
        except Exception:
            pass
        if self.text3d is None:
            ue.log_warning(
                f'PyActorText3D: could not find "{self.TEXT_COMPONENT_NAME}" '
                f'on {self.uobject.get_name()}')
            return

        # Try to bind cursor-over events (may work depending on UEP build)
        self._component_hover = False
        try:
            self.text3d.bind_event('OnBeginCursorOver', self._comp_hover_begin)
            self.text3d.bind_event('OnEndCursorOver',   self._comp_hover_end)
            self._component_hover = True
            ue.log(f'PyActorText3D: cursor-over events bound on {self.uobject.get_name()}')
        except Exception as e:
            ue.log(
                f'PyActorText3D: cursor-over bind failed ({e}), '
                'using tick-based hover detection')

        # OnClicked is NOT supported on Text3DComponent — tick-based only
        ue.log(
            f'PyActorText3D: click detection is tick-based '
            f'on {self.uobject.get_name()}')

        # Add self to the scene-wide typing system + bootstrap it.
        # register_actor is idempotent and _ensure_global_typing
        # short-circuits after the first caller.
        PyActorText3D.register_actor(self.uobject)
        PyActorText3D._ensure_global_typing()

    # ---------------- Cursor singleton (class-level) ----------------
    #
    # Single shared PyActorCursor for the whole scene — only one caret
    # ever exists.  Spawned lazily on first show_cursor_at() call.

    _cursor_pyactor = None

    @classmethod
    def _get_or_spawn_cursor(cls, world_provider):
        """Return the singleton PyActorCursor proxy, spawning if needed.
        ``world_provider`` is any actor (used only to fetch a UWorld)."""
        if cls._cursor_pyactor is not None:
            try:
                proxy = cls._cursor_pyactor.get_py_proxy()
                if proxy is not None:
                    return proxy
            except Exception:
                pass
            cls._cursor_pyactor = None  # stale handle — respawn

        try:
            from ue_spawn import spawn_pyactor
            cls._cursor_pyactor = spawn_pyactor(
                'actors.pyactor_cursor', 'PyActorCursor',
                components=[dict(class_name='StaticMeshComponent',
                                 name='Cube', root=True,
                                 mesh='/Engine/BasicShapes/Cube.Cube')],
                name='TextCursor')
        except Exception as e:
            ue.log_warning(f'PyActorText3D: cursor spawn failed: {e}')
            return None

        if cls._cursor_pyactor is None:
            return None
        try:
            return cls._cursor_pyactor.get_py_proxy()
        except Exception:
            return None

    @classmethod
    def show_cursor_at(cls, actor, target_glyph, string_idx=None, text=None):
        """Move the singleton cursor to ``target_glyph`` on ``actor``.
        Returns True on success.

        Pass ``string_idx`` + ``text`` (the caret's string position and the
        full text) for row-aware placement — without them the caret can't
        tell which line it's on and Enter won't move it down."""
        if actor is None:
            return False
        placement = cls.compute_placement(
            actor, target_glyph, string_idx=string_idx, text=text)
        if placement is None:
            return False
        proxy = cls._get_or_spawn_cursor(actor)
        if proxy is None:
            return False
        world_pt, scale_vec, rot = placement
        proxy.move_to(world_pt, scale_vec, rot)
        return True

    @classmethod
    def hide_cursor(cls):
        if cls._cursor_pyactor is None:
            return
        try:
            proxy = cls._cursor_pyactor.get_py_proxy()
        except Exception:
            return
        if proxy is not None:
            proxy.hide()

    @classmethod
    def compute_placement(cls, actor, target_glyph, string_idx=None, text=None):
        """Compute (world_pt, scale_vec, rotation) for the caret at the
        left edge of glyph ``target_glyph`` on ``actor``.  ``target_glyph``
        may equal the glyph count (cursor sits one width past the last
        glyph).  Returns None on failure.

        When ``string_idx`` + ``text`` are supplied, placement is row-aware:
        the caret lands on the text line implied by the newlines before
        ``string_idx`` (so Enter on the last line drops the caret to a fresh
        empty line instead of leaving it past the previous line's last
        glyph).  Without them the legacy glyph-only, whole-block geometry is
        used — the selection-highlight pool still relies on that path, so it
        lives here as the single source of truth for caret/highlight geometry.
        """
        if actor is None:
            return None
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return None
        if t3d is None:
            return None

        kernings = None
        try:
            kernings = t3d.CharacterKernings
        except Exception:
            pass
        meshes = None
        try:
            meshes = t3d.CharacterMeshes
        except Exception:
            pass

        if not kernings or len(kernings) == 0:
            return None

        glyph_h = cls.CHAR_HEIGHT
        glyph_w = cls.CHAR_WIDTH

        # Read glyph dimensions from the reference mesh (target, clamped).
        ref_idx = target_glyph
        if ref_idx >= len(kernings):
            ref_idx = len(kernings) - 1
        if ref_idx < 0:
            ref_idx = 0
        if (meshes is not None
                and 0 <= ref_idx < len(meshes)
                and meshes[ref_idx] is not None):
            try:
                _, e = meshes[ref_idx].GetComponentBounds()
                glyph_h = e.z * 2.0
                glyph_w = e.y * 2.0
            except Exception:
                pass

        row_aware = string_idx is not None and text is not None

        # Horizontal: caret X/Y relative to the actor.  Row-aware first so a
        # caret on an empty line lands at the left margin instead of one width
        # past the previous line's last glyph; otherwise legacy glyph-only
        # geometry (left edge of target glyph, or one width past the last).
        target_rel = None
        if row_aware:
            target_rel = cls._caret_target_rel(
                text, string_idx, kernings, meshes, glyph_w)
        if target_rel is None:
            if (0 <= target_glyph < len(kernings)
                    and kernings[target_glyph] is not None):
                try:
                    target_rel = kernings[target_glyph].get_relative_location()
                except Exception:
                    pass
            elif len(kernings) > 0 and kernings[-1] is not None:
                try:
                    r = kernings[-1].get_relative_location()
                    target_rel = FVector(r.x, r.y + glyph_w, r.z)
                except Exception:
                    pass
        if target_rel is None:
            return None

        actor_loc = actor.get_actor_location()
        actor_rot = actor.get_actor_rotation()

        # Vertical: place the caret on its own text line.  Row-aware when a
        # string index is known; otherwise the whole-block geometry (correct
        # for single-line text and what the highlight pool relies on).
        cursor_h = None
        cursor_z = None
        if row_aware:
            cursor_h, cursor_z = cls._caret_vertical_for_row(
                kernings, meshes, glyph_h, text, string_idx)
        # Whole-block geometry spans every line, so it's only valid for
        # single-line text; multi-line falls through to the caret line's
        # own kerning Z (target_rel.z, row-aware via _caret_ys).
        if cursor_h is None and not (row_aware and '\n' in text):
            cursor_h, cursor_z = cls._whole_block_vertical(t3d, meshes, glyph_h)
        if cursor_h is None:
            cursor_h = glyph_h
            cursor_z = actor_loc.z + target_rel.z

        world_pt = FVector(
            actor_loc.x + target_rel.x,
            actor_loc.y + target_rel.y,
            cursor_z - glyph_h * cls.CURSOR_VERTICAL_OFFSET_FRAC,
        )
        scale_vec = FVector(
            0.01,
            glyph_w * cls.CURSOR_WIDTH_FRAC / 100.0,
            (cursor_h / 100.0) * cls.CURSOR_HEIGHT_MULTIPLIER,
        )
        return world_pt, scale_vec, actor_rot

    @classmethod
    def _whole_block_vertical(cls, t3d, meshes, glyph_h):
        """Caret (height, center_z) spanning the entire text block — the
        legacy geometry, correct only for single-line text.  Returns
        (None, None) when no bounds are available."""
        full_top = None
        full_bot = None
        if meshes is not None:
            for m in meshes:
                if m is None:
                    continue
                try:
                    o, e = m.GetComponentBounds()
                    t = o.z + e.z
                    b = o.z - e.z
                    if full_top is None or t > full_top:
                        full_top = t
                    if full_bot is None or b < full_bot:
                        full_bot = b
                except Exception:
                    continue
        try:
            o, e = t3d.GetComponentBounds()
            t = o.z + e.z
            b = o.z - e.z
            if full_top is None or t > full_top:
                full_top = t
            if full_bot is None or b < full_bot:
                full_bot = b
        except Exception:
            pass
        if full_top is None or full_bot is None:
            return None, None
        tight = full_top - full_bot
        full_top += tight * cls.CURSOR_DIACRITIC_HEADROOM_FRAC
        return full_top - full_bot, (full_top + full_bot) * 0.5

    @classmethod
    def _text_lines(cls, kernings, glyph_h):
        """Group glyph indices into text lines by their kerning (layout) Z.

        Kerning Z is where Text3D *places* each glyph, so it's identical for
        every glyph on a line regardless of glyph shape — unlike mesh bounds,
        whose center varies per glyph (a quote sits high, a period low), which
        would split one line of mixed-height text into phantom rows.

        Returns (lines, kern_spacing) with lines a list of
        {'kz', 'idxs'} ordered top→bottom, or ([], 0.0) when unusable."""
        pairs = []
        if kernings:
            for i in range(len(kernings)):
                k = kernings[i]
                if k is None:
                    continue
                try:
                    pairs.append((k.get_relative_location().z, i))
                except Exception:
                    continue
        if not pairs:
            return [], 0.0
        pairs.sort(key=lambda p: -p[0])
        # Kerning Z has no intra-line spread, and lines are a glyph-height or
        # more apart, so half a glyph height cleanly separates them.
        tol = 0.5 * (glyph_h or cls.CHAR_HEIGHT)
        lines = []
        for kz, i in pairs:
            if lines and (lines[-1]['kz'] - kz) <= tol:
                lines[-1]['idxs'].append(i)
            else:
                lines.append({'kz': kz, 'idxs': [i]})
        if len(lines) >= 2:
            gaps = sorted(lines[j]['kz'] - lines[j + 1]['kz']
                          for j in range(len(lines) - 1))
            kern_spacing = gaps[len(gaps) // 2]
        else:
            kern_spacing = (glyph_h or cls.CHAR_HEIGHT) * 1.2
        return lines, kern_spacing

    @classmethod
    def _caret_vertical_for_row(cls, kernings, meshes, glyph_h, text, string_idx):
        """Caret (height, center_z) for the line containing ``string_idx``.
        Lines are grouped by kerning Z; each line's world band comes from its
        glyph meshes.  Extrapolates below the last line for empty trailing
        lines (a freshly inserted newline).  Returns (None, None) when no
        lines can be derived, so the caller falls back to whole-block geometry."""
        lines, kern_spacing = cls._text_lines(kernings, glyph_h)
        if not lines:
            return None, None

        def band(idxs):
            top = bot = None
            if meshes is not None:
                for i in idxs:
                    if i >= len(meshes) or meshes[i] is None:
                        continue
                    try:
                        o, e = meshes[i].GetComponentBounds()
                        t = o.z + e.z
                        b = o.z - e.z
                        if top is None or t > top:
                            top = t
                        if bot is None or b < bot:
                            bot = b
                    except Exception:
                        continue
            return top, bot

        # Map text rows to glyph lines.  Rows with no visible glyph (blank or
        # spaces-only) have no kerning line, so text row N is NOT glyph line
        # N once a blank row appears above it.  glyph_row[k] = text row of
        # the k-th glyph line.
        row_texts = text.split('\n')
        glyph_row = [r for r, t in enumerate(row_texts)
                     if any(c not in ' \t' for c in t)]
        glyph_row = glyph_row[:len(lines)]
        line_of_row = {r: k for k, r in enumerate(glyph_row)}

        # World band per line; derive world line-spacing (per text row) from
        # band centers, dividing by the rows between them so blank rows don't
        # inflate it.  Fall back to kerning spacing when too few bands.
        bands = [band(L['idxs']) for L in lines]
        samples = []
        for k in range(min(len(bands), len(glyph_row)) - 1):
            (t0, b0), (t1, b1) = bands[k], bands[k + 1]
            dr = glyph_row[k + 1] - glyph_row[k]
            if t0 is None or t1 is None or dr <= 0:
                continue
            samples.append(((t0 + b0) - (t1 + b1)) * 0.5 / dr)
        if samples:
            samples.sort()
            spacing = samples[len(samples) // 2]
        else:
            spacing = kern_spacing or ((glyph_h or cls.CHAR_HEIGHT) * 1.2)

        n = len(text)
        si = max(0, min(string_idx, n))
        row = text.count('\n', 0, si)
        if row in line_of_row:
            top, bot = bands[line_of_row[row]]
        else:
            # Blank row (or geometry not laid out yet): shift the nearest
            # glyph line above it (else below it) by whole rows.
            above = [r for r in glyph_row if r < row]
            ref_row = above[-1] if above else (glyph_row[0] if glyph_row else None)
            if ref_row is None:
                ref_row, (top, bot) = len(lines) - 1, bands[-1]
            else:
                top, bot = bands[line_of_row[ref_row]]
            if top is not None:
                shift = spacing * (row - ref_row)
                top -= shift
                bot -= shift
        if top is None or bot is None:
            return None, None
        tight = top - bot
        top += tight * cls.CURSOR_DIACRITIC_HEADROOM_FRAC
        return top - bot, (top + bot) * 0.5

    @classmethod
    def _caret_target_rel(cls, text, string_idx, kernings, meshes, glyph_w):
        """Relative (x, y, z) of the caret at ``string_idx`` on its own text
        line.  Every string index gets its own slot — spaces, indentation,
        trailing spaces and empty lines included (see _caret_ys).  Returns
        None to fall back to legacy glyph-only placement."""
        ys, ref_x, zs = cls._caret_ys(text, kernings, meshes)
        if ys is None:
            return None
        si = max(0, min(string_idx, len(text)))
        return FVector(ref_x, ys[si], zs[si])

    @staticmethod
    def _median(vals, default):
        vals = sorted(v for v in vals if v is not None)
        if not vals:
            return default
        return vals[len(vals) // 2]

    @classmethod
    def _caret_ys(cls, text, kernings, meshes):
        """Caret position (relative Y and Z) for EVERY string index
        0..len(text).  Returns (ys, ref_x, zs), or (None, None, None).

        Text3D only creates kerning/mesh slots for visible characters — spaces
        and newlines get none — so mapping through glyph indices alone
        collapses a run of spaces into a single caret position.

        Only kerning (layout) positions are used: the glyph mesh components
        don't expose GetComponentBounds to Python, so ink extents are
        unavailable.  Here:
          - a glyph's left edge is its kerning Y; right after it is the next
            glyph's left edge when adjacent, else left + typical advance
          - Z is the line's kerning Z; lines with no glyph (blank or
            spaces-only) are spaced from their neighbours by the measured
            line pitch
          - characters with no glyph (spaces, or glyphs not laid out yet) are
            spread between the surrounding glyphs in proportion to an
            estimated advance, or extrapolated at line starts/ends and on
            glyph-less lines; indentation is spread from the left margin.
        """
        if not kernings:
            return None, None, None
        n = len(text)
        nk = len(kernings)

        meas = {}       # string idx -> [left_y, right_y or None, rel_z]
        widths = []
        ref_x = None
        g = 0
        for i, c in enumerate(text):
            if c in ' \t\n':
                continue
            gi = g
            g += 1
            if gi >= nk or kernings[gi] is None:
                continue
            try:
                rel = kernings[gi].get_relative_location()
            except Exception:
                continue
            if ref_x is None:
                ref_x = rel.x
            w = None
            if meshes is not None and gi < len(meshes) and meshes[gi] is not None:
                try:
                    _, e = meshes[gi].GetComponentBounds()
                    w = e.y * 2.0
                    widths.append(w)
                except Exception:
                    pass
            meas[i] = [rel.y, None if w is None else rel.y + w, rel.z]
        if not meas:
            return None, None, None

        # Rows: (start, end) string indices; end = index of '\n' or n.
        rows = []
        s = 0
        while True:
            nl = text.find('\n', s)
            if nl < 0:
                rows.append((s, n))
                break
            rows.append((s, nl))
            s = nl + 1

        # Typical advance from directly adjacent glyph pairs on one row.
        advs = [meas[i + 1][0] - meas[i][0]
                for rs, re_ in rows for i in range(rs, re_ - 1)
                if i in meas and i + 1 in meas
                and meas[i + 1][0] > meas[i][0]]
        glyph_w = cls._median(widths, cls._median(advs, cls.CHAR_WIDTH))
        for i, m in meas.items():
            if m[1] is None:
                if i + 1 in meas and meas[i + 1][0] > m[0]:
                    m[1] = meas[i + 1][0]
                else:
                    m[1] = m[0] + glyph_w

        # Per-row Z (kerning layout Z).  Glyph-less rows extrapolate from the
        # nearest measured row by the line pitch.
        row_z = [None] * len(rows)
        for r, (rs, re_) in enumerate(rows):
            for i in range(rs, re_):
                if i in meas:
                    row_z[r] = meas[i][2]
                    break
        known = [r for r in range(len(rows)) if row_z[r] is not None]
        pitch = cls._median(
            [(row_z[a] - row_z[b]) / (b - a) for a, b in zip(known, known[1:])
             if row_z[a] > row_z[b]],
            glyph_w * 2.3)
        for r in range(len(rows)):
            if row_z[r] is None:
                above = [k for k in known if k < r]
                k = above[-1] if above else known[0]
                row_z[r] = row_z[k] - pitch * (r - k)

        starts = [meas[rs][0] for rs, _ in rows if rs in meas]
        margin = min(starts) if starts else min(m[0] for m in meas.values())

        # Space width: from indentation and from pure-space runs between
        # glyphs (minus the normal ink gap between adjacent glyphs).
        ink_gaps, runs, samples = [], [], []
        for rs, re_ in rows:
            prev = None
            for i in range(rs, re_):
                if i not in meas:
                    continue
                if prev is None:
                    if i > rs and starts and all(text[j] == ' ' for j in range(rs, i)):
                        samples.append((meas[i][0] - margin) / (i - rs))
                else:
                    k = i - prev - 1
                    gap = meas[i][0] - meas[prev][1]
                    if k == 0:
                        ink_gaps.append(gap)
                    elif all(text[j] == ' ' for j in range(prev + 1, i)):
                        runs.append((gap, k))
                prev = i
        ink_gap = cls._median(ink_gaps, 0.0)
        samples += [(gap - ink_gap) / k for gap, k in runs]
        space_w = cls._median([v for v in samples if v > 0], glyph_w * 0.6)

        def adv(i):
            return space_w if text[i] in ' \t' else glyph_w

        ys = [0.0] * (n + 1)
        for rs, re_ in rows:
            anchors = [i for i in range(rs, re_) if i in meas]
            if not anchors:
                y = margin
                for i in range(rs, re_ + 1):
                    ys[i] = y
                    if i < re_:
                        y += adv(i)
                continue
            a0 = anchors[0]
            lead = range(rs, a0)
            if (a0 > rs and starts
                    and all(text[i] == ' ' for i in lead)
                    and meas[a0][0] > margin):
                for i in lead:
                    ys[i] = margin + (meas[a0][0] - margin) * (i - rs) / (a0 - rs)
            else:
                y = meas[a0][0]
                for i in range(a0 - 1, rs - 1, -1):
                    y -= adv(i)
                    ys[i] = y
            for a, b in zip(anchors, anchors[1:] + [None]):
                ys[a] = meas[a][0]
                if b is None:
                    y = meas[a][1]
                    for i in range(a + 1, re_ + 1):
                        ys[i] = y
                        if i < re_:
                            y += adv(i)
                    continue
                total = sum(adv(i) for i in range(a + 1, b))
                lo, hi = meas[a][1], meas[b][0]
                acc = 0.0
                for i in range(a + 1, b):
                    ys[i] = lo + (hi - lo) * (acc / total if total else 0.0)
                    acc += adv(i)
        zs = [0.0] * (n + 1)
        for r, (rs, re_) in enumerate(rows):
            for i in range(rs, re_ + 1):
                zs[i] = row_z[r]
        return ys, ref_x, zs

    def tick(self, dt):
        # Scale lerp
        cur = self.uobject.get_actor_scale()
        tgt = self.target_scale
        a = min(1.0, self.LERP_SPEED * dt)
        self.uobject.set_actor_scale(FVector(
            cur.x + (tgt.x - cur.x) * a,
            cur.y + (tgt.y - cur.y) * a,
            cur.z + (tgt.z - cur.z) * a,
        ))

        if self.text3d is None:
            return

        # Cursor hit this actor?
        hit = self.uobject.get_hit_result_under_cursor(ECollisionChannel.ECC_WorldDynamic)
        on_self = hit is not None and hit.actor == self.uobject

        # Tick-based hover fallback
        if not self._component_hover:
            if on_self and not self._hovered:
                self._hovered = True
                self.on_hover_begin(self.text3d)
            elif not on_self and self._hovered:
                self._hovered = False
                self.on_hover_end(self.text3d)

        # Click detection (rising-edge on left mouse button)
        mouse_down = self._is_mouse_down()
        if mouse_down and not self._was_mouse_down:
            if on_self:
                self._process_click(hit.impact_point)
        self._was_mouse_down = mouse_down

    # Hover callbacks (called by component events or tick fallback)

    def _comp_hover_begin(self, component):
        self._hovered = True
        self.on_hover_begin(component)

    def _comp_hover_end(self, component):
        self._hovered = False
        self.on_hover_end(component)

    def on_hover_begin(self, component):
        d = self.HOVER_DELTA
        bs = self.base_scale
        self.target_scale = FVector(bs.x + d, bs.y + d, bs.z + d)

    def on_hover_end(self, component):
        self.target_scale = self.base_scale

    # Click processing — world hit -> local coords -> character col/row

    def _process_click(self, world_pt):
        text = ''
        char_meshes = None
        if self.text3d is not None:
            try:
                text = str(self.text3d.Text or '')
            except Exception:
                pass
            try:
                char_meshes = self.text3d.CharacterMeshes
            except Exception:
                pass

        # Strategy 1: CharacterMeshes (proportional fonts)
        mesh_idx = None
        mesh_letter = None
        if char_meshes is not None and len(char_meshes) > 0:
            best_idx = -1
            best_dist = float('inf')
            for i, mesh in enumerate(char_meshes):
                if mesh is None:
                    continue
                try:
                    origin, extent = mesh.GetComponentBounds()
                    lo_y = origin.y - extent.y
                    hi_y = origin.y + extent.y
                    lo_z = origin.z - extent.z
                    hi_z = origin.z + extent.z
                    in_y = lo_y <= world_pt.y <= hi_y
                    in_z = lo_z <= world_pt.z <= hi_z
                    if in_y and in_z:
                        best_idx = i
                        break
                    mid_y = (lo_y + hi_y) / 2.0
                    d = abs(world_pt.y - mid_y)
                    if d < best_dist:
                        best_dist = d
                        best_idx = i
                except Exception:
                    continue
            if best_idx >= 0:
                flat = text.replace('\n', '')
                mesh_idx = best_idx
                mesh_letter = flat[best_idx] if best_idx < len(flat) else '?'

        # Strategy 2: fixed-width grid fallback
        local_pt = self._world_to_local(world_pt)
        col = -1
        row = -1
        if local_pt is not None:
            col = int(local_pt.y / self.CHAR_WIDTH)
            row = int(-local_pt.z / self.CHAR_HEIGHT)

        # Pick best result
        if mesh_idx is not None:
            letter = mesh_letter
            idx = mesh_idx
            method = 'CharacterMeshes'
        else:
            idx = col
            lines = text.split('\n')
            if 0 <= row < len(lines) and 0 <= col < len(lines[row]):
                letter = lines[row][col]
            else:
                letter = '?'
            method = 'fixed-width'

        local_str = ''
        if local_pt is not None:
            local_str = (f'local=({local_pt.x:.1f}, {local_pt.y:.1f}, '
                         f'{local_pt.z:.1f})  ')

        if self._VERBOSE:
            ue.log(
                f'PyActorText3D click: letter="{letter}"  index={idx}  '
                f'method={method}  '
                f'actor={self.uobject.get_name()}  '
                f'{local_str}'
                f'world=({world_pt.x:.1f}, {world_pt.y:.1f}, {world_pt.z:.1f})'
            )
        self._on_char_click(col, row, letter=letter, char_index=idx)

    def _world_to_local(self, world_pt):
        actor_transform = self.uobject.get_actor_transform()
        try:
            from unreal_engine.classes import KismetMathLibrary
            return KismetMathLibrary.InverseTransformLocation(actor_transform, world_pt)
        except Exception:
            pass
        # Manual fallback
        try:
            import math
            loc = self.uobject.get_actor_location()
            rot = self.uobject.get_actor_rotation()
            delta = FVector(world_pt.x - loc.x,
                            world_pt.y - loc.y,
                            world_pt.z - loc.z)
            yaw = math.radians(-rot.yaw)
            pitch = math.radians(-rot.pitch)
            roll = math.radians(-rot.roll)
            cy, sy = math.cos(yaw), math.sin(yaw)
            x1 =  cy * delta.x + sy * delta.y
            y1 = -sy * delta.x + cy * delta.y
            z1 = delta.z
            cp, sp = math.cos(pitch), math.sin(pitch)
            x2 =  cp * x1 - sp * z1
            y2 = y1
            z2 =  sp * x1 + cp * z1
            cr, sr = math.cos(roll), math.sin(roll)
            return FVector(x2, cr * y2 + sr * z2, -sr * y2 + cr * z2)
        except Exception as e:
            ue.log_warning(f'PyActorText3D._world_to_local fallback failed: {e}')
            return None

    @classmethod
    def _world_to_local_cls(cls, actor, world_pt):
        """Class-level world→local for the global click path (no self)."""
        try:
            actor_transform = actor.get_actor_transform()
        except Exception:
            return None
        try:
            from unreal_engine.classes import KismetMathLibrary
            return KismetMathLibrary.InverseTransformLocation(actor_transform, world_pt)
        except Exception:
            pass
        try:
            import math
            loc = actor.get_actor_location()
            rot = actor.get_actor_rotation()
            delta = FVector(world_pt.x - loc.x,
                            world_pt.y - loc.y,
                            world_pt.z - loc.z)
            yaw = math.radians(-rot.yaw)
            pitch = math.radians(-rot.pitch)
            roll = math.radians(-rot.roll)
            cy, sy = math.cos(yaw), math.sin(yaw)
            x1 =  cy * delta.x + sy * delta.y
            y1 = -sy * delta.x + cy * delta.y
            z1 = delta.z
            cp, sp = math.cos(pitch), math.sin(pitch)
            x2 =  cp * x1 - sp * z1
            y2 = y1
            z2 =  sp * x1 + cp * z1
            cr, sr = math.cos(roll), math.sin(roll)
            return FVector(x2, cr * y2 + sr * z2, -sr * y2 + cr * z2)
        except Exception:
            return None

    def _is_mouse_down(self):
        try:
            from unreal_engine import FKey
            return self.player_controller.IsInputKeyDown(FKey('LeftMouseButton'))
        except Exception:
            pass
        try:
            return self.player_controller.IsInputKeyDown('LeftMouseButton')
        except Exception:
            return False

    # Focus state — proxies the global registry on PyActorGlobalClick so
    # callers can read/write `actor.focused` per instance while a single
    # source of truth remains class-level (only one Text3D can be focused
    # at a time across the scene).

    @property
    def focused(self):
        return PyActorGlobalClick._focused_actor is self.uobject

    @focused.setter
    def focused(self, value):
        if value:
            PyActorText3D._set_focused_actor(self.uobject)
        elif PyActorGlobalClick._focused_actor is self.uobject:
            PyActorText3D._set_focused_actor(None)

    # Override point

    def _on_char_click(self, col, row, letter=None, char_index=None):
        """
        Called after every click with the character position.

        Parameters
        ----------
        col        : int   — column (0-indexed from left) via fixed-width grid
        row        : int   — row (0-indexed from top) via fixed-width grid
        letter     : str   — the resolved character ('A', 'z', ' ', etc.)
        char_index : int   — flat index into the text string (accounts for
                             proportional glyph widths when CharacterMeshes
                             is available)

        Override in a subclass or monkey-patch after spawn.

        Caret placement is NOT done here: begin_play registers this actor
        with the global typing system, whose mouse poll (_poll_mouse_click)
        places the caret and handles selection.  Moving the caret here too
        (by glyph index, which can't see spaces) raced it.
        """
        pass

    # ============================================================
    # Typing system (class-level) — absorbed from test_text3d_click
    # ============================================================

    @staticmethod
    def _actor_alive(actor):
        """False for None and for wrappers whose UObject died with a previous
        PIE session (every call on them raises 'invalid state')."""
        if actor is None:
            return False
        try:
            actor.get_name()
            return True
        except Exception:
            return False

    @classmethod
    def _prune_stale(cls):
        """Drop class-level refs to actors destroyed by a previous PIE
        session. The interpreter outlives PIE, so these otherwise persist."""
        alive = cls._actor_alive
        cls._watched = {a for a in cls._watched if alive(a)}
        cls._watched_renderer = {
            a: r for a, r in cls._watched_renderer.items() if alive(a)}
        cls._highlight_actors = [a for a in cls._highlight_actors if alive(a)]
        cls._inline_images = [t for t in cls._inline_images if alive(t[0])]
        if not alive(cls._cursor_pyactor):
            cls._cursor_pyactor = None
        if not alive(cls._global_actor):
            cls._global_actor = None
        fa = PyActorGlobalClick._focused_actor
        if fa is not None and not alive(fa):
            PyActorGlobalClick._focused_actor = None
            cls._string_idx = 0
            cls._anchor = 0

    @classmethod
    def register_actor(cls, actor, renderer=None):
        """Register *actor* as a typing target.  Idempotent.

        ``renderer`` is an optional table renderer that will get
        recompute_layout() called on it when *actor* loses focus (for
        auto-sizing tables that should refit after a text edit)."""
        if actor is None:
            return
        cls._watched.add(actor)
        if renderer is not None:
            cls._watched_renderer[actor] = renderer

    @classmethod
    def _ensure_global_typing(cls):
        """One-shot init of ctypes + PyActorGlobalClick + global tick.
        Safe to call repeatedly — short-circuits after the first time."""
        cls._prune_stale()
        if cls._typing_initialized and cls._actor_alive(cls._global_actor):
            return
        cls._typing_initialized = True

        # ctypes / Win32 setup (keyboard, clipboard).  Mouse uses VK_LBUTTON
        # via the same GetAsyncKeyState path so we don't need an
        # input_manager dependency.
        try:
            import ctypes
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
            user32.GetAsyncKeyState.restype = ctypes.c_short
            user32.GetKeyState.argtypes = [ctypes.c_int]
            user32.GetKeyState.restype = ctypes.c_short
            user32.MapVirtualKeyW.argtypes = [ctypes.c_uint, ctypes.c_uint]
            user32.MapVirtualKeyW.restype = ctypes.c_uint
            user32.ToUnicode.argtypes = [
                ctypes.c_uint, ctypes.c_uint,
                ctypes.POINTER(ctypes.c_ubyte), ctypes.c_wchar_p,
                ctypes.c_int, ctypes.c_uint,
            ]
            user32.ToUnicode.restype = ctypes.c_int
            user32.OpenClipboard.argtypes = [ctypes.c_void_p]
            user32.OpenClipboard.restype = ctypes.c_int
            user32.CloseClipboard.argtypes = []
            user32.CloseClipboard.restype = ctypes.c_int
            user32.EmptyClipboard.argtypes = []
            user32.EmptyClipboard.restype = ctypes.c_int
            user32.GetClipboardData.argtypes = [ctypes.c_uint]
            user32.GetClipboardData.restype = ctypes.c_void_p
            user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
            user32.SetClipboardData.restype = ctypes.c_void_p
            user32.IsClipboardFormatAvailable.argtypes = [ctypes.c_uint]
            user32.IsClipboardFormatAvailable.restype = ctypes.c_int
            user32.GetDoubleClickTime.argtypes = []
            user32.GetDoubleClickTime.restype = ctypes.c_uint
            kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
            kernel32.GlobalAlloc.restype = ctypes.c_void_p
            kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
            kernel32.GlobalLock.restype = ctypes.c_void_p
            kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
            kernel32.GlobalUnlock.restype = ctypes.c_int
            kernel32.GlobalSize.argtypes = [ctypes.c_void_p]
            kernel32.GlobalSize.restype = ctypes.c_size_t
            cls._ctypes = ctypes
            cls._user32 = user32
            cls._kernel32 = kernel32
            cls._WIN32_TYPING_OK = True
        except Exception as e:
            cls._WIN32_TYPING_OK = False
            ue.log_warning(f'PyActorText3D: ctypes typing unavailable ({e})')

        # Spawn PyActorGlobalClick + attach the global tick.  Hook the
        # renderer-refit-on-unfocus behaviour via add_unfocus_handler so
        # focus state stays single-sourced on PyActorGlobalClick.
        try:
            from ue_spawn import spawn_pyactor
            cls._global_actor = spawn_pyactor(
                'actors.pyactor_global_click', 'PyActorGlobalClick',
                location=FVector(0, 0, 0),
                name='PyActorGlobalClick')
            proxy = cls._global_actor.get_py_proxy()
            proxy.set_tick_fn(cls._global_tick)
            PyActorGlobalClick.add_unfocus_handler(cls._on_actor_unfocus)
            ue.log('PyActorText3D: typing system online '
                   '(PyActorGlobalClick + Win32 keyboard/mouse)')
        except Exception as e:
            ue.log_warning(
                f'PyActorText3D: typing-system bootstrap failed: {e}')

    @classmethod
    def _on_actor_unfocus(cls, prev_actor):
        """Refit the previous actor's table renderer (if any) so an
        auto-sizing table snaps back after a text edit.  Registered with
        PyActorGlobalClick.add_unfocus_handler from _ensure_global_typing."""
        renderer = cls._watched_renderer.get(prev_actor)
        if renderer is None:
            return
        if not getattr(renderer, 'auto_size', True):
            return
        try:
            renderer.recompute_layout()
        except Exception as e:
            ue.log_warning(f'PyActorText3D: recompute_layout failed: {e}')

    # ---- Focus + selection helpers ----

    @classmethod
    def _set_focused_actor(cls, actor):
        """Single mutation point for focus.  Delegates to PyActorGlobalClick
        which fires unfocus handlers; this class registered _on_actor_unfocus
        to handle table refit."""
        PyActorGlobalClick.set_focused_actor(actor)

    @classmethod
    def _get_focused(cls):
        return PyActorGlobalClick.get_focused_actor()

    @classmethod
    def _sel_range(cls):
        """Return (start, end) of the selection sorted.  start==end means none."""
        a = cls._anchor
        c = cls._string_idx
        return (a, c) if a <= c else (c, a)

    @classmethod
    def _has_sel(cls):
        return cls._anchor != cls._string_idx

    @classmethod
    def _set_caret(cls, idx, extend_selection=False):
        cls._string_idx = idx
        if not extend_selection:
            cls._anchor = idx

    # TEMP DEBUG: log how Text3D lays out the glyph arrays vs the source text,
    # so we can confirm whether spaces/newlines occupy kerning/mesh slots.
    # Remove once the index mapping is verified.
    _DEBUG_GLYPHS = False

    # TEMP: per-click logging disabled. Flip to True to restore.
    _VERBOSE = False

    @classmethod
    def _log_glyph_arrays(cls, where, text, kernings, meshes):
        try:
            nk = len(kernings) if kernings else 0
            nm = len(meshes) if meshes else 0
            sp = text.count(' ')
            nl = text.count('\n')
            none_meshes = sum(1 for m in (meshes or []) if m is None)
            ue.log(
                f'[T3D-DBG {where}] text={text!r} len={len(text)} '
                f'spaces={sp} newlines={nl} | kernings={nk} meshes={nm} '
                f'none_meshes={none_meshes} | '
                f'space-incl(len-nl)={len(text) - nl} '
                f'space-excl(len-sp-nl)={len(text) - sp - nl}')
        except Exception as e:
            ue.log_warning(f'[T3D-DBG] log failed: {e}')

    @staticmethod
    def _string_idx_to_glyph(text, sidx):
        """Count visible chars in text[:sidx] (Text3D makes no glyph for
        space, tab or newline)."""
        sidx = max(0, min(sidx, len(text)))
        return sum(1 for c in text[:sidx] if c not in ' \t\n')

    @staticmethod
    def _glyph_to_string_idx(text, tg):
        """Return the string index of the tg-th visible char (or len(text))."""
        count = 0
        for i, c in enumerate(text):
            if count == tg:
                return i
            if c not in ' \t\n':
                count += 1
        return len(text)

    # ---- Selection-highlight pool ----

    @classmethod
    def _spawn_highlight_box(cls):
        """Spawn one selection-highlight bar, built exactly like the caret
        (BP_PyActorEmpty + 'Cube' mesh + the caret's translucent material,
        see pyactor_cursor.PyActorHighlight) so it renders the same way.
        Hidden until _render_highlight_segment places it."""
        try:
            from ue_spawn import spawn_pyactor
            actor = spawn_pyactor(
                'actors.pyactor_cursor', 'PyActorHighlight',
                components=[dict(class_name='StaticMeshComponent',
                                 name='Cube', root=True,
                                 mesh='/Engine/BasicShapes/Cube.Cube')],
                name='TextSelHighlight')
        except Exception as e:
            ue.log_warning(f'PyActorText3D: highlight spawn failed: {e}')
            return None
        if actor is None:
            return None
        try:
            actor.SetActorEnableCollision(False)
        except Exception:
            pass
        try:
            actor.SetActorHiddenInGame(True)
        except Exception:
            pass
        return actor

    @classmethod
    def _ensure_highlight(cls, i):
        """Lazily grow the highlight pool to at least i+1 actors."""
        while len(cls._highlight_actors) <= i:
            a = cls._spawn_highlight_box()
            if a is None:
                return None
            try:
                a.SetActorLabel(f'TextSelHighlight_{len(cls._highlight_actors)}')
            except Exception:
                pass
            cls._highlight_actors.append(a)
        return cls._highlight_actors[i]

    @classmethod
    def _hide_highlights(cls):
        for a in cls._highlight_actors:
            try:
                a.SetActorHiddenInGame(True)
            except Exception:
                pass

    @classmethod
    def _unfocus(cls):
        cls._set_focused_actor(None)
        cls._string_idx = 0
        cls._anchor = 0
        cls.hide_cursor()
        cls._hide_highlights()

    @classmethod
    def _render_highlight_segment(cls, pool_idx, actor, text, seg_start, seg_end,
                                  pad=0.0):
        """Render one highlight box for string range [seg_start, seg_end) on
        a single line, using the same placement as the caret.  ``pad`` widens
        the right end (selection running through the line's newline, so a
        selected blank line still shows)."""
        box = cls._ensure_highlight(pool_idx)
        if box is None:
            return
        left = cls.compute_placement(
            actor, cls._string_idx_to_glyph(text, seg_start),
            string_idx=seg_start, text=text)
        right = cls.compute_placement(
            actor, cls._string_idx_to_glyph(text, seg_end),
            string_idx=seg_end, text=text)
        if left is None or right is None:
            try:
                box.SetActorHiddenInGame(True)
            except Exception:
                pass
            return
        lwp, lscale, lrot = left
        rwp, _, _ = right
        span_uu = (rwp.y - lwp.y) + pad
        if span_uu < 1.0:
            try:
                box.SetActorHiddenInGame(True)
            except Exception:
                pass
            return
        mid_wp = FVector(lwp.x, lwp.y + span_uu * 0.5, lwp.z)
        try:
            box.set_actor_scale(FVector(0.01, span_uu / 100.0, lscale.z))
        except Exception:
            pass
        box.set_actor_location(mid_wp)
        box.set_actor_rotation(lrot)
        box.SetActorHiddenInGame(False)

    HIGHLIGHT_NEWLINE_PAD = 20.0

    @classmethod
    def _update_highlight(cls):
        """Rebuild highlight boxes from current selection (one per line)."""
        cls._hide_highlights()
        actor = cls._get_focused()
        if actor is None or not cls._has_sel():
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return
        try:
            text = str(t3d.Text or '')
        except Exception:
            return
        start, end = cls._sel_range()
        end = min(end, len(text))
        pool_idx = 0
        s = start
        while s < end:
            nl = text.find('\n', s, end)
            seg_end = end if nl == -1 else nl
            pad = cls.HIGHLIGHT_NEWLINE_PAD if nl != -1 else 0.0
            if seg_end > s or pad:
                cls._render_highlight_segment(pool_idx, actor, text, s, seg_end, pad)
                pool_idx += 1
            s = seg_end + 1 if nl != -1 else end

    # ---- Mouse → string index ----

    @classmethod
    def _row_caret_zs(cls, actor, text):
        """World Z where the caret renders on each text line (so a click maps
        to the line it visually landed on)."""
        zs = []
        s = 0
        while True:
            p = cls.compute_placement(
                actor, cls._string_idx_to_glyph(text, s), string_idx=s, text=text)
            zs.append(p[0].z if p is not None else None)
            nl = text.find('\n', s)
            if nl < 0:
                return zs
            s = nl + 1

    @classmethod
    def _idx_from_hit(cls, actor, world_pt, row_zs=None):
        """String index nearest a world-space click: the line whose caret is
        closest in Z, then the closest caret slot on that line (spaces
        included).  Returns (idx, text, row_zs) or None."""
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
            text = str(t3d.Text or '')
            kernings = t3d.CharacterKernings
            meshes = t3d.CharacterMeshes
        except Exception:
            return None
        ys, _, _ = cls._caret_ys(text, kernings, meshes)
        if ys is None:
            return None
        if row_zs is None:
            row_zs = cls._row_caret_zs(actor, text)
        rows = []
        s = 0
        while True:
            nl = text.find('\n', s)
            rows.append((s, len(text) if nl < 0 else nl))
            if nl < 0:
                break
            s = nl + 1
        cand = [r for r in range(len(rows))
                if r < len(row_zs) and row_zs[r] is not None]
        row = (min(cand, key=lambda r: abs(world_pt.z - row_zs[r]))
               if cand else 0)
        local = cls._world_to_local_cls(actor, world_pt)
        ly = (local.y if local is not None
              else world_pt.y - actor.get_actor_location().y)
        rs, re_ = rows[row]
        idx = min(range(rs, re_ + 1), key=lambda i: abs(ys[i] - ly))
        return idx, text, row_zs

    @classmethod
    def _word_range(cls, text, idx):
        """(start, end) of the word / whitespace run / symbol at ``idx`` —
        what a double-click selects."""
        n = len(text)
        i = idx if idx < n and text[idx] != '\n' else idx - 1
        if i < 0 or text[i] == '\n':
            return idx, idx
        c = text[i]
        if cls._is_word_char(c):
            same = cls._is_word_char
        elif c in ' \t':
            same = lambda ch: ch in ' \t'
        else:
            return i, i + 1
        s = i
        while s > 0 and same(text[s - 1]):
            s -= 1
        e = i + 1
        while e < n and same(text[e]):
            e += 1
        return s, e

    @classmethod
    def _apply_caret(cls, actor, text, idx, anchor):
        """Set caret + anchor and redraw the cursor and highlight."""
        cls._string_idx = idx
        cls._anchor = anchor
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(text, idx),
                           string_idx=idx, text=text)
        cls._update_highlight()

    @classmethod
    def _position_cursor(cls, hit_actor, hit, extend=False, click_count=1):
        """Place the caret from a click hit and focus ``hit_actor``.

        extend      — Shift+click: keep the anchor, select up to the click.
        click_count — 2 selects the word under the click, 3 the whole line."""
        if hit_actor is None:
            return

        t3d = None
        try:
            t3d = hit_actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            pass

        text = ''
        kernings = None
        meshes = None
        if t3d is not None:
            try:
                text = str(t3d.Text or '')
            except Exception:
                pass
            try:
                kernings = t3d.CharacterKernings
            except Exception:
                pass
            try:
                meshes = t3d.CharacterMeshes
            except Exception:
                pass

        if cls._DEBUG_GLYPHS:
            cls._log_glyph_arrays('click', text, kernings, meshes)

        res = cls._idx_from_hit(hit_actor, hit.impact_point)

        # No kernings — drop the caret directly at the click point via
        # the singleton cursor (skipping placement math entirely).
        if res is None:
            cursor_proxy = cls._get_or_spawn_cursor(hit_actor)
            if cursor_proxy is not None:
                try:
                    cursor_proxy.move_to(
                        hit.impact_point,
                        FVector(0.01, 0.04, 0.5),
                        hit_actor.get_actor_rotation())
                except Exception:
                    pass
            cls._set_focused_actor(hit_actor)
            cls._string_idx = len(text)
            cls._anchor = len(text)
            cls._hide_highlights()
            cls._drag_rows = None
            return

        idx, text, row_zs = res
        cls._drag_rows = row_zs
        same_actor = cls._get_focused() is hit_actor

        if click_count >= 3:
            anchor = cls._line_edge(text, idx, -1)
            idx = cls._line_edge(text, idx, +1)
        elif click_count == 2:
            anchor, idx = cls._word_range(text, idx)
        elif extend and same_actor:
            anchor = cls._anchor
        else:
            anchor = idx

        cls._set_focused_actor(hit_actor)
        # If the previous focus was an auto-sizing table cell, that table
        # just refit and may have shifted hit_actor — _apply_caret places
        # the caret against the current geometry.
        cls._apply_caret(hit_actor, text, idx, anchor)

    @classmethod
    def _drag_to(cls, actor, hit):
        """LMB held after a click on ``actor``: extend the selection to the
        point under the mouse, keeping the anchor from the initial click."""
        if cls._get_focused() is not actor:
            return
        res = cls._idx_from_hit(actor, hit.impact_point, cls._drag_rows)
        if res is None:
            return
        idx, text, _ = res
        anchor = cls._anchor
        if cls._drag_word is not None:
            # Double-click drag: grow by whole words around the first word.
            ws, we = cls._drag_word
            s, e = cls._word_range(text, idx)
            if idx < ws:
                idx, anchor = s, we
            else:
                idx, anchor = max(e, we), ws
        if (idx, anchor) != (cls._string_idx, cls._anchor):
            cls._apply_caret(actor, text, idx, anchor)

    # ---- Text mutation ----

    @classmethod
    def _handle_typed_char(cls, ch):
        """Insert/delete at cursor.  ch='\\b'=backspace, '\\n'=newline, else literal."""
        actor = cls._get_focused()
        if actor is None:
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return

        try:
            text = str(t3d.Text or '')
        except Exception:
            text = ''

        if cls._has_sel():
            start, end = cls._sel_range()
            text = text[:start] + text[end:]
            idx = start
            cls._string_idx = idx
            cls._anchor = idx
            if ch == '\b':
                # Selection-backspace just deletes the selection.
                try:
                    t3d.Text = text
                except Exception as e:
                    ue.log_warning(f'PyActorText3D: failed to set text: {e}')
                    return
                cls.show_cursor_at(actor, cls._string_idx_to_glyph(text, idx),
                                   string_idx=idx, text=text)
                cls._update_highlight()
                return

        idx = max(0, min(cls._string_idx, len(text)))

        if ch == '\b':
            if idx == 0:
                return
            text = text[:idx - 1] + text[idx:]
            idx -= 1
        else:
            text = text[:idx] + ch + text[idx:]
            idx += 1

        try:
            t3d.Text = text
        except Exception as e:
            ue.log_warning(f'PyActorText3D: failed to set text: {e}')
            return

        cls._string_idx = idx
        cls._anchor = idx

        target_glyph = cls._string_idx_to_glyph(text, idx)
        cls.show_cursor_at(actor, target_glyph, string_idx=idx, text=text)
        cls._update_highlight()

    # ---- Modifier-key probes ----

    @classmethod
    def _build_kb_state(cls):
        """256-byte keyboard state for ToUnicode.  High bit=down, low bit=toggle."""
        buf = (cls._ctypes.c_ubyte * 256)()
        for vk in range(256):
            if cls._user32.GetAsyncKeyState(vk) & 0x8000:
                buf[vk] = 0x80
        for tvk in (0x14, 0x90, 0x91):   # Caps / Num / Scroll lock
            if cls._user32.GetKeyState(tvk) & 0x0001:
                buf[tvk] |= 0x01
        return buf

    @classmethod
    def _ctrl_down(cls):
        return cls._WIN32_TYPING_OK and bool(cls._user32.GetAsyncKeyState(0x11) & 0x8000)

    @classmethod
    def _shift_held(cls):
        return cls._WIN32_TYPING_OK and bool(cls._user32.GetAsyncKeyState(0x10) & 0x8000)

    @classmethod
    def _alt_down(cls):
        return cls._WIN32_TYPING_OK and bool(cls._user32.GetAsyncKeyState(0x12) & 0x8000)

    @classmethod
    def _win_down(cls):
        if not cls._WIN32_TYPING_OK:
            return False
        return (bool(cls._user32.GetAsyncKeyState(0x5B) & 0x8000)
                or bool(cls._user32.GetAsyncKeyState(0x5C) & 0x8000))

    # ---- Caret navigation ----

    @staticmethod
    def _is_word_char(c):
        return c.isalnum() or c == '_'

    @classmethod
    def _word_boundary(cls, text, idx, direction):
        """Move idx to the next word boundary in `direction` (+1 or -1)."""
        n = len(text)
        idx = max(0, min(idx, n))
        if direction > 0:
            while idx < n and not cls._is_word_char(text[idx]):
                idx += 1
            while idx < n and cls._is_word_char(text[idx]):
                idx += 1
        else:
            idx = max(0, idx - 1)
            while idx > 0 and not cls._is_word_char(text[idx]):
                idx -= 1
            while idx > 0 and cls._is_word_char(text[idx - 1]):
                idx -= 1
        return idx

    @staticmethod
    def _line_edge(text, idx, direction):
        """Move idx to start (-1) or end (+1) of its line."""
        n = len(text)
        idx = max(0, min(idx, n))
        if direction < 0:
            nl = text.rfind('\n', 0, idx)
            return 0 if nl == -1 else nl + 1
        nl = text.find('\n', idx)
        return n if nl == -1 else nl

    @classmethod
    def _line_delta(cls, text, idx, direction):
        """Move idx up (-1) or down (+1) one line, preserving column."""
        n = len(text)
        idx = max(0, min(idx, n))
        line_start = cls._line_edge(text, idx, -1)
        col = idx - line_start
        if direction < 0:
            if line_start == 0:
                return 0
            prev_end = line_start - 1
            prev_start = cls._line_edge(text, prev_end, -1)
            return min(prev_start + col, prev_end)
        line_end = cls._line_edge(text, idx, +1)
        if line_end == n:
            return n
        next_start = line_end + 1
        next_end = cls._line_edge(text, next_start, +1)
        return min(next_start + col, next_end)

    @classmethod
    def _move_caret_to(cls, new_idx, extend):
        """Set caret, optionally extending selection; refresh cursor + highlight."""
        actor = cls._get_focused()
        if actor is None:
            return
        t3d = None
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            pass
        text = ''
        if t3d is not None:
            try:
                text = str(t3d.Text or '')
            except Exception:
                pass
        new_idx = max(0, min(new_idx, len(text)))
        cls._set_caret(new_idx, extend_selection=extend)
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(text, new_idx),
                           string_idx=new_idx, text=text)
        cls._update_highlight()

    # ---- Clipboard ----

    @classmethod
    def _clipboard_get_text(cls):
        if not cls._WIN32_TYPING_OK:
            return None
        try:
            if not cls._user32.OpenClipboard(0):
                return None
            try:
                if not cls._user32.IsClipboardFormatAvailable(cls._CF_UNICODETEXT):
                    return None
                h = cls._user32.GetClipboardData(cls._CF_UNICODETEXT)
                if not h:
                    return None
                p = cls._kernel32.GlobalLock(h)
                if not p:
                    return None
                try:
                    return cls._ctypes.c_wchar_p(p).value
                finally:
                    cls._kernel32.GlobalUnlock(h)
            finally:
                cls._user32.CloseClipboard()
        except Exception as e:
            ue.log_warning(f'PyActorText3D: clipboard read failed: {e}')
            return None

    @classmethod
    def _clipboard_set_text(cls, text):
        if not cls._WIN32_TYPING_OK or text is None:
            return False
        try:
            if not cls._user32.OpenClipboard(0):
                return False
            try:
                cls._user32.EmptyClipboard()
                GMEM_MOVEABLE = 0x0002
                data = text.encode('utf-16-le') + b'\x00\x00'
                size = len(data)
                h = cls._kernel32.GlobalAlloc(GMEM_MOVEABLE, size)
                if not h:
                    return False
                p = cls._kernel32.GlobalLock(h)
                if not p:
                    return False
                cls._ctypes.memmove(p, data, size)
                cls._kernel32.GlobalUnlock(h)
                # After SetClipboardData, the system owns the handle.
                return bool(cls._user32.SetClipboardData(cls._CF_UNICODETEXT, h))
            finally:
                cls._user32.CloseClipboard()
        except Exception as e:
            ue.log_warning(f'PyActorText3D: clipboard write failed: {e}')
            return False

    @classmethod
    def _clipboard_get_image(cls):
        try:
            from PIL import ImageGrab, Image as PILImage
            img = ImageGrab.grabclipboard()
            if isinstance(img, PILImage.Image):
                return img
            return None
        except Exception as e:
            ue.log_warning(f'PyActorText3D: ImageGrab failed: {e}')
            return None

    # ---- Edit actions ----

    @classmethod
    def _delete_selection(cls):
        """Delete selected text in focused actor.  Returns True if anything deleted."""
        actor = cls._get_focused()
        if actor is None or not cls._has_sel():
            return False
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return False
        if t3d is None:
            return False
        try:
            text = str(t3d.Text or '')
        except Exception:
            return False
        start, end = cls._sel_range()
        new_text = text[:start] + text[end:]
        try:
            t3d.Text = new_text
        except Exception as e:
            ue.log_warning(f'PyActorText3D: delete_selection failed: {e}')
            return False
        cls._string_idx = start
        cls._anchor = start
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(new_text, start),
                           string_idx=start, text=new_text)
        cls._update_highlight()
        return True

    @classmethod
    def _select_all(cls):
        actor = cls._get_focused()
        if actor is None:
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return
        try:
            text = str(t3d.Text or '')
        except Exception:
            return
        cls._anchor = 0
        cls._string_idx = len(text)
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(text, len(text)),
                           string_idx=len(text), text=text)
        cls._update_highlight()

    @classmethod
    def _copy(cls):
        if not cls._has_sel():
            return
        actor = cls._get_focused()
        if actor is None:
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return
        try:
            text = str(t3d.Text or '')
        except Exception:
            return
        s, e = cls._sel_range()
        cls._clipboard_set_text(text[s:e])

    @classmethod
    def _cut(cls):
        if not cls._has_sel():
            return
        cls._copy()
        cls._delete_selection()

    @classmethod
    def _paste(cls):
        if cls._get_focused() is None:
            return
        # Image first — if clipboard has a bitmap, inline-paste it.
        img = cls._clipboard_get_image()
        if img is not None:
            cls._paste_image(img)
            return
        # Otherwise paste text at caret, replacing any selection.
        clip = cls._clipboard_get_text()
        if not clip:
            return
        if cls._has_sel():
            cls._delete_selection()
        for c in clip:
            if c == '\r':
                continue   # CRLF → LF
            cls._handle_typed_char(c)

    @classmethod
    def _delete_forward(cls):
        actor = cls._get_focused()
        if actor is None:
            return
        if cls._has_sel():
            cls._delete_selection()
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return
        try:
            text = str(t3d.Text or '')
        except Exception:
            return
        idx = cls._string_idx
        if idx >= len(text):
            return
        new_text = text[:idx] + text[idx + 1:]
        try:
            t3d.Text = new_text
        except Exception:
            return
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(new_text, idx),
                           string_idx=idx, text=new_text)
        cls._update_highlight()

    @classmethod
    def _cycle_focus(cls, direction=1):
        """Ctrl+Tab — move focus to the next (or previous) registered actor."""
        if not cls._watched:
            return
        ordered = list(cls._watched)
        current = cls._get_focused()
        if current in ordered:
            i = (ordered.index(current) + direction) % len(ordered)
        else:
            i = 0
        new_actor = ordered[i]
        new_text = ''
        try:
            t3d = new_actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
            if t3d is not None:
                new_text = str(t3d.Text or '')
        except Exception:
            pass
        cls._set_focused_actor(new_actor)
        cls._string_idx = len(new_text)
        cls._anchor = len(new_text)
        cls.show_cursor_at(new_actor, cls._string_idx_to_glyph(new_text, len(new_text)),
                           string_idx=len(new_text), text=new_text)
        cls._hide_highlights()

    # ---- Inline image paste ----

    @classmethod
    def _paste_image(cls, pil_img):
        """Inline-paste a PIL image into the focused Text3D at the caret.
        The image is scaled so its height matches the text's line height,
        then space characters are inserted to reserve horizontal room and
        the image actor is placed over the reserved spaces."""
        actor = cls._get_focused()
        if actor is None:
            return
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
        except Exception:
            return
        if t3d is None:
            return
        try:
            text = str(t3d.Text or '')
        except Exception:
            text = ''

        text_h = 50.0
        try:
            o, e = t3d.GetComponentBounds()
            text_h = max(text_h, e.z * 2.0 * 0.8)
        except Exception:
            pass
        glyph_w = 50.0
        try:
            meshes = t3d.CharacterMeshes
            if meshes is not None:
                for m in meshes:
                    if m is None:
                        continue
                    try:
                        _, e = m.GetComponentBounds()
                        glyph_w = e.y * 2.0
                        break
                    except Exception:
                        continue
        except Exception:
            pass

        iw, ih = float(pil_img.width), float(pil_img.height)
        if ih <= 0:
            return
        img_h_uu = text_h
        img_w_uu = iw / ih * img_h_uu
        n_spaces = max(1, int(round(img_w_uu / glyph_w)))

        if cls._has_sel():
            cls._delete_selection()
            try:
                text = str(t3d.Text or '')
            except Exception:
                text = ''

        idx = cls._string_idx
        placeholder = ' ' * n_spaces
        new_text = text[:idx] + placeholder + text[idx:]
        try:
            t3d.Text = new_text
        except Exception as e:
            ue.log_warning(f'PyActorText3D: paste_image set text failed: {e}')
            return

        image_actor = None
        try:
            import tempfile, os, time
            from ue_spawn import spawn_image
            tmpdir = os.path.join(tempfile.gettempdir(), 'ue_clipboard_images')
            try:
                os.makedirs(tmpdir, exist_ok=True)
            except Exception:
                pass
            tmp_path = os.path.join(tmpdir, f'clip_{int(time.time()*1000)}.png')
            pil_img.convert('RGBA').save(tmp_path, 'PNG')
            img_scale = FVector(img_w_uu / 100.0, 0.05, img_h_uu / 100.0)
            image_actor = spawn_image(tmp_path, scale=img_scale)
        except Exception as e:
            ue.log_warning(f'PyActorText3D: spawn_image failed: {e}')

        if image_actor is not None:
            try:
                mid_idx = idx + n_spaces // 2
                mid_glyph = cls._string_idx_to_glyph(new_text, mid_idx)
                placement = cls.compute_placement(actor, mid_glyph)
                if placement is not None:
                    world_pt, _, rot = placement
                    image_actor.set_actor_location(world_pt)
                    image_actor.set_actor_rotation(rot)
                    image_actor.attach_to_actor(actor)
            except Exception as e:
                ue.log_warning(f'PyActorText3D: image position failed: {e}')
            cls._inline_images.append(
                (actor, image_actor, idx, n_spaces, img_w_uu, img_h_uu))

        new_idx = idx + n_spaces
        cls._string_idx = new_idx
        cls._anchor = new_idx
        cls.show_cursor_at(actor, cls._string_idx_to_glyph(new_text, new_idx),
                           string_idx=new_idx, text=new_text)
        cls._update_highlight()

    # ---- Keyboard rising-edge dispatch ----

    @classmethod
    def _on_vk_rise(cls, vk):
        """Rising-edge handler.  Dispatches shortcuts, then falls through to
        ToUnicode for ordinary character entry (notepad's WM_CHAR semantics)."""
        if cls._get_focused() is None:
            return

        ctrl = cls._ctrl_down()
        shift = cls._shift_held()
        alt = cls._alt_down()
        win = cls._win_down()

        # Notepad parity: Alt+key (Alt+Tab/Enter/F4/Backspace) and Win+key
        # are never text input.  AltGr on European layouts reports
        # Alt+Ctrl together AND produces characters through ToUnicode, so
        # the `not ctrl` clause keeps that path open.
        if (alt and not ctrl) or win:
            return

        if ctrl:
            if vk == 0x41:    # A
                cls._select_all(); return
            if vk == 0x43:    # C
                cls._copy(); return
            if vk == 0x58:    # X
                cls._cut(); return
            if vk == 0x56:    # V
                cls._paste(); return
            if vk == 0x09:    # Tab
                cls._cycle_focus(-1 if shift else +1); return
            actor = cls._get_focused()
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME) if actor else None
            text = str(t3d.Text or '') if t3d else ''
            idx = cls._string_idx
            if vk == 0x25:    # Ctrl+Left  — prev word
                cls._move_caret_to(cls._word_boundary(text, idx, -1), shift); return
            if vk == 0x27:    # Ctrl+Right — next word
                cls._move_caret_to(cls._word_boundary(text, idx, +1), shift); return
            if vk == 0x24:    # Ctrl+Home  — doc start
                cls._move_caret_to(0, shift); return
            if vk == 0x23:    # Ctrl+End   — doc end
                cls._move_caret_to(len(text), shift); return

        if vk in (0x25, 0x27, 0x26, 0x28, 0x24, 0x23):
            actor = cls._get_focused()
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME) if actor else None
            text = str(t3d.Text or '') if t3d else ''
            idx = cls._string_idx
            if vk == 0x25:    # Left
                if cls._has_sel() and not shift:
                    cls._move_caret_to(cls._sel_range()[0], False); return
                cls._move_caret_to(max(0, idx - 1), shift); return
            if vk == 0x27:    # Right
                if cls._has_sel() and not shift:
                    cls._move_caret_to(cls._sel_range()[1], False); return
                cls._move_caret_to(min(len(text), idx + 1), shift); return
            if vk == 0x26:    # Up
                cls._move_caret_to(cls._line_delta(text, idx, -1), shift); return
            if vk == 0x28:    # Down
                cls._move_caret_to(cls._line_delta(text, idx, +1), shift); return
            if vk == 0x24:    # Home
                cls._move_caret_to(cls._line_edge(text, idx, -1), shift); return
            if vk == 0x23:    # End
                cls._move_caret_to(cls._line_edge(text, idx, +1), shift); return

        if vk == 0x08:        # VK_BACK
            cls._handle_typed_char('\b'); return
        if vk == 0x2E:        # VK_DELETE
            cls._delete_forward(); return
        if vk == 0x0D:        # VK_RETURN
            # Ctrl+Enter and Shift+Enter are PyActorText3DExecutor's "run"
            # chords, not text. If the typing system inserted a newline here
            # too, every run would append a blank line to the focused code
            # (and a mid-text caret would corrupt it). Let the executor
            # consume both chords.
            if ctrl or shift:
                return
            cls._handle_typed_char('\n'); return
        if vk == 0x09:        # VK_TAB
            cls._handle_typed_char('\t'); return
        if vk == 0x1B:        # VK_ESCAPE
            cls._unfocus(); return

        # Suppress Ctrl+letter producing control chars (e.g. Ctrl+B → 0x02).
        if ctrl:
            return
        try:
            kb_state = cls._build_kb_state()
            scan_code = cls._user32.MapVirtualKeyW(vk, 0)
            outbuf = cls._ctypes.create_unicode_buffer(8)
            result = cls._user32.ToUnicode(
                vk, scan_code, kb_state, outbuf, len(outbuf), 0)
        except Exception:
            return
        if result > 0:
            for c in outbuf.value[:result]:
                if c and ord(c) >= 0x20:
                    cls._handle_typed_char(c)

    @classmethod
    def _poll_keyboard(cls):
        """Call each tick.  Fires character events on rising edges while focused."""
        if not cls._WIN32_TYPING_OK:
            return
        curr = bytearray(256)
        for vk in range(256):
            if cls._user32.GetAsyncKeyState(vk) & 0x8000:
                curr[vk] = 1
        if cls._get_focused() is not None:
            for vk in range(256):
                if curr[vk] and not cls._prev_vk_down[vk]:
                    cls._on_vk_rise(vk)
        for i in range(256):
            cls._prev_vk_down[i] = curr[i]

    # ---- Mouse rising-edge → focus + cursor placement ----

    @classmethod
    def _trace_under_cursor(cls):
        """Hit result under the mouse (Visibility, then WorldDynamic) or None."""
        # Need a UObject for get_hit_result_under_cursor; use the global
        # actor's uobject (ticking already guarantees it).
        trace_obj = cls._global_actor
        pc = None
        try:
            pc = get_world().get_player_controller(0)
        except Exception:
            pass
        for channel in (ECollisionChannel.ECC_Visibility,
                        ECollisionChannel.ECC_WorldDynamic):
            for src in (trace_obj, pc):
                if src is None:
                    continue
                try:
                    h = src.get_hit_result_under_cursor(channel)
                    if h is not None:
                        return h
                except Exception:
                    continue
        return None

    @classmethod
    def _double_click_secs(cls):
        try:
            return max(0.1, cls._user32.GetDoubleClickTime() / 1000.0)
        except Exception:
            return 0.5

    class _RayHit:
        """Minimal stand-in for a trace hit (actor + impact_point + distance)."""
        def __init__(self, actor, point, distance):
            self.actor = actor
            self.impact_point = point
            self.distance = distance

    @classmethod
    def _mouse_ray(cls):
        """(origin, direction) of the mouse ray in world space, or None."""
        try:
            pc = get_world().get_player_controller(0)
            ok, o, d = pc.DeprojectMousePositionToWorld()
            if ok:
                return o, d
        except Exception:
            pass
        return None

    @classmethod
    def _ray_text_plane(cls, actor, ray):
        """Intersect the mouse ray with ``actor``'s text plane.
        Returns (world_point, distance) or None."""
        o, d = ray
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
            k0 = t3d.CharacterKernings[0]
            try:
                p = k0.get_world_location()
            except Exception:
                loc = actor.get_actor_location()
                r = k0.get_relative_location()
                p = FVector(loc.x + r.x, loc.y + r.y, loc.z + r.z)
            n = actor.get_actor_forward()
        except Exception:
            return None
        denom = d.x * n.x + d.y * n.y + d.z * n.z
        if abs(denom) < 1e-6:
            return None
        t = ((p.x - o.x) * n.x + (p.y - o.y) * n.y + (p.z - o.z) * n.z) / denom
        if t <= 0:
            return None
        return FVector(o.x + d.x * t, o.y + d.y * t, o.z + d.z * t), t

    @classmethod
    def _text_rect(cls, actor):
        """World (y_min, y_max, z_min, z_max) covering ``actor``'s text,
        including empty trailing lines and trailing spaces."""
        # Built from caret placements (line starts and ends) — glyph mesh
        # bounds aren't readable from Python.
        try:
            t3d = actor.get_actor_component(cls.TEXT_COMPONENT_NAME)
            text = str(t3d.Text or '')
        except Exception:
            return None
        y0 = y1 = z0 = z1 = None
        s = 0
        while True:
            nl = text.find('\n', s)
            end = len(text) if nl < 0 else nl
            for idx in (s, end):
                p = cls.compute_placement(
                    actor, cls._string_idx_to_glyph(text, idx),
                    string_idx=idx, text=text)
                if p is None:
                    continue
                wp, sc, _ = p
                half = sc.z * 50.0
                y0 = wp.y if y0 is None else min(y0, wp.y)
                y1 = wp.y if y1 is None else max(y1, wp.y)
                z0 = wp.z - half if z0 is None else min(z0, wp.z - half)
                z1 = wp.z + half if z1 is None else max(z1, wp.z + half)
            if nl < 0:
                break
            s = nl + 1
        if y0 is None:
            return None
        pad = cls.CHAR_WIDTH * 0.5
        return y0 - pad, y1 + pad, z0, z1

    @classmethod
    def _ray_pick_text(cls, max_distance=None):
        """Watched actor whose text area the mouse ray crosses (nearest
        first), as a _RayHit — for clicks the collision box misses (e.g.
        lines below the first).  Ignores text farther than ``max_distance``
        (something solid in front of it).  Returns None if none."""
        ray = cls._mouse_ray()
        if ray is None:
            return None
        best = None
        for w in cls._watched:
            if not cls._actor_alive(w):
                continue
            res = cls._ray_text_plane(w, ray)
            if res is None:
                continue
            pt, dist = res
            if max_distance is not None and dist > max_distance:
                continue
            rect = cls._text_rect(w)
            if rect is None:
                continue
            ya, yb, za, zb = rect
            if ya <= pt.y <= yb and za <= pt.z <= zb:
                if best is None or dist < best.distance:
                    best = cls._RayHit(w, pt, dist)
        return best

    @classmethod
    def _poll_mouse_click(cls):
        """LMB polling for the typing system:
          - rising edge on a watched actor: place caret + focus (Shift+click
            extends the selection; double-click selects a word, triple-click
            a line).  Off-click unfocuses.
          - held after a click on a watched actor: drag-select.
          - release: end the drag."""
        if not cls._WIN32_TYPING_OK:
            return
        # VK_LBUTTON = 0x01 — system-wide mouse state, doesn't need foreground.
        down = bool(cls._user32.GetAsyncKeyState(0x01) & 0x8000)
        prev = cls._prev_lbutton_down
        cls._prev_lbutton_down = down

        if not down:
            cls._drag_actor = None
            cls._drag_rows = None
            cls._drag_word = None
            return

        if prev:
            # Held: drag-select while the mouse stays over the clicked text.
            actor = cls._drag_actor
            if actor is None or not cls._actor_alive(actor):
                cls._drag_actor = None
                return
            hit = cls._trace_under_cursor()
            if hit is None or not (hit.actor == actor):
                # Off the collision box (other lines, or past the text):
                # follow the mouse ray on the text's own plane instead.
                ray = cls._mouse_ray()
                res = cls._ray_text_plane(actor, ray) if ray else None
                hit = cls._RayHit(actor, res[0], res[1]) if res else None
            if hit is not None:
                cls._drag_to(actor, hit)
            return

        hit = cls._trace_under_cursor()
        hit_actor = hit.actor if hit is not None else None
        matched = None
        if hit_actor is not None:
            for w in cls._watched:
                try:
                    if w == hit_actor:
                        matched = w
                        break
                except Exception:
                    pass

        if cls._DEBUG_GLYPHS:
            try:
                ha = hit_actor.get_name() if hit_actor is not None else None
                ma = matched.get_name() if matched is not None else None
                ue.log(f'[T3D-DBG poll] hit={ha} matched={ma} '
                       f'watched={len(cls._watched)}')
            except Exception:
                pass

        if matched is None:
            # The trace missed the text's collision box (it doesn't cover
            # every line) — try the mouse ray against each text's area,
            # unless something solid sits in front of it.
            dist = None
            try:
                if hit is not None and hit.actor is not None:
                    dist = hit.distance
            except Exception:
                dist = None
            rh = cls._ray_pick_text(max_distance=dist)
            if rh is not None:
                hit, matched = rh, rh.actor
        if matched is None:
            cls._click_count = 0
            cls._unfocus()
            return

        # Multi-click: same actor, within the system double-click time.
        import time
        now = time.perf_counter()
        if (matched is cls._last_click_actor
                and now - cls._last_click_time <= cls._double_click_secs()):
            cls._click_count = cls._click_count % 3 + 1
        else:
            cls._click_count = 1
        cls._last_click_time = now
        cls._last_click_actor = matched

        shift = cls._shift_held() and cls._click_count == 1
        cls._position_cursor(matched, hit, extend=shift,
                             click_count=cls._click_count)
        cls._drag_actor = matched
        cls._drag_word = (cls._sel_range() if cls._click_count == 2 else None)

    @classmethod
    def _global_tick(cls, dt):
        """The tick attached to PyActorGlobalClick by _ensure_global_typing."""
        cls._poll_keyboard()
        cls._poll_mouse_click()
