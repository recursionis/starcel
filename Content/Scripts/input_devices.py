import unreal_engine as ue
from unreal_engine.enums import EMouseCursor, ECollisionChannel
from unreal_engine.classes import StarcelHelper, InputSettings
import time


def _clean(s: str):
    return s.replace(" ", "").replace("_", "").lower()


def _load_project_input_names():
    """Read axis/action mapping names from Project Settings > Input.
    Returns (axis_map, action_map): lowercase token -> canonical name.

    Tries GetAxisNames/GetActionNames first, then falls back to iterating
    the AxisMappings/ActionMappings UPROPERTY arrays. UnrealEnginePython's
    binding for the output-param Get*Names variants can return empty on UE 4.27.
    """
    axis_map, action_map = {}, {}
    try:
        settings = ue.get_mutable_default(InputSettings)
    except Exception as e:
        ue.log_warning(f'input_devices: could not read project input settings: {e}')
        return axis_map, action_map

    def _add(m, name):
        if name:
            m[_clean(name)] = name

    # Preferred: GetAxisNames / GetActionNames (may be empty on 4.27).
    try:
        for n in (settings.GetAxisNames() or []):
            _add(axis_map, str(n))
    except Exception:
        pass
    try:
        for n in (settings.GetActionNames() or []):
            _add(action_map, str(n))
    except Exception:
        pass

    # Fallback: iterate mapping arrays directly.
    if not axis_map:
        try:
            for m in (settings.AxisMappings or []):
                _add(axis_map, str(getattr(m, 'AxisName', '') or ''))
        except Exception:
            pass
    if not action_map:
        try:
            for m in (settings.ActionMappings or []):
                _add(action_map, str(getattr(m, 'ActionName', '') or ''))
        except Exception:
            pass

    return axis_map, action_map


class Keyboard:
    def __init__(self):
        self.ue_keys = ["AnyKey",
                        "MouseX", "MouseY", "Mouse2D", "MouseScrollUp", "MouseScrollDown", "MouseWheelAxis",
                        "LeftMouseButton", "RightMouseButton", "MiddleMouseButton", "ThumbMouseButton", "ThumbMouseButton2",
                        "BackSpace", "Tab", "Enter", "Pause",
                        "CapsLock", "Escape", "SpaceBar", "PageUp", "PageDown", "End", "Home",
                        "Left", "Up", "Right", "Down",
                        "Insert", "Delete",
                        "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
                        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                        "NumPadZero", "NumPadOne", "NumPadTwo", "NumPadThree", "NumPadFour", "NumPadFive", "NumPadSix", "NumPadSeven", "NumPadEight", "NumPadNine",
                        "Multiply", "Add", "Subtract", "Decimal", "Divide",
                        "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                        "NumLock",
                        "ScrollLock",
                        "LeftShift", "RightShift", "LeftControl", "RightControl", "LeftAlt", "RightAlt", "LeftCommand", "RightCommand",
                        "Semicolon", "Equals", "Comma", "Underscore", "Hyphen", "Period", "Slash", "Tilde", "LeftBracket", "Backslash", "RightBracket", "Apostrophe",
                        "Ampersand", "Asterix", "Caret", "Colon", "Dollar", "Exclamation", "LeftParantheses", "RightParantheses", "Quote"
                        ]

        self.LEGEND_TO_UE = {
            # letters
            **{chr(i): chr(i).upper() for i in range(ord('a'), ord('z') + 1)},
            **{chr(i).upper(): chr(i).upper() for i in range(ord('a'), ord('z') + 1)},

            # numbers
            "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four", "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine",

            # numpad
            "NumPadZero": "NumPadZero",
            "NumPadOne": "NumPadOne",
            "NumPadTwo": "NumPadTwo",
            "NumPadThree": "NumPadThree",
            "NumPadFour": "NumPadFour",
            "NumPadFive": "NumPadFive",
            "NumPadSix": "NumPadSix",
            "NumPadSeven": "NumPadSeven",
            "NumPadEight": "NumPadEight",
            "NumPadNine": "NumPadNine",

            # control keys
            "Esc": "Escape",
            "Tab": "Tab",
            "Caps": "CapsLock",
            "Enter": "Enter",
            "Backspace": "BackSpace",
            "Space": "SpaceBar",

            "LeftShift": "LeftShift",
            "RightShift": "RightShift",
            "LeftCtrl": "LeftControl",
            "RightCtrl": "RightControl",
            "LeftAlt": "LeftAlt",
            "RightAlt": "RightAlt",
            "Win": "Win",
            "Menu": "Menu",

            # arrows
            "Left": "Left",
            "Right": "Right",
            "Up": "Up",
            "Down": "Down",

            # navigation
            "Ins": "Insert",
            "Del": "Delete",
            "Home": "Home",
            "End": "End",
            "PgUp": "PageUp",
            "PgDn": "PageDown",

            # symbols
            "`": "Tilde",
            "~": "Tilde",
            "-": "Hyphen",
            "_": "Underscore",
            "=": "Equals",
            "+": "Add",
            "[": "LeftBracket",
            "]": "RightBracket",
            "\\": "Backslash",
            "|": "Backslash",
            ";": "Semicolon",
            ":": "Colon",
            "'": "Apostrophe",
            "\"": "Quote",
            ",": "Comma",
            ".": "Period",
            "/": "Slash",
            "?": "Slash",

            "!": "Exclamation",
            "@": "At",
            "#": "Hash",
            "$": "Dollar",
            "%": "Percent",
            "^": "Caret",
            "&": "Ampersand",
            "*": "Asterix",
            "(": "LeftParantheses",
            ")": "RightParantheses",
        }

        self.keyboard_wootingtwohe = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "PrtSc", "Pause", "ScrLk", "M1", "M2", "M3", "MR"],
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace", "Ins", "Home", "PgUp", "Num", "/", "*", "-"],
            ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\", "Del", "End", "PgDn", "NumPadSeven", "NumPadEight", "NumPadNine", "+"],
            ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter", None, None, None, "NumPadFour", "NumPadFive", "NumPadSix", "+"],
            ["LeftShift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "RightShift", None, "Up", None, "NumPadOne", "NumPadTwo", "NumPadThree", "Enter"],
            ["LeftCtrl", "Win", "LeftAlt", "Space", "RightAlt", "Menu", "Fn", "RightCtrl", "Left", "Down", "Right", "NumPadZero", "NumPadZero", ".", "Enter"]
        ]
        self.keyboard_wootingtwohe_shift = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "PrtSc", "Pause", "ScrLk", "M1", "M2", "M3", "MR"],
            ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "Backspace", "Ins", "Home", "PgUp", "Num", "/", "*", "-"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|", "Del", "End", "PgDn", "NumPadSeven", "NumPadEight", "NumPadNine", "+"],
            ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "Enter", None, None, None, "NumPadFour", "NumPadFive", "NumPadSix", "+"],
            ["LeftShift", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "RightShift", None, "Up", None, "NumPadOne", "NumPadTwo", "NumPadThree", "Enter"],
            ["LeftCtrl", "Win", "LeftAlt", "Space", "RightAlt", "Menu", "Fn", "RightCtrl", "Left", "Down", "Right", "NumPadZero", "NumPadZero", ".", "Enter"]
        ]
        self.keyboard_razerblade152019 = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Ins", "Delete"],
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter"],
            ["LeftShift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Up", "RightShift"],
            ["LeftCtrl", "Fn", "Win", "LeftAlt", "Space", "RightAlt", "RightCtrl", "Left", "Down", "Right", "Fn"]
        ]
        self.keyboard_razerblade152019_shift = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Ins", "Delete"],
            ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "Backspace"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
            ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "Enter"],
            ["LeftShift", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "Up", "RightShift"],
            ["LeftCtrl", "Fn", "Win", "LeftAlt", "Space", "RightAlt", "RightCtrl", "Left", "Down", "Right", "Fn"]
        ]
        self.keyboard_ANSI = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
            ["Caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter"],
            ["LeftShift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "RightShift"],
            ["LeftCtrl", "Win", "LeftAlt", "Space", "RightAlt", "Win", "Menu", "RightCtrl"]
        ]
        self.keyboard_ANSI_shift = [
            ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "Backspace"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
            ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\"", "Enter"],
            ["LeftShift", "Z", "X", "C", "V", "B", "N", "M", "<", ">", "?", "RightShift"],
            ["LeftCtrl", "Win", "LeftAlt", "Space", "RightAlt", "Win", "Menu", "RightCtrl"]
        ]

        self.ue_ansi = self.keyboard_to_ue_keyboard(self.keyboard_ANSI)
        self.ue_ansi_shift = self.keyboard_to_ue_keyboard(self.keyboard_ANSI_shift)
        self.ue_wooting = self.keyboard_to_ue_keyboard(self.keyboard_wootingtwohe)
        self.ue_wooting_shift = self.keyboard_to_ue_keyboard(self.keyboard_wootingtwohe_shift)
        self.ue_razerblade152019 = self.keyboard_to_ue_keyboard(self.keyboard_razerblade152019)
        self.ue_razerblade152019_shift = self.keyboard_to_ue_keyboard(self.keyboard_razerblade152019_shift)

        # user-defined aliases
        self.ALIASES = {
            "ctrl": "LeftControl",
            "control": "LeftControl",
            "shift": "LeftShift",
            "alt": "LeftAlt",
            "cmd": "LeftCommand",
            "command": "LeftCommand",
            "win": "LeftCommand",
            "esc": "Escape",
            "space": "SpaceBar",
            "bksp": "BackSpace",
            "del": "Delete",
        }

        self._build_normalize_map()

    def _build_normalize_map(self):
        self.normalize_map = {}
        for k, v in self.LEGEND_TO_UE.items():
            self.normalize_map[_clean(k)] = v
        for k in self.ue_keys:
            self.normalize_map[_clean(k)] = k
        for k, v in self.ALIASES.items():
            self.normalize_map[_clean(k)] = v

    def normalize(self, token):
        if not token:
            return None
        t = token.strip().lower()

        # check aliases first
        if t in self.ALIASES:
            return self.ALIASES[t]

        # check LEGEND_TO_UE
        if token in self.LEGEND_TO_UE:
            return self.LEGEND_TO_UE[token]
        for k, v in self.LEGEND_TO_UE.items():
            if k.lower() == t:
                return v

        # fallback: UE native keys
        if token in self.ue_keys:
            return token
        for k in self.ue_keys:
            if k.lower() == t:
                return k

        print(f"{token} not registered in input_devices")
        return None

    def keyboard_to_ue_keyboard(self, keyboard_layout):
        ue_keyboard = []

        for row in keyboard_layout:
            ue_row = []
            for key in row:
                if key is None or key == "":
                    ue_row.append(None)
                    continue

                ue_key = self.LEGEND_TO_UE.get(key)

                # fallback: already a UE key?
                if ue_key is None and key in self.LEGEND_TO_UE.values():
                    ue_key = key

                ue_row.append(ue_key)
            ue_keyboard.append(ue_row)

        return ue_keyboard


