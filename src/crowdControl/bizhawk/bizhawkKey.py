from enum import Enum, auto


class BizhawkKey(Enum):

    ESC = auto()
    F1 = auto()
    F2 = auto()
    F3 = auto()
    F4 = auto()
    F5 = auto()
    F6 = auto()
    F7 = auto()
    F8 = auto()
    F9 = auto()
    F10 = auto()
    F11 = auto()
    F12 = auto()
    F13 = auto()
    F14 = auto()
    F15 = auto()

    @property
    def intValue(self) -> int:
        # The below key values come from here:
        # https://github.com/AndersMalmgren/FreePIE/blob/master/FreePIE.Core.Plugins/KeyboardPlugin.cs

        match self:
            case BizhawkKey.ESC: return 53
            case BizhawkKey.F1: return 54
            case BizhawkKey.F2: return 55
            case BizhawkKey.F3: return 56
            case BizhawkKey.F4: return 57
            case BizhawkKey.F5: return 58
            case BizhawkKey.F6: return 59
            case BizhawkKey.F7: return 60
            case BizhawkKey.F8: return 61
            case BizhawkKey.F9: return 62
            case BizhawkKey.F10: return 63
            case BizhawkKey.F11: return 64
            case BizhawkKey.F12: return 65
            case BizhawkKey.F13: return 66
            case BizhawkKey.F14: return 67
            case BizhawkKey.F15: return 68
            case _: raise ValueError(f'Unknown BizhawkKey: \"{self}\"')
