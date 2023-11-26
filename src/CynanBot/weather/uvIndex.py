from enum import Enum, auto

import CynanBot.misc.utils as utils


class UvIndex(Enum):

    LOW = auto()
    MODERATE_TO_HIGH = auto()
    VERY_HIGH_TO_EXTREME = auto()

    @classmethod
    def fromFloat(cls, uvIndex: float):
        if not utils.isValidNum(uvIndex):
            raise ValueError(f'uvIndex argument is malformed: \"{uvIndex}\"')

        if uvIndex <= 2:
            return UvIndex.LOW
        elif uvIndex <= 7:
            return UvIndex.MODERATE_TO_HIGH
        else:
            return UvIndex.VERY_HIGH_TO_EXTREME

    def isNoteworthy(self) -> bool:
        return self is UvIndex.MODERATE_TO_HIGH or self is UvIndex.VERY_HIGH_TO_EXTREME

    def toStr(self) -> str:
        if self is UvIndex.LOW:
            return 'low'
        elif self is UvIndex.MODERATE_TO_HIGH:
            return 'moderate to high'
        elif self is UvIndex.VERY_HIGH_TO_EXTREME:
            return 'very high to extreme'
        else:
            raise RuntimeError(f'unknown UvIndex: \"{self}\"')