class Mouse:
    def __init__(self):
        self.ue_keys = ["AnyKey",
                        "MouseX", "MouseY", "Mouse2D", "MouseScrollUp", "MouseScrollDown", "MouseWheelAxis",
                        "LeftMouseButton", "RightMouseButton", "MiddleMouseButton", "ThumbMouseButton", "ThumbMouseButton2",
                        "BackSpace", "Tab", "Enter", "Pause",
                        "CapsLock", "Escape", "SpaceBar", "PageUp", "PageDown", "End", "Home",
                        "Left", "Up", "Right", "Down",
                        "Insert", "Delete",
                        "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
                        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                        "NumPadZero", "NumPadOne", "NumPadTwo", "NumPadThree", "NumPadFour", "NumPadFive", "NumPadSix", "NumPadSeven", "NumPadEight", "NumPadNine",
                        "Multiply", "Add", "Subtract", "Decimal", "Divide",
                        "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
                        "NumLock",
                        "ScrollLock",
                        "LeftShift", "RightShift", "LeftControl", "RightControl", "LeftAlt", "RightAlt", "LeftCommand", "RightCommand",
                        "Semicolon", "Equals", "Comma", "Underscore", "Hyphen", "Period", "Slash", "Tilde", "LeftBracket", "Backslash", "RightBracket", "Apostrophe",
                        "Ampersand", "Asterix", "Caret", "Colon", "Dollar", "Exclamation", "LeftParantheses", "RightParantheses", "Quote"
                        ]

        self.mouse = ["Left", "Right", "Middle", "ThumbUp", "ThumbDown", "ScrollUp", "ScrollDown", "MouseX", "MouseY", "Mouse2D", "MouseWheelAxis"]

        self.LEGEND_TO_UE = {
            "Left": "LeftMouseButton",
            "Right": "RightMouseButton",
            "Middle": "MiddleMouseButton",
            "ThumbUp": "ThumbUpMouseButton",
            "ThumbDown": "ThumbDownMouseButton",
            "ScrollUp": "MouseScrollUp",
            "ScrollDown": "MouseScrollDown",
            "MouseX": "MouseX",
            "MouseY": "MouseY",
            "Mouse2D": "Mouse2D",
            "MouseWheelAxis": "MouseWheelAxis",
        }

        self.ALIASES = {
            "lmb": "LeftMouseButton",
            "rmb": "RightMouseButton",
            "mmb": "MiddleMouseButton",
            "left": "LeftMouseButton",
            "right": "RightMouseButton",
            "middle": "MiddleMouseButton",
            "wheel": "MouseWheelAxis",
            "scrollup": "MouseScrollUp",
            "scrolldown": "MouseScrollDown",
        }
        self._build_normalize_map()

    def _build_normalize_map(self):
        self.normalize_map = {}
        for k, v in self.LEGEND_TO_UE.items():
            self.normalize_map[_clean(k)] = v
        for k in self.ue_keys:
            self.normalize_map[_clean(k)] = k
        for k, v in self.ALIASES.items():
            self.normalize_map[_clean(k)] = v

    def normalize(self, token):
        if not token:
            return None
        t = token.strip().lower()

        if t in self.ALIASES:
            return self.ALIASES[t]
        if token in self.LEGEND_TO_UE:
            return self.LEGEND_TO_UE[token]
        for k, v in self.LEGEND_TO_UE.items():
            if k.lower() == t:
                return v
        if token in self.ue_keys:
            return token
        for k in self.ue_keys:
            if k.lower() == t:
                return k

        return None  # just return None, no warning


class TraceHelper:
    def __init__(self, uobject):
        self.uobject = uobject
        self.pc = uobject.get_player_controller()

    def trace_forward(self, dist=1000):
        """Trace from camera forward direction"""
        start = self.pc.get_pawn().get_actor_location()
        end = start + self.pc.get_control_rotation().get_forward_vector() * dist
        hit = self.uobject.line_trace_single_by_channel(start, end, ECollisionChannel.ECC_Visibility)
        return hit

    def trace_cursor(self, channel=ECollisionChannel.ECC_Visibility):
        """Trace from cursor position into the world
        Returns: dict with hit information or None if no hit
        """
        return self.uobject.get_hit_result_under_cursor(channel)

    def trace_line(self, start, end, channel=ECollisionChannel.ECC_Visibility):
        """Generic line trace between two points"""
        return self.uobject.line_trace_single_by_channel(start, end, channel)

    def deproject_screen(self, x, y):
        """Convert screen coordinates to world position and direction"""
        success, world_pos, world_dir = self.pc.DeprojectScreenPositionToWorld(x, y)
        if success:
            return world_pos, world_dir
        return None, None

    # Debug logging
    @staticmethod
    def _log_hit(hit, label, show_normal=False, show_distance=False):
        ue.log(f"=== {label} ===")
        if not hit:
            ue.log("Nothing hit")
            return
        actor = hit.get('actor')
        ue.log(f"Hit Actor: {actor.get_name() if actor else 'None'}")
        ue.log(f"Hit Location: {hit.get('location')}")
        if show_normal:
            ue.log(f"Hit Normal: {hit.get('normal')}")
        if show_distance:
            ue.log(f"Distance: {hit.get('distance', 0):.1f}")

    def log_cursor_hit(self, channel=ECollisionChannel.ECC_Visibility):
        """Trace from the cursor into the world and log what was hit"""
        hit = self.trace_cursor(channel)
        self._log_hit(hit, "CURSOR TRACE", show_normal=True)
        return hit

    def log_forward_hit(self, dist=5000):
        """Trace forward from the pawn along the control rotation and log what was hit"""
        hit = self.trace_forward(dist=dist)
        self._log_hit(hit, "FORWARD TRACE", show_distance=True)
        return hit


