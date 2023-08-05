from enum import Enum
from typing import Dict, List


__all__ = [
        "Keys",
        "ALL_KEYS",
        ]


class Keys(str, Enum):
    """
    List of keys for use in key bindings.

    Note that this is an "StrEnum", all values can be compared against
    strings.
    """

    value: str

    Escape = "escape"  # Also Control-[
    ShiftEscape = "s-escape"

    ControlAt = "ctrl-@"  # Also Control-Space.

    ControlA = "ctrl-a"
    ControlB = "ctrl-b"
    ControlC = "ctrl-c"
    ControlD = "ctrl-d"
    ControlE = "ctrl-e"
    ControlF = "ctrl-f"
    ControlG = "ctrl-g"
    ControlH = "ctrl-h"
    ControlI = "ctrl-i"  # Tab
    ControlJ = "ctrl-j"  # Newline
    ControlK = "ctrl-k"
    ControlL = "ctrl-l"
    ControlM = "ctrl-m"  # Carriage return
    ControlN = "ctrl-n"
    ControlO = "ctrl-o"
    ControlP = "ctrl-p"
    ControlQ = "ctrl-q"
    ControlR = "ctrl-r"
    ControlS = "ctrl-s"
    ControlT = "ctrl-t"
    ControlU = "ctrl-u"
    ControlV = "ctrl-v"
    ControlW = "ctrl-w"
    ControlX = "ctrl-x"
    ControlY = "ctrl-y"
    ControlZ = "ctrl-z"

    Control1 = "ctrl-1"
    Control2 = "ctrl-2"
    Control3 = "ctrl-3"
    Control4 = "ctrl-4"
    Control5 = "ctrl-5"
    Control6 = "ctrl-6"
    Control7 = "ctrl-7"
    Control8 = "ctrl-8"
    Control9 = "ctrl-9"
    Control0 = "ctrl-0"

    ControlShift1 = "c-s-1"
    ControlShift2 = "c-s-2"
    ControlShift3 = "c-s-3"
    ControlShift4 = "c-s-4"
    ControlShift5 = "c-s-5"
    ControlShift6 = "c-s-6"
    ControlShift7 = "c-s-7"
    ControlShift8 = "c-s-8"
    ControlShift9 = "c-s-9"
    ControlShift0 = "c-s-0"

    ControlBackslash = "ctrl-\\"
    ControlSquareClose = "ctrl-]"
    ControlCircumflex = "ctrl-^"
    ControlUnderscore = "ctrl-_"

    Left = "left"
    Right = "right"
    Up = "up"
    Down = "down"
    Home = "home"
    End = "end"
    Insert = "insert"
    Delete = "delete"
    PageUp = "pageup"
    PageDown = "pagedown"

    ControlLeft = "ctrl-left"
    ControlRight = "ctrl-right"
    ControlUp = "ctrl-up"
    ControlDown = "ctrl-down"
    ControlHome = "ctrl-home"
    ControlEnd = "ctrl-end"
    ControlInsert = "ctrl-insert"
    ControlDelete = "ctrl-delete"
    ControlPageUp = "ctrl-pageup"
    ControlPageDown = "ctrl-pagedown"

    ShiftLeft = "s-left"
    ShiftRight = "s-right"
    ShiftUp = "s-up"
    ShiftDown = "s-down"
    ShiftHome = "s-home"
    ShiftEnd = "s-end"
    ShiftInsert = "s-insert"
    ShiftDelete = "s-delete"
    ShiftPageUp = "s-pageup"
    ShiftPageDown = "s-pagedown"

    ControlShiftLeft = "c-s-left"
    ControlShiftRight = "c-s-right"
    ControlShiftUp = "c-s-up"
    ControlShiftDown = "c-s-down"
    ControlShiftHome = "c-s-home"
    ControlShiftEnd = "c-s-end"
    ControlShiftInsert = "c-s-insert"
    ControlShiftDelete = "c-s-delete"
    ControlShiftPageUp = "c-s-pageup"
    ControlShiftPageDown = "c-s-pagedown"

    BackTab = "s-tab"  # shift + tab

    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    F13 = "f13"
    F14 = "f14"
    F15 = "f15"
    F16 = "f16"
    F17 = "f17"
    F18 = "f18"
    F19 = "f19"
    F20 = "f20"
    F21 = "f21"
    F22 = "f22"
    F23 = "f23"
    F24 = "f24"

    ControlF1 = "ctrl-f1"
    ControlF2 = "ctrl-f2"
    ControlF3 = "ctrl-f3"
    ControlF4 = "ctrl-f4"
    ControlF5 = "ctrl-f5"
    ControlF6 = "ctrl-f6"
    ControlF7 = "ctrl-f7"
    ControlF8 = "ctrl-f8"
    ControlF9 = "ctrl-f9"
    ControlF10 = "ctrl-f10"
    ControlF11 = "ctrl-f11"
    ControlF12 = "ctrl-f12"
    ControlF13 = "ctrl-f13"
    ControlF14 = "ctrl-f14"
    ControlF15 = "ctrl-f15"
    ControlF16 = "ctrl-f16"
    ControlF17 = "ctrl-f17"
    ControlF18 = "ctrl-f18"
    ControlF19 = "ctrl-f19"
    ControlF20 = "ctrl-f20"
    ControlF21 = "ctrl-f21"
    ControlF22 = "ctrl-f22"
    ControlF23 = "ctrl-f23"
    ControlF24 = "ctrl-f24"

    # Matches any key.
    Any = "<any>"

    # Special.
    ScrollUp = "<scroll-up>"
    ScrollDown = "<scroll-down>"

    CPRResponse = "<cursor-position-response>"
    Vt100MouseEvent = "<vt100-mouse-event>"
    WindowsMouseEvent = "<windows-mouse-event>"
    BracketedPaste = "<bracketed-paste>"

    # For internal use: key which is ignored.
    # (The key binding for this key should not do anything.)
    Ignore = "<ignore>"

    # Some 'Key' aliases (for backwards-compatibility).
    ControlSpace = ControlAt
    Tab = ControlI
    Enter = ControlM
    Backspace = ControlH

    # ShiftControl was renamed to ControlShift in
    # 888fcb6fa4efea0de8333177e1bbc792f3ff3c24 (20 Feb 2020).
    ShiftControlLeft = ControlShiftLeft
    ShiftControlRight = ControlShiftRight
    ShiftControlHome = ControlShiftHome
    ShiftControlEnd = ControlShiftEnd


ALL_KEYS: List[str] = [k.value for k in Keys]


# Aliases.
KEY_ALIASES: Dict[str, str] = {
    "backspace": "ctrl-h",
    "ctrl-space": "ctrl-@",
    "enter": "ctrl-m",
    "tab": "ctrl-i",
    # ShiftControl was renamed to ControlShift.
    "s-c-left": "c-s-left",
    "s-c-right": "c-s-right",
    "s-c-home": "c-s-home",
    "s-c-end": "c-s-end",
}
