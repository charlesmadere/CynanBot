from typing import Any

from .bizhawkKey import BizhawkKey
from .bizhawkKeyMapperInterface import BizhawkKeyMapperInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class BizhawkKeyMapper(BizhawkKeyMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def fromString(self, string: str | Any | None) -> BizhawkKey | None:
        if not utils.isValidStr(string):
            return None

        string = string.lower()

        match string:
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
            case _:
                self.__timber.log('BizhawkKeyMapper', f'Encountered unknown BizhawkKey value: \"{string}\"')
                return None