class HotkeyManager:
    def __init__(self, uobject, keyboard, mouse, poll_rate=0.02):
        self.uobject = uobject
        self.keyboard = keyboard
        self.mouse = mouse
        self.sequence_bindings = []
        self.sequence_progress = {}
        self._axis_handlers = {}
        self._last_axis_values = {}
        self.poll_rate = poll_rate
        self._repeat_bindings = []
        self._pollers = []
        self._key_registry = {}  # For future keyboard visualization
        self._is_shutting_down = False

        self._axis_names, self._action_names = _load_project_input_names()

        self.player_controller = self.uobject.get_player_controller()

        # Seed from PC so toggle_cursor() doesn't no-op on first call when
        # bShowMouseCursor is False but our flag would default to True.
        try:
            self._cursor_visible = bool(self.player_controller.bShowMouseCursor)
        except Exception:
            self._cursor_visible = False

    def resolve_axis_name(self, token):
        """Return the canonical axis name for *token*.

        Always returns the token (or its canonical-case form) so that
        UE's own bind_axis can resolve it — unknown tokens are silently
        ignored by UE, matching the pre-validation behavior. The local
        _axis_names table is only used for case-normalization; on UE 4.27
        the InputSettings reflection is unreliable, so a missing entry
        is not treated as an error."""
        if not token:
            return None
        if self._axis_names:
            canonical = self._axis_names.get(_clean(token))
            if canonical is not None:
                return canonical
        return token

    def resolve_action_name(self, token):
        """Return the canonical action name for *token*. Same fallback
        behavior as resolve_axis_name."""
        if not token:
            return None
        if self._action_names:
            canonical = self._action_names.get(_clean(token))
            if canonical is not None:
                return canonical
            ue.log_warning(
                f"bind_action: '{token}' is not a defined action mapping. "
                f"Check Project Settings > Input > Action Mappings.")
        return token

    # Shutdown
    def shutdown(self):
        """Call this in uObject_EndPlay to clean up properly"""
        self._is_shutting_down = True

        # Stop all pollers
        for ticker in self._pollers:
            try:
                if ticker and hasattr(ticker, 'is_valid') and ticker.is_valid():
                    ue.remove_ticker(ticker)
            except:
                pass

        for ticker in self._repeat_bindings:
            try:
                if ticker and hasattr(ticker, 'is_valid') and ticker.is_valid():
                    ue.remove_ticker(ticker)
            except:
                pass

        self._pollers.clear()
        self._repeat_bindings.clear()
        ue.log("HotkeyManager shutdown complete")

    # Cursor
    def enable_mouse_events(self, click=True, over=True):
        """Enable mouse click and mouse-over events"""
        try:
            self.player_controller.bEnableClickEvents = click
            self.player_controller.bEnableMouseOverEvents = over
        except:
            ue.log_warning("Mouse event flags not supported")

    def show_cursor(self, visible=True):
        """Show or hide mouse cursor"""
        try:
            self.player_controller.bShowMouseCursor = visible
            self._cursor_visible = visible
        except:
            ue.log_warning("show cursor failed")

    def set_cursor(self, cursor_type=EMouseCursor.Default):
        """Set cursor type
        Options: None, Default, TextEditBeam, ResizeLeftRight, ResizeUpDown,
                 ResizeSouthEast, ResizeSouthWest, CardinalCross, Crosshairs,
                 Hand, GrabHand, GrabHandClosed, SlashedCircle, EyeDropper
        """
        try:
            self.player_controller.CurrentMouseCursor = cursor_type
            ue.log(f"Mouse cursor set to: {cursor_type}")
        except Exception as e:
            ue.log_warning(f"Failed to set cursor: {e}")

    def toggle_cursor(self):
        """Toggle cursor visibility"""
        self.show_cursor(not self._cursor_visible)
        vw, vh = ue.get_viewport_size()
        self.set_mouse_position(vw / 2, vh / 2)
        def _delayed_click(delta):
            StarcelHelper.ClickLMB()
            ue.log("LMB click fired")
            return False

        # UEP GCs the ticker if no reference is held — see unreal_engine_tools.py:584
        # ('assignment required or gc will destroy'). Store on self to keep alive.
        if not hasattr(self, '_click_tickers'):
            self._click_tickers = []
        self._click_tickers.append(ue.add_ticker(_delayed_click, 0.02))

    def print_cursor_info(self):
        """Print cursor configuration information"""
        pc = self.player_controller
        ue.log(f"ClickEventKeys = {getattr(pc, 'ClickEventKeys', None)}")
        ue.log(f"DefaultMouseCursor = {getattr(pc, 'DefaultMouseCursor', None)}")
        ue.log(f"CurrentMouseCursor = {getattr(pc, 'CurrentMouseCursor', None)}")

    def get_cursor_info(self):
        """Get cursor screen position, world position, and direction
        Returns: dict with keys: 'screen_x', 'screen_y', 'world_pos', 'world_dir'
        """
        pos_data = self.get_mouse_position(deproject=True)
        if not pos_data:
            return None

        x, y, world, direction = pos_data
        return {
            'screen_x': x,
            'screen_y': y,
            'world_pos': world,
            'world_dir': direction
        }

    def log_mouse_world(self):
        """Log the cursor's screen position and its deprojected world position/direction"""
        info = self.get_cursor_info()
        if not info:
            ue.log("Could not get mouse position")
            return None
        ue.log("=== CURSOR INFO ===")
        ue.log(f"Mouse Screen: ({info['screen_x']:.1f}, {info['screen_y']:.1f})")
        ue.log(f"World Pos: {info['world_pos']}")
        ue.log(f"World Dir: {info['world_dir']}")
        return info

    def log_key_bindings(self, key):
        """Log every binding registered for a specific key"""
        bindings = self.get_key_bindings(key)
        ue.log(f"=== Bindings for '{key}' ===")
        for binding in bindings:
            ue.log(f"  Type: {binding['type']}, Keys: {binding['keys']}, Callback: {binding['callback']}")
        return bindings

    # Normalize
    def normalize_input_token(self, token):
        """Normalize input token to UE format"""
        k = self.keyboard.normalize(token)
        if k:
            return k
        m = self.mouse.normalize(token)
        if m:
            return m
        return token

    def parse_chord(self, chord):
        """Parse chord string into tuple of normalized keys"""
        if isinstance(chord, str):
            parts = chord.split("+")
        else:
            parts = chord
        return tuple(self.normalize_input_token(p) for p in parts)

    # Key Registry (for future visualization)
    def _register_binding(self, keys, binding_type, callback_name=None):
        """Register a binding for future keyboard visualization"""
        key_tuple = keys if isinstance(keys, tuple) else (keys,)

        for key in key_tuple:
            if key not in self._key_registry:
                self._key_registry[key] = []

            self._key_registry[key].append({
                'type': binding_type,
                'keys': key_tuple,
                'callback': callback_name or str(callback_name)
            })

    def get_key_bindings(self, key=None):
        """Get all bindings for a specific key, or all bindings if key is None"""
        if key is None:
            return self._key_registry
        return self._key_registry.get(self.normalize_input_token(key), [])

    # Chords
    def bind_chord_event(self, chord, event_type, callback):
        """Bind a chord (key combination) to a callback"""
        primary = chord[-1]
        modifiers = set(chord[:-1])

        def _handler(method=None):
            for m in modifiers:
                if not self.uobject.is_input_key_down(m):
                    return
            callback()

        self.uobject.bind_key(primary, event_type, _handler)
        self._register_binding(chord, f"chord_{event_type}", callback.__name__ if hasattr(callback, '__name__') else None)

    def bind_sequence(self, sequence, callback, timeout=1.0):
        """Bind a sequence of key presses to a callback"""
        seq_parsed = []

        for step in sequence:
            if isinstance(step, dict) and "axis" in step:
                seq_parsed.append(("AXIS", step["axis"], id(step), step["condition"]))
            else:
                release = False
                if isinstance(step, str) and step.endswith(":release"):
                    step = step.replace(":release", "")
                    release = True

                chord = self.parse_chord(step)
                seq_parsed.append(("KEY", chord, release))

        self.sequence_bindings.append({
            "sequence": seq_parsed,
            "callback": callback,
            "timeout": timeout
        })

        self._bind_sequence_step(seq_parsed[0], seq_parsed, 0)

    def _bind_sequence_step(self, step, sequence, index):
        """Internal: bind a single step in a sequence"""
        kind = step[0]

        if kind == "AXIS":
            _, axis_name, step_id, condition_fn = step

            def _axis_callback(v=None):
                self._advance_sequence_dynamic(sequence, index)

            self.bind_axis_for_sequence(axis_name, condition_fn, _axis_callback)

        elif kind == "KEY":
            _, chord, release = step

            primary = chord[-1]
            modifiers = set(chord[:-1])
            event = ue.IE_RELEASED if release else ue.IE_PRESSED

            def _chord_callback(method=None):
                for m in modifiers:
                    if not self.uobject.is_input_key_down(m):
                        return
                self._advance_sequence_dynamic(sequence, index)

            self.uobject.bind_key(primary, event, _chord_callback)

    def _advance_sequence_dynamic(self, sequence, index_triggered):
        """Internal: advance through a sequence when a step is triggered"""
        now = time.time()

        key = tuple(
            id(step) if step[0] == "AXIS" else (tuple(step[1]), step[2])
            for step in sequence
        )

        progress = self.sequence_progress.get(key, {"index": 0, "last_time": 0})

        timeout = 1.0
        for seq in self.sequence_bindings:
            if seq["sequence"] == sequence:
                timeout = seq["timeout"]
                break

        if now - progress["last_time"] > timeout:
            progress = {"index": 0, "last_time": 0}

        expected = sequence[progress["index"]]

        if expected == sequence[index_triggered]:
            progress["index"] += 1
            progress["last_time"] = now

            if progress["index"] < len(sequence):
                self._bind_sequence_step(sequence[progress["index"]], sequence, progress["index"])
            else:
                for seq in self.sequence_bindings:
                    if seq["sequence"] == sequence:
                        seq["callback"]()
                        break

                progress = {"index": 0, "last_time": 0}

        else:
            progress = {"index": 0, "last_time": 0}

        self.sequence_progress[key] = progress

    def bind_press(self, chord, callback):
        """Bind key press event"""
        parsed_chord = self.parse_chord(chord)
        self.bind_chord_event(parsed_chord, ue.IE_PRESSED, callback)

    def bind_release(self, chord, callback):
        """Bind key release event"""
        parsed_chord = self.parse_chord(chord)
        self.bind_chord_event(parsed_chord, ue.IE_RELEASED, callback)

    def bind_double_click(self, chord, callback):
        """Bind double click event"""
        parsed_chord = self.parse_chord(chord)
        self.bind_chord_event(parsed_chord, ue.IE_DOUBLE_CLICK, callback)

    # Repeat (poll based)
    def bind_repeat(self, chord, callback):
        """Bind a key to repeat while held down (uses polling)"""
        chord = self.parse_chord(chord)

        def poll(delta):
            if self._is_shutting_down:
                return False
            if not self.uobject or not self.uobject.is_valid():
                return False

            primary = chord[-1]
            mods = chord[:-1]
            if self.uobject.is_input_key_down(primary):
                for m in mods:
                    if not self.uobject.is_input_key_down(m):
                        return True
                callback()
            return True

        ticker = ue.add_ticker(poll, self.poll_rate)
        self._repeat_bindings.append(ticker)
        self._register_binding(chord, "repeat", callback.__name__ if hasattr(callback, '__name__') else None)

    # Poll (non-binding check)
    def bind_poll(self, chord, callback, rate=None):
        """Poll a key state continuously without overriding engine bindings
        This checks key state without binding, so it won't interfere with actions like Jump
        """
        chord = self.parse_chord(chord)
        poll_rate = rate if rate is not None else self.poll_rate

        def poll(delta):
            if self._is_shutting_down:
                return False
            if not self.uobject or not self.uobject.is_valid():
                return False

            primary = chord[-1]
            mods = chord[:-1]

            # Check if all keys are down
            all_down = self.uobject.is_input_key_down(primary)
            if all_down:
                for m in mods:
                    if not self.uobject.is_input_key_down(m):
                        all_down = False
                        break

            if all_down:
                callback()

            return True

        ticker = ue.add_ticker(poll, poll_rate)
        self._pollers.append(ticker)
        self._register_binding(chord, "poll", callback.__name__ if hasattr(callback, '__name__') else None)

    def is_key_down(self, key):
        """Check if a key is currently pressed (non-binding check)"""
        normalized = self.normalize_input_token(key)
        return self.uobject.is_input_key_down(normalized)

    def is_chord_down(self, chord):
        """Check if all keys in a chord are currently pressed"""
        parsed = self.parse_chord(chord)
        for key in parsed:
            if not self.uobject.is_input_key_down(key):
                return False
        return True

    # Axis
    def bind_axis(self, axis_name, callback, deadzone=0.0, poll=True):
        """Bind an axis input to a callback
        Note: For MouseX/MouseY, use bind_axis_poll instead as bind_axis may not work reliably
        """
        axis = self.resolve_axis_name(axis_name)
        if axis is None:
            return

        def _handler(v):
            if abs(v) < deadzone:
                v = 0.0
            last = self._last_axis_values.get(axis)
            if last == v:
                return
            self._last_axis_values[axis] = v
            callback(v)

        self.uobject.bind_axis(axis, _handler)
        self._register_binding((axis,), "axis", callback.__name__ if hasattr(callback, '__name__') else None)

        if poll:
            def poller(dt):
                if self._is_shutting_down:
                    return False
                if not self.uobject or not self.uobject.is_valid():
                    return False
                v = self.uobject.get_input_axis(axis)
                _handler(v)
                return True

            ticker = ue.add_ticker(poller, self.poll_rate)
            self._pollers.append(ticker)

    def bind_axis_poll(self, axis_name, callback, deadzone=0.0, rate=None):
        """Bind an axis using only polling (more reliable for MouseX/MouseY)
        Use this for mouse movement tracking
        """
        axis = self.resolve_axis_name(axis_name)
        if axis is None:
            return
        poll_rate = rate if rate is not None else self.poll_rate

        def poller(dt):
            if self._is_shutting_down:
                return False
            if not self.uobject or not self.uobject.is_valid():
                return False

            v = self.uobject.get_input_axis(axis)

            if abs(v) < deadzone:
                v = 0.0

            last = self._last_axis_values.get(axis)
            if last != v:
                self._last_axis_values[axis] = v
                if v != 0:  # Only callback if non-zero
                    callback(v)

            return True

        ticker = ue.add_ticker(poller, poll_rate)
        self._pollers.append(ticker)
        self._register_binding((axis,), "axis_poll", callback.__name__ if hasattr(callback, '__name__') else None)

    def get_input_axis(self, axis):
        """Get current value of an axis"""
        return self.uobject.get_input_axis(axis)

    def bind_input_axis(self, axis, callback):
        """Bind an input axis directly (alternative method)"""
        self.uobject.bind_input_axis(axis, callback)

    def bind_axis_for_sequence(self, axis_name, condition_fn, callback):
        """Internal: bind axis for sequence detection"""
        axis = self.resolve_axis_name(axis_name)
        if axis is None:
            return

        def _handler(v):
            if condition_fn(v):
                callback(v)

        self.uobject.bind_axis(axis, _handler)

    # Actions
    def bind_action(self, name, pressed_cb=None, released_cb=None):
        """Bind an action defined in project input settings"""
        action = self.resolve_action_name(name)
        if action is None:
            return
        if pressed_cb:
            self.uobject.bind_action(action, ue.IE_PRESSED, pressed_cb)
        if released_cb:
            self.uobject.bind_action(action, ue.IE_RELEASED, released_cb)
        self._register_binding((action,), "action", pressed_cb.__name__ if pressed_cb and hasattr(pressed_cb, '__name__') else None)

    def is_action_pressed(self, name):
        """Check if action is currently pressed"""
        return self.uobject.is_action_pressed(name)

    def is_action_released(self, name):
        """Check if action is currently released"""
        return self.uobject.is_action_released(name)

    def get_engine_defined_action_mappings(self):
        """Get list of engine-defined action mappings"""
        return ue.get_engine_defined_action_mappings()

    # Key State
    def was_pressed(self, key):
        """Check if key was just pressed this frame"""
        return self.player_controller.WasInputKeyJustPressed(key)

    def was_released(self, key):
        """Check if key was just released this frame"""
        return self.player_controller.WasInputKeyJustReleased(key)

    # Mouse
    def get_mouse_position(self, deproject=False):
        """Get mouse position in screen coordinates
        If deproject=True, also returns world position and direction
        Returns: (x, y) or (x, y, world_pos, world_dir) if deproject=True
        """
        ok, x, y = self.player_controller.GetMousePosition()
        if not ok:
            return None

        if deproject:
            success, world, direction = self.player_controller.DeprojectScreenPositionToWorld(x, y)
            if success:
                return x, y, world, direction

        return x, y

    def set_mouse_position(self, x, y):
        """Set mouse position in screen coordinates"""
        self.player_controller.SetMouseLocation(x, y)

    def deproject_mouse(self):
        """Get world position and direction from current mouse position
        Returns: (success, world_pos, world_dir)
        """
        success, world_pos, world_dir = self.player_controller.DeprojectMousePositionToWorld()
        return success, world_pos, world_dir

    # Mouse Delta (Timer)
    def log_mouse_delta_timer(self, rate=0.05):
        """Start logging mouse delta at specified rate"""

        def tick():
            if self._is_shutting_down:
                return
            dx, dy = self.player_controller.GetInputMouseDelta()
            if dx or dy:
                ue.log(f"MouseDelta {dx:.3f}, {dy:.3f}")

        self.uobject.set_timer(rate, tick, True)


