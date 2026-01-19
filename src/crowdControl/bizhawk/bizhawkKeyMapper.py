from typing import Any, Final

from .bizhawkKey import BizhawkKey
from .bizhawkKeyMapperInterface import BizhawkKeyMapperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class BizhawkKeyMapper(BizhawkKeyMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Final[TimberInterface] = timber

    async def fromString(self, string: str | Any | None) -> BizhawkKey | None:
        if not utils.isValidStr(string):
            return None

        string = string.lower()

        match string:
            case 'a': return BizhawkKey.A
            case 'arrow_down': return BizhawkKey.ARROW_DOWN
            case 'arrow_left': return BizhawkKey.ARROW_LEFT
            case 'arrow_right': return BizhawkKey.ARROW_RIGHT
            case 'arrow_up': return BizhawkKey.ARROW_UP
            case 'b': return BizhawkKey.B
            case 'c': return BizhawkKey.C
            case 'd': return BizhawkKey.D
            case 'e': return BizhawkKey.E
            case 'enter': return BizhawkKey.ENTER
            case 'esc': return BizhawkKey.ESC
            case 'f1': return BizhawkKey.F1
            case 'f2': return BizhawkKey.F2
            case 'f3': return BizhawkKey.F3
            case 'f4': return BizhawkKey.F4
            case 'f5': return BizhawkKey.F5
            case 'f6': return BizhawkKey.F6
            case 'f7': return BizhawkKey.F7
            case 'f8': return BizhawkKey.F8
            case 'f9': return BizhawkKey.F9
            case 'f10': return BizhawkKey.F10
            case 'f11': return BizhawkKey.F11
            case 'f12': return BizhawkKey.F12
            case 'f13': return BizhawkKey.F13
            case 'f14': return BizhawkKey.F14
            case 'f15': return BizhawkKey.F15
            case 's': return BizhawkKey.S
            case 'space': return BizhawkKey.SPACE
            case 'w': return BizhawkKey.W
            case 'x': return BizhawkKey.X
            case 'y': return BizhawkKey.Y
            case 'z': return BizhawkKey.Z
            case _:
                self.__timber.log('BizhawkKeyMapper', f'Encountered unknown BizhawkKey value: \"{string}\"')
                return None

    async def toString(self, bizhawkKey: BizhawkKey) -> str:
        if not isinstance(bizhawkKey, BizhawkKey):
            raise TypeError(f'bizhawkKey argument is malformed: \"{bizhawkKey}\"')

        match bizhawkKey:
            case BizhawkKey.A: return 'a'
            case BizhawkKey.ARROW_DOWN: return 'arrow_down'
            case BizhawkKey.ARROW_LEFT: return 'arrow_left'
            case BizhawkKey.ARROW_RIGHT: return 'arrow_right'
            case BizhawkKey.ARROW_UP: return 'arrow_up'
            case BizhawkKey.B: return 'b'
            case BizhawkKey.C: return 'c'
            case BizhawkKey.D: return 'd'
            case BizhawkKey.E: return 'e'
            case BizhawkKey.ENTER: return 'enter'
            case BizhawkKey.ESC: return 'esc'
            case BizhawkKey.F1: return 'f1'
            case BizhawkKey.F2: return 'f2'
            case BizhawkKey.F3: return 'f3'
            case BizhawkKey.F4: return 'f4'
            case BizhawkKey.F5: return 'f5'
            case BizhawkKey.F6: return 'f6'
            case BizhawkKey.F7: return 'f7'
            case BizhawkKey.F8: return 'f8'
            case BizhawkKey.F9: return 'f9'
            case BizhawkKey.F10: return 'f10'
            case BizhawkKey.F11: return 'f11'
            case BizhawkKey.F12: return 'f12'
            case BizhawkKey.F13: return 'f13'
            case BizhawkKey.F14: return 'f14'
            case BizhawkKey.F15: return 'f15'
            case BizhawkKey.S: return 's'
            case BizhawkKey.SPACE: return 'space'
            case BizhawkKey.W: return 'w'
            case BizhawkKey.X: return 'x'
            case BizhawkKey.Y: return 'y'
            case BizhawkKey.Z: return 'z'
            case _: raise ValueError(f'Encountered unknown BizhawkKey value: \"{bizhawkKey}\"')
