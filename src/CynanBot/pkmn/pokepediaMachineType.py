from enum import Enum, auto

import CynanBot.misc.utils as utils


class PokepediaMachineType(Enum):

    HM = auto()
    TM = auto()
    TR = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text.startswith('hm'):
            return PokepediaMachineType.HM
        elif text.startswith('tm'):
            return PokepediaMachineType.TM
        elif text.startswith('tr'):
            return PokepediaMachineType.TR
        else:
            raise ValueError(f'unknown PokepediaMachineType: \"{text}\"')

    def getMaxMachineNumber(self) -> int:
        if self is PokepediaMachineType.HM:
            return 12
        elif self is PokepediaMachineType.TM:
            return 112
        elif self is PokepediaMachineType.TR:
            return 90
        else:
            raise RuntimeError(f'unknown PokepediaMachineType: \"{self}\"')

    def toStr(self) -> str:
        if self is PokepediaMachineType.HM:
            return 'HM'
        elif self is PokepediaMachineType.TM:
            return 'TM'
        elif self is PokepediaMachineType.TR:
            return 'TR'
        else:
            raise RuntimeError(f'unknown PokepediaMachineType: \"{self}\"')