# Binding doc generator
#
# rebuild_generated_modules() in unreal_engine_tools.py invokes this to write
# a Markdown index of every input binding in the codebase. The output file is
# chmod'd read-only so a stale hand-edit can't drift from the source.

_NATIVE_KEY_EVENT = {"bind_key", "bind_chord_event"}
_HM_KEY_EVENT = {"bind_press", "bind_release", "bind_double_click",
                 "bind_repeat", "bind_poll"}
_BIND_AXIS = {"bind_axis", "bind_axis_poll", "bind_input_axis"}
_BIND_ACTION = {"bind_action"}
_BIND_SEQUENCE = {"bind_sequence"}
_KEY_CHECK = {"is_input_key_down", "is_key_down", "is_chord_down",
              "was_pressed", "was_released",
              "WasInputKeyJustPressed", "WasInputKeyJustReleased"}
_ALL_BIND_NAMES = (_NATIVE_KEY_EVENT | _HM_KEY_EVENT | _BIND_AXIS
                   | _BIND_ACTION | _BIND_SEQUENCE | _KEY_CHECK)

_MOUSE_TOKENS = {
    "leftmousebutton", "rightmousebutton", "middlemousebutton",
    "thumbmousebutton", "thumbmousebutton2",
    "mousex", "mousey", "mouse2d",
    "mousescrollup", "mousescrolldown", "mousewheelaxis",
}

