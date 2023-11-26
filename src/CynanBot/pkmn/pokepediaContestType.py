from enum import Enum, auto
from typing import Optional

import CynanBot.misc.utils as utils


class PokepediaContestType(Enum):

    BEAUTY = auto()
    COOL = auto()
    CUTE = auto()
    SMART = auto()
    TOUGH = auto()

    @classmethod
    def fromStr(cls, text: Optional[str]):
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        for contestType in PokepediaContestType:
            if contestType.toStr().lower() == text:
                return contestType

        raise ValueError(f'unknown PokepediaContestType: \"{text}\"')

    def toStr(self) -> str:
        if self is PokepediaContestType.BEAUTY:
            return 'Beauty'
        elif self is PokepediaContestType.COOL:
            return 'Cool'
        elif self is PokepediaContestType.CUTE:
            return 'Cute'
        elif self is PokepediaContestType.SMART:
            return 'Smart'
        elif self is PokepediaContestType.TOUGH:
            return 'Tough'
        else:
            raise RuntimeError(f'unknown PokepediaContestType: \"{self}\"')