_SCAN_SKIP_DIRS = {"__pycache__", "unreal_engine"}
_SCAN_SKIP_FILES = {"input_devices.py", "gen_cli.py"}


def _is_mouse_token(token):
    if not token:
        return False
    for piece in str(token).split("+"):
        if _clean(piece) in _MOUSE_TOKENS:
            return True
    return False


def _ast_literal_key(node):
    """Return the literal string from a key/chord/axis arg, or None for dynamic."""
    import ast
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.List):
        parts = []
        for el in node.elts:
            if isinstance(el, ast.Constant) and isinstance(el.value, str):
                parts.append(el.value)
            else:
                parts.append("<dynamic>")
        return " -> ".join(parts) if parts else None
    return None


def _ast_unparse(node):
    import ast
    try:
        return ast.unparse(node).strip()
    except Exception:
        return f"<{type(node).__name__}>"


def _ast_extract_call(method, args, keywords):
    """Return (key_node, callback_node) for a binding call."""
    if not args:
        return None, None
    key_node = args[0]
    cb = None
    if method in _NATIVE_KEY_EVENT:
        # bind_key(key, event, callback) / bind_chord_event(chord, event, callback)
        if len(args) > 2:
            cb = args[2]
    elif method in _BIND_ACTION:
        if len(args) >= 3:
            # native: bind_action(name, event, callback)
            cb = args[2]
        else:
            # HotkeyManager: bind_action(name, pressed_cb=, released_cb=)
            for kw in keywords:
                if kw.arg in ("pressed_cb", "released_cb", "callback"):
                    cb = kw.value
                    break
    elif method in (_HM_KEY_EVENT | _BIND_AXIS | _BIND_SEQUENCE):
        if len(args) > 1:
            cb = args[1]
        else:
            for kw in keywords:
                if kw.arg in ("callback", "cb"):
                    cb = kw.value
                    break
    return key_node, cb


def _ast_find_purpose(tree, callback_node):
    """Find a one-line purpose string for *callback_node* by looking up its
    function definition in *tree* and returning its first docstring line."""
    import ast
    if callback_node is None:
        return ""
    if isinstance(callback_node, ast.Lambda):
        body = _ast_unparse(callback_node.body)
        return f"lambda: {body}" if body else "lambda"
    name = None
    if isinstance(callback_node, ast.Attribute):
        name = callback_node.attr
    elif isinstance(callback_node, ast.Name):
        name = callback_node.id
    if not name:
        return ""
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            doc = ast.get_docstring(n)
            if doc:
                return doc.splitlines()[0].strip()
            return ""
    return ""


def _md_cell(s):
    if s is None:
        s = ""
    s = s.replace("|", r"\|").replace("\n", " ").strip()
    return s or "—"


def generate_input_bindings_doc(scripts_dir=None, output_path=None):
    """Scan the Scripts tree for input bindings and write a read-only Markdown index.

    Walks every .py file under *scripts_dir* (skipping __pycache__,
    unreal_engine/ stubs, and the binding-defining files themselves) and
    collects each call to:

        Native UE   : bind_key, bind_axis, bind_action, bind_input_axis,
                      is_input_key_down, WasInputKeyJustPressed,
                      WasInputKeyJustReleased
        HotkeyManager: bind_press, bind_release, bind_double_click,
                       bind_repeat, bind_poll, bind_chord_event,
                       bind_sequence, bind_axis, bind_axis_poll,
                       bind_action, is_key_down, is_chord_down,
                       was_pressed, was_released

    Each call site contributes a row recording the key/chord/axis/action,
    the bound callback, the callback's first docstring line if available,
    and the file:line. The output is chmod'd read-only so a hand-edit
    can't drift from source — regenerate via rebuild_generated_modules().
    """
    import ast
    import os
    import stat
    from datetime import datetime, timezone

    if scripts_dir is None:
        scripts_dir = os.path.join(os.path.abspath(ue.get_content_dir()), "Scripts")
    if output_path is None:
        output_path = os.path.join(scripts_dir, "input_bindings.md")

    bind_rows, check_rows, files_scanned, parse_errors = scan_input_bindings(scripts_dir)
    _write_input_bindings_md(output_path, bind_rows, check_rows, files_scanned, parse_errors)


def scan_input_bindings(scripts_dir):
    """AST-scan *scripts_dir* for binding calls.

    Returns (bind_rows, check_rows, files_scanned, parse_errors), where each
    row is a dict with key/method/callback/purpose/location/category.
    Shared by generate_input_bindings_doc() and generate_keyboard_guide_image().
    """
    import ast
    import os

    files_scanned = 0
    parse_errors = []
    bind_rows = []
    check_rows = []

    for root, dirs, files in os.walk(scripts_dir):
        dirs[:] = [d for d in dirs if d not in _SCAN_SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            if fname in _SCAN_SKIP_FILES:
                continue
            full = os.path.join(root, fname)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    src = f.read()
            except Exception as e:
                parse_errors.append((full, str(e)))
                continue
            try:
                tree = ast.parse(src, filename=full)
            except SyntaxError as e:
                parse_errors.append((full, f"SyntaxError: {e}"))
                continue
            files_scanned += 1

            rel = os.path.relpath(full, scripts_dir).replace("\\", "/")

            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                method = None
                if isinstance(node.func, ast.Attribute):
                    method = node.func.attr
                elif isinstance(node.func, ast.Name):
                    method = node.func.id
                if method not in _ALL_BIND_NAMES:
                    continue

                key_node, cb_node = _ast_extract_call(method, node.args, node.keywords)
                key_str = _ast_literal_key(key_node) if key_node is not None else None
                if key_str is None:
                    # Non-literal key: render the source expression with an
                    # <expr> marker so it's clearly distinguishable from a
                    # literal key in the output.
                    if key_node is None:
                        key_str = "<no-arg>"
                    else:
                        key_str = f"<expr: {_ast_unparse(key_node)}>"
                callback = _ast_unparse(cb_node) if cb_node is not None else "—"
                purpose = _ast_find_purpose(tree, cb_node)

                if method in _BIND_AXIS:
                    category = "axis"
                elif method in _BIND_ACTION:
                    category = "action"
                elif method in _BIND_SEQUENCE:
                    category = "sequence"
                elif method in _KEY_CHECK:
                    category = "check"
                else:
                    category = "mouse" if _is_mouse_token(key_str) else "key"

                row = {
                    "key": key_str,
                    "method": method,
                    "callback": callback,
                    "purpose": purpose,
                    "location": f"{rel}:{node.lineno}",
                    "category": category,
                }
                if category == "check":
                    check_rows.append(row)
                else:
                    bind_rows.append(row)

    bind_rows.sort(key=lambda r: (r["category"], r["key"].lower(), r["location"]))
    check_rows.sort(key=lambda r: (r["key"].lower(), r["location"]))
    return bind_rows, check_rows, files_scanned, parse_errors


def _write_input_bindings_md(output_path, bind_rows, check_rows, files_scanned, parse_errors):
    import os
    import stat
    from datetime import datetime, timezone

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    section_titles = [
        ("key",      "Keyboard / Chord Bindings"),
        ("mouse",    "Mouse Bindings"),
        ("axis",     "Axis Bindings"),
        ("action",   "Action Bindings"),
        ("sequence", "Sequence Bindings"),
    ]

    lines = []
    lines.append("# Input Bindings (auto-generated)")
    lines.append("")
    lines.append(f"_Generated at {generated_at}_")
    lines.append("")
    lines.append("This file is regenerated by `input_devices.generate_input_bindings_doc()` "
                 "from `unreal_engine_tools.rebuild_generated_modules()`. "
                 "**Do not edit by hand** — the file is set read-only and any local edits "
                 "will be overwritten on the next rebuild.")
    lines.append("")
    lines.append(f"- Files scanned: **{files_scanned}**")
    lines.append(f"- Bindings found: **{len(bind_rows)}**")
    lines.append(f"- State checks found: **{len(check_rows)}**")
    lines.append("")

    for cat_id, cat_title in section_titles:
        rows = [r for r in bind_rows if r["category"] == cat_id]
        if not rows:
            continue
        first_col = "Name" if cat_id in ("axis", "action", "sequence") else "Key / Chord"
        lines.append(f"## {cat_title}")
        lines.append("")
        lines.append(f"| {first_col} | Method | Callback | Purpose | Location |")
        lines.append("| --- | --- | --- | --- | --- |")
        for r in rows:
            lines.append(
                f"| `{_md_cell(r['key'])}` "
                f"| `{_md_cell(r['method'])}` "
                f"| `{_md_cell(r['callback'])}` "
                f"| {_md_cell(r['purpose'])} "
                f"| {_md_cell(r['location'])} |"
            )
        lines.append("")

    if check_rows:
        lines.append("## Key State Checks (non-binding)")
        lines.append("")
        lines.append("Read-only queries — these check whether a key is currently down or was "
                     "just pressed/released, but don't bind a callback.")
        lines.append("")
        lines.append("| Key | Method | Location |")
        lines.append("| --- | --- | --- |")
        for r in check_rows:
            lines.append(
                f"| `{_md_cell(r['key'])}` "
                f"| `{_md_cell(r['method'])}` "
                f"| {_md_cell(r['location'])} |"
            )
        lines.append("")

    if parse_errors:
        lines.append("## Files Skipped Due to Parse Errors")
        lines.append("")
        for path, err in parse_errors:
            lines.append(f"- `{os.path.basename(path)}`: {err}")
        lines.append("")

    content = "\n".join(lines)

    # Clear read-only bit if the file already exists, write fresh content,
    # then re-apply read-only. Windows honors only S_IWRITE/S_IREAD.
    if os.path.exists(output_path):
        try:
            os.chmod(output_path, stat.S_IWRITE | stat.S_IREAD)
        except OSError:
            pass
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    try:
        os.chmod(output_path, stat.S_IREAD)
    except OSError:
        pass

    print(f"Generated {output_path} "
          f"({files_scanned} files scanned, "
          f"{len(bind_rows)} bindings, {len(check_rows)} checks)")
    return output_path


# Keyboard shortcut guide image
#
# generate_keyboard_guide_image() draws one of the saved Keyboard layouts
# (keyboard_razerblade152019, keyboard_ANSI, keyboard_wootingtwohe, ...) with
# every bound key highlighted, plus a Windows-Shortcut-Guide-style legend of
# "key tiles -> what it does", grouped by where the binding lives.
#
# Sources, in order:
#   1. scan_input_bindings()       - HotkeyManager / native UE bind_* calls
#   2. Config/DefaultInput.ini     - real keys behind each bound axis/action
#   3. _GUIDE_MANUAL_BINDINGS      - shortcuts polled via Win32 (Text3D), which
#                                    the AST scan can't see. Keep in sync by hand.

_GUIDE_CONTEXTS = {
    "main.py": "Global",
    "pypawn_drone.py": "Drone",
    "pyactor_stickman.py": "StickMan",
    "gizmo_edit_mode.py": "Gizmo",
    "pyactor_gizmo.py": "Gizmo",
    "pyactor_text3d.py": "Text editing",
    "pyactor_text3d_executor.py": "Code cells",
}

# (alternative chords, description, context). Chords use "+" between keys.
_GUIDE_MANUAL_BINDINGS = [
    (["Ctrl+Enter", "Shift+Enter"], "Run the focused code cell", "Code cells"),
    (["Ctrl+A"], "Select all", "Text editing"),
    (["Ctrl+C"], "Copy", "Text editing"),
    (["Ctrl+X"], "Cut", "Text editing"),
    (["Ctrl+V"], "Paste text or image", "Text editing"),
    (["Ctrl+Tab", "Ctrl+Shift+Tab"], "Next / previous text field", "Text editing"),
    (["Ctrl+Left", "Ctrl+Right"], "Jump by word", "Text editing"),
    (["Ctrl+Home", "Ctrl+End"], "Start / end of text", "Text editing"),
    (["Escape"], "Leave the text field", "Text editing"),
]

_GUIDE_AXIS_LABELS = {
    "MoveForward": ("Move forward", "Move backward"),
    "MoveRight": ("Move right", "Move left"),
    "MoveUp": ("Move up", "Move down"),
    "TurnRate": ("Turn right", "Turn left"),
    "LookUpRate": ("Look up", "Look down"),
    "MouseX": ("Turn left / right", None),
    "MouseY": ("Look up / down", None),
}

_GUIDE_KEY_TEXT = {
    "LeftControl": "Ctrl", "RightControl": "Ctrl", "LeftShift": "Shift", "RightShift": "Shift",
    "LeftAlt": "Alt", "RightAlt": "Alt", "LeftCommand": "Win", "RightCommand": "Win",
    "SpaceBar": "Space", "Escape": "Esc", "BackSpace": "Bksp", "Delete": "Del", "Insert": "Ins",
    "PageUp": "PgUp", "PageDown": "PgDn", "CapsLock": "Caps",
    "Left": "\u2190", "Right": "\u2192", "Up": "\u2191", "Down": "\u2193",
    "Zero": "0", "One": "1", "Two": "2", "Three": "3", "Four": "4",
    "Five": "5", "Six": "6", "Seven": "7", "Eight": "8", "Nine": "9",
    "Hyphen": "-", "Equals": "=", "Comma": ",", "Period": ".", "Slash": "/", "Backslash": "\\",
    "Semicolon": ";", "Apostrophe": "'", "LeftBracket": "[", "RightBracket": "]", "Tilde": "`",
    "LeftMouseButton": "LMB", "RightMouseButton": "RMB", "MiddleMouseButton": "MMB",
    "ThumbMouseButton": "Mouse 4", "ThumbMouseButton2": "Mouse 5",
    "MouseScrollUp": "Scroll \u2191", "MouseScrollDown": "Scroll \u2193",
    "MouseWheelAxis": "Scroll", "MouseX": "Mouse X", "MouseY": "Mouse Y", "Mouse2D": "Mouse",
}

# Legends on the drawn keyboard (layout legend -> face text).
_GUIDE_LEGEND_TEXT = {
    "LeftShift": "Shift", "RightShift": "Shift", "LeftCtrl": "Ctrl", "RightCtrl": "Ctrl",
    "LeftAlt": "Alt", "RightAlt": "Alt", "Space": "", "Backspace": "Backspace",
    "Left": "\u2190", "Right": "\u2192", "Up": "\u2191", "Down": "\u2193", "Delete": "Del",
    **{f"NumPad{w}": str(i) for i, w in enumerate(
        ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"])},
}

# Key widths in key units; everything else is 1u.
_GUIDE_KEY_WIDTHS = {
    "Backspace": 2.0, "Tab": 1.5, "\\": 1.5, "Caps": 1.75, "Enter": 2.25,
    "LeftShift": 2.25, "RightShift": 2.75, "Space": 6.25,
    "LeftCtrl": 1.25, "RightCtrl": 1.25,
}

# Generic modifier names that mean "either side".
_GUIDE_EITHER_SIDE = {
    "ctrl": ("LeftControl", "RightControl"), "control": ("LeftControl", "RightControl"),
    "shift": ("LeftShift", "RightShift"), "alt": ("LeftAlt", "RightAlt"),
    "win": ("LeftCommand", "RightCommand"), "cmd": ("LeftCommand", "RightCommand"),
    "command": ("LeftCommand", "RightCommand"),
}

_GUIDE_MOD_ORDER = {"ctrl": 0, "shift": 1, "alt": 2, "win": 3}


def _guide_canon(kb, token):
    """Token ('Ctrl', 'LeftAlt', 'w', ',') -> tuple of UE key names it covers."""
    t = _clean(str(token))
    if t in _GUIDE_EITHER_SIDE:
        return _GUIDE_EITHER_SIDE[t]
    if t in _MOUSE_TOKENS:
        for k in _GUIDE_KEY_TEXT:
            if _clean(k) == t:
                return (k,)
    ue_key = kb.LEGEND_TO_UE.get(token) or kb.normalize_map.get(t)
    if ue_key == "Win":
        ue_key = "LeftCommand"
    return (ue_key,) if ue_key else ()


def _guide_tile_text(kb, token):
    keys = _guide_canon(kb, token)
    if not keys:
        return str(token)
    return _GUIDE_KEY_TEXT.get(keys[0], keys[0])


def _guide_humanize(callback_src):
    """'self._unless_typing(self.gizmo_mode.toggle)' -> 'Toggle gizmo mode'."""
    import re
    s = (callback_src or "").strip()
    m = re.search(r"\(([\w\.]+)\)\s*$", s)   # unwrap decorators like _unless_typing(fn)
    if m:
        s = m.group(1)
    parts = [p for p in s.split(".") if p not in ("self", "cls")]
    if not parts:
        return ""
    name = parts[-1].strip("_")
    name = re.sub(r"^on_", "", name)
    name = re.sub(r"_(pressed|released|press|release|down|up)$", "", name)
    words = name.replace("_", " ").strip()
    if words in ("toggle", "show", "hide", "open", "close", "start", "stop", "run") and len(parts) > 1:
        words = f"{words} {parts[-2].strip('_').replace('_', ' ')}"
    return words[:1].upper() + words[1:]


def _guide_read_input_ini(scripts_dir):
    """Parse Config/DefaultInput.ini -> (axes, actions).

    axes:    {AxisName: [(key, scale), ...]}
    actions: {ActionName: ["Ctrl+Shift+K", ...]}
    """
    import os
    import re
    path = os.path.normpath(os.path.join(scripts_dir, "..", "..", "Config", "DefaultInput.ini"))
    axes, actions = {}, {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError:
        return axes, actions
    for name, scale, key in re.findall(
            r'^\+AxisMappings=\(AxisName="([^"]+)",Scale=([-\d.]+),Key=(\w+)\)', text, re.M):
        axes.setdefault(name, []).append((key, float(scale)))
    for name, sh, ct, al, cm, key in re.findall(
            r'^\+ActionMappings=\(ActionName="([^"]+)",bShift=(\w+),bCtrl=(\w+),'
            r'bAlt=(\w+),bCmd=(\w+),Key=(\w+)\)', text, re.M):
        mods = [m for m, on in (("Ctrl", ct), ("Shift", sh), ("Alt", al), ("Win", cm)) if on == "True"]
        actions.setdefault(name, []).append("+".join(mods + [key]))
    return axes, actions


def collect_keyboard_guide_entries(scripts_dir, kb=None):
    """Gather every known shortcut as guide entries.

    Each entry: {"chords": [[token, ...], ...], "desc": str, "context": str}
    - one chord list per alternative ("Ctrl+Left or Ctrl+Right").
    """
    import os
    kb = kb or Keyboard()
    bind_rows, _, _, _ = scan_input_bindings(scripts_dir)
    axes, actions = _guide_read_input_ini(scripts_dir)
    known_keys = set(kb.ue_keys) | set(kb.LEGEND_TO_UE.values())

    def ctx_of(location):
        fname = os.path.basename(location.rsplit(":", 1)[0])
        return _GUIDE_CONTEXTS.get(fname, os.path.splitext(fname)[0])

    entries = []
    keyed = {}   # (chord, context) -> {"press": desc, "release": desc}
    for r in bind_rows:
        key, cat, ctx = r["key"], r["category"], ctx_of(r["location"])
        if key.startswith("<"):
            continue   # dynamic key expression - can't be drawn
        desc = r["purpose"] if r["purpose"] and not r["purpose"].startswith("lambda") \
            else _guide_humanize(r["callback"])
        if cat in ("key", "mouse"):
            slot = keyed.setdefault((key, ctx), {})
            kind = "release" if "release" in r["method"] else "press"
            slot.setdefault(kind, desc)
        elif cat == "sequence":
            entries.append({"chords": [[p.strip() for p in key.split("->")]],
                            "desc": desc, "context": ctx, "sequence": True})
        elif cat == "axis":
            pos_label, neg_label = _GUIDE_AXIS_LABELS.get(key, (f"{key} +", f"{key} -"))
            mapped = axes.get(key, [])
            mouse = [k for k, _ in mapped if _is_mouse_token(k)]
            pos = [k for k, s in mapped if s > 0 and k in known_keys and not _is_mouse_token(k)]
            neg = [k for k, s in mapped if s < 0 and k in known_keys and not _is_mouse_token(k)]
            if pos:
                entries.append({"chords": [[k] for k in pos], "desc": pos_label, "context": "Movement"})
            if neg and neg_label:
                entries.append({"chords": [[k] for k in neg], "desc": neg_label, "context": "Movement"})
            if mouse:
                entries.append({"chords": [[k] for k in mouse], "desc": pos_label, "context": "Movement"})
        elif cat == "action":
            chords = actions.get(key, [])
            chords = [c for c in chords if all(_guide_canon(kb, p) for p in c.split("+"))]
            if chords:
                entries.append({"chords": [c.split("+") for c in chords], "desc": desc or key,
                                "context": ctx})

    for (key, ctx), slot in keyed.items():
        if "press" in slot:
            desc = slot["press"]
            if "release" in slot and "hold" not in desc.lower():
                desc += " (hold)"
        else:
            desc = slot["release"] + " (on release)"
        entries.append({"chords": [key.split("+")], "desc": desc, "context": ctx})

    for chords, desc, ctx in _GUIDE_MANUAL_BINDINGS:
        entries.append({"chords": [c.split("+") for c in chords], "desc": desc, "context": ctx})

    # Same chord bound from two files in one context (e.g. gizmo LMB) -> keep one.
    seen, unique = set(), []
    for e in entries:
        sig = (e["context"], tuple(tuple(c) for c in e["chords"]))
        if sig in seen:
            continue
        seen.add(sig)
        unique.append(e)
    return unique


def _guide_font(size, bold=False):
    import os
    from PIL import ImageFont
    fonts_dir = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    names = ["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    for n in names + ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]:
        for p in (os.path.join(fonts_dir, n), n):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _guide_text_size(draw, text, font):
    if not text:
        return 0, 0
    try:
        l, t, r, b = draw.textbbox((0, 0), text, font=font)
        return r - l, b - t
    except AttributeError:   # Pillow < 8
        return font.getsize(text)


def _guide_rrect(draw, box, radius, fill=None, outline=None, width=1):
    try:
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    except AttributeError:   # Pillow < 8.2
        draw.rectangle(box, fill=fill, outline=outline, width=width)


def _guide_fit(draw, text, font, max_w):
    """Trim *text* with an ellipsis until it fits in *max_w* pixels."""
    if _guide_text_size(draw, text, font)[0] <= max_w:
        return text
    while len(text) > 1 and _guide_text_size(draw, text + "\u2026", font)[0] > max_w:
        text = text[:-1]
    return text.rstrip() + "\u2026"


def _guide_wrap(draw, text, font, max_w, max_lines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if _guide_text_size(draw, trial, font)[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1] + " \u2026"
    return [_guide_fit(draw, ln, font, max_w) for ln in lines]


def _guide_layout_rows(rows):
    """Layout rows -> ([[(legend, width_units), ...], ...], total_units), stretched
    so every row matches the most common row width (the widest key flexes)."""
    from collections import Counter
    out = [[(k, _GUIDE_KEY_WIDTHS.get(k, 1.0)) for k in row if k is not None] for row in rows]
    widths = [round(sum(w for _, w in r), 2) for r in out if r]
    if not widths:
        return out, 0
    counts = Counter(widths)
    target = max(counts, key=lambda w: (counts[w], w))
    for r in out:
        diff = target - sum(w for _, w in r)
        if abs(diff) < 1e-6 or not r:
            continue
        i = max(range(len(r)), key=lambda j: (r[j][0] == "Space", r[j][1]))
        if r[i][1] + diff >= 1.0:
            r[i] = (r[i][0], r[i][1] + diff)
    return out, max(sum(w for _, w in r) for r in out)


def generate_keyboard_guide_image(layout="razerblade152019", output_path=None,
                                  scripts_dir=None, title=None, unit=64):
    """Render a shortcut-guide PNG for a saved keyboard layout.

    layout      : name of a saved layout on Keyboard ("razerblade152019",
                  "ANSI", "wootingtwohe") or a list of legend rows.
    output_path : default Scripts/keyboard_guide_<layout>.png
    unit        : pixel size of a 1u key.

    Keys that trigger something are filled blue with a short description on
    the keycap; keys only used as chord modifiers are outlined blue. Below the
    keyboard, every shortcut is listed as key tiles + description, grouped by
    context. Returns the output path.
    """
    import os
    from PIL import Image, ImageDraw

    kb = Keyboard()
    if isinstance(layout, str):
        name = layout
        rows = getattr(kb, f"keyboard_{layout}", None)
        if rows is None:
            saved = [a[len("keyboard_"):] for a in vars(kb)
                     if a.startswith("keyboard_") and not a.endswith("_shift")]
            raise ValueError(f"Unknown keyboard layout {layout!r}; saved layouts: {saved}")
        shift_rows = getattr(kb, f"keyboard_{layout}_shift", None)
    else:
        name, rows, shift_rows = "custom", layout, None

    if scripts_dir is None:
        try:
            scripts_dir = os.path.join(os.path.abspath(ue.get_content_dir()), "Scripts")
        except Exception:
            scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if output_path is None:
        output_path = os.path.join(scripts_dir, f"keyboard_guide_{name}.png")

    entries = collect_keyboard_guide_entries(scripts_dir, kb)

    # Which UE keys are triggers / modifiers, and the first description per key.
    primary_desc, modifier_keys = {}, set()
    for e in entries:
        for chord in e["chords"]:
            for i, tok in enumerate(chord):
                is_primary = e.get("sequence") or i == len(chord) - 1
                for k in _guide_canon(kb, tok):
                    if is_primary:
                        primary_desc.setdefault(k, e["desc"])
                    else:
                        modifier_keys.add(k)

    # Colors (RGBA so the PNG can be overlaid as a texture).
    BG = (14, 14, 16, 238)
    KEY = (44, 44, 48, 255)
    KEY_TEXT = (165, 165, 170, 255)
    ACCENT = (0, 120, 215, 255)
    WHITE = (255, 255, 255, 255)
    DESC = (232, 232, 235, 255)
    HEAD = (130, 185, 245, 255)
    MUTED = (125, 125, 134, 255)
    CAP_TEXT = (222, 236, 252, 255)

    f_title = _guide_font(30, bold=True)
    f_head = _guide_font(19, bold=True)
    f_legend = _guide_font(max(12, unit // 4), bold=True)
    f_shift = _guide_font(max(10, unit // 6))
    f_cap = _guide_font(max(9, unit // 6))
    f_tile = _guide_font(19, bold=True)
    f_desc = _guide_font(20)
    f_or = _guide_font(17)

    scratch = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    pad, gap = 44, max(4, unit // 11)
    title = title or f"Shortcuts \u2014 {name}"

    key_rows, kb_units = _guide_layout_rows(rows)
    kb_w, kb_h = int(kb_units * unit), len(key_rows) * unit

    tile_h, row_h, head_h, sec_gap, col_gap = 40, 50, 44, 18, 48

    def tiles_for(entry):
        """[(text, kind)] where kind is 'tile', 'plus' or 'or'."""
        chords, seq = entry["chords"], entry.get("sequence")
        parts = []
        mods = [tuple(c[:-1]) for c in chords]
        # "Ctrl + <- or ->" when alternatives share the same modifiers.
        if len(chords) > 1 and len(set(mods)) == 1 and mods[0] and not seq:
            for m in mods[0]:
                parts += [(_guide_tile_text(kb, m), "tile"), ("+", "plus")]
            for i, c in enumerate(chords):
                if i:
                    parts.append(("or", "or"))
                parts.append((_guide_tile_text(kb, c[-1]), "tile"))
            return parts
        for i, c in enumerate(chords):
            if i:
                parts.append(("or", "or"))
            if not seq:   # modifiers first, in Ctrl/Shift/Alt/Win order
                c = sorted(c[:-1], key=lambda t: _GUIDE_MOD_ORDER.get(
                    _clean(_guide_tile_text(kb, t)), 9)) + c[-1:]
            for j, tok in enumerate(c):
                if j:
                    parts.append(("\u2192" if seq else "+", "plus"))
                parts.append((_guide_tile_text(kb, tok), "tile"))
        return parts

    def part_w(text, kind):
        if kind == "tile":
            return max(tile_h, _guide_text_size(scratch, text, f_tile)[0] + 22)
        return _guide_text_size(scratch, text, f_or if kind == "or" else f_desc)[0] + 14

    for e in entries:
        e["_parts"] = tiles_for(e)
        e["_tiles_w"] = sum(part_w(t, k) for t, k in e["_parts"])
        e["_desc_w"] = _guide_text_size(scratch, e["desc"], f_desc)[0]

    order = ["Global", "Movement", "Drone", "Gizmo", "Text editing", "Code cells"]
    contexts = sorted({e["context"] for e in entries},
                      key=lambda c: (order.index(c) if c in order else len(order), c))
    sections = [(c, [e for e in entries if e["context"] == c]) for c in contexts]

    ncols = 3 if len(entries) > 10 else max(1, min(2, len(sections)))

    # Flow whole sections into columns, aiming for even heights.
    def sec_height(items):
        return head_h + len(items) * row_h + sec_gap
    target_h = sum(sec_height(i) for _, i in sections) / ncols
    columns, cur_h = [[]], 0
    for sec in sections:
        h = sec_height(sec[1])
        if columns[-1] and cur_h + h / 2 > target_h and len(columns) < ncols:
            columns.append([])
            cur_h = 0
        columns[-1].append(sec)
        cur_h += h
    list_h = max((sum(sec_height(i) for _, i in col) for col in columns), default=0)

    # Each column is as wide as its own tiles + descriptions; spare width
    # (when the keyboard is wider than the list) goes into the gaps.
    col_tiles, col_ws = [], []
    for col in columns:
        items = [e for _, sec_items in col for e in sec_items]
        tw = max((e["_tiles_w"] for e in items), default=0)
        dw = max((e["_desc_w"] for e in items), default=0)
        col_tiles.append(tw)
        col_ws.append(max(tw + 18 + min(dw, 420),
                          max(_guide_text_size(scratch, s.upper(), f_head)[0] for s, _ in col)))
    list_w = sum(col_ws) + (len(columns) - 1) * col_gap
    img_w = max(kb_w + 2 * pad, list_w + 2 * pad)
    if len(columns) > 1:
        col_gap = (img_w - 2 * pad - sum(col_ws)) / (len(columns) - 1)

    title_h = 64
    img_h = pad + title_h + kb_h + 40 + list_h + pad - sec_gap
    img = Image.new("RGBA", (img_w, img_h), BG)
    d = ImageDraw.Draw(img)

    # Title + color legend
    d.text((pad, pad - 6), title, font=f_title, fill=WHITE)
    lx = img_w - pad
    for label, fill, outline in (("Modifier", KEY, ACCENT), ("Bound key", ACCENT, None)):
        lx -= _guide_text_size(d, label, f_or)[0]
        d.text((lx, pad + 2), label, font=f_or, fill=DESC)
        lx -= 30
        _guide_rrect(d, (lx, pad + 3, lx + 22, pad + 25), 4, fill=fill, outline=outline, width=2)
        lx -= 28

    # Keyboard
    kx0, ky0 = (img_w - kb_w) // 2, pad + title_h
    for r, row in enumerate(key_rows):
        shift_row = None
        if shift_rows and r < len(shift_rows):
            shift_row = [k for k in shift_rows[r] if k is not None]
            if len(shift_row) != len(row):
                shift_row = None
        x = kx0
        for i, (legend, wu) in enumerate(row):
            w = int(round(wu * unit))
            box = (x + gap // 2, ky0 + r * unit + gap // 2,
                   x + w - gap // 2, ky0 + (r + 1) * unit - gap // 2)
            x += w
            canon = _guide_canon(kb, legend) if legend else ()
            ue_key = canon[0] if canon else None
            bound = ue_key in primary_desc
            is_mod = ue_key in modifier_keys and not bound
            _guide_rrect(d, box, max(4, unit // 10), fill=ACCENT if bound else KEY,
                         outline=ACCENT if is_mod else None, width=3 if is_mod else 1)

            face = _GUIDE_LEGEND_TEXT.get(legend, legend or "")
            if len(face) == 1 and face.isalpha():
                face = face.upper()
            fg = WHITE if (bound or is_mod) else KEY_TEXT
            bx0, by0, bx1, by1 = box
            if bound:
                # Legend top-left, description along the bottom of the cap.
                d.text((bx0 + 7, by0 + 2), face, font=f_legend, fill=fg)
                lh = _guide_text_size(d, "Ag", f_cap)[1] + 3
                lines = _guide_wrap(d, primary_desc[ue_key], f_cap, bx1 - bx0 - 10, 2)
                for li, line in enumerate(lines):
                    d.text((bx0 + 5, by1 - 6 - lh * (len(lines) - li)), line,
                           font=f_cap, fill=CAP_TEXT)
                continue
            tw, th = _guide_text_size(d, face, f_legend)
            shifted = shift_row[i] if shift_row else None
            if shifted and shifted != legend and shifted.upper() != (legend or "").upper():
                d.text((bx0 + 7, by0 + 3), shifted, font=f_shift, fill=MUTED)
                d.text((bx0 + 7, by1 - th - 12), face, font=f_legend, fill=fg)
            else:
                d.text(((bx0 + bx1 - tw) / 2, (by0 + by1 - th) / 2 - 4), face,
                       font=f_legend, fill=fg)

    # Shortcut list
    ly0 = ky0 + kb_h + 40
    cx = pad
    for ci, col in enumerate(columns):
        col_w, tiles_col = col_ws[ci], col_tiles[ci]
        if ci:
            cx += col_ws[ci - 1] + col_gap
        y = ly0
        for sec_name, items in col:
            d.text((cx, y + 4), sec_name.upper(), font=f_head, fill=HEAD)
            d.line((cx, y + head_h - 8, cx + col_w, y + head_h - 8), fill=(62, 62, 68, 255))
            y += head_h
            for e in items:
                x = cx
                for text, kind in e["_parts"]:
                    w = part_w(text, kind)
                    if kind == "tile":
                        _guide_rrect(d, (x, y, x + w, y + tile_h), 4, fill=ACCENT)
                        font, color = f_tile, WHITE
                    else:
                        font = f_or if kind == "or" else f_desc
                        color = MUTED if kind == "or" else DESC
                    tw, th = _guide_text_size(d, text, font)
                    d.text((x + (w - tw) / 2, y + (tile_h - th) / 2 - 5), text, font=font, fill=color)
                    x += w
                dx = cx + tiles_col + 18
                desc = _guide_fit(d, e["desc"], f_desc, cx + col_w - dx)
                d.text((dx, y + 6), desc, font=f_desc, fill=DESC)
                y += row_h
            y += sec_gap

    img.save(output_path)
    print(f"Generated {output_path} ({len(entries)} shortcuts, layout {name})")
    return output_path
