from __future__ import annotations

from enum import Enum, auto

from ..misc import utils as utils


class PokepediaContestType(Enum):

    BEAUTY = auto()
    COOL = auto()
    CUTE = auto()
    SMART = auto()
    TOUGH = auto()

    @classmethod
    def fromStr(cls, text: str | None) -> PokepediaContestType | None:
        if not utils.isValidStr(text):
            return None

        text = text.lower()

        for contestType in PokepediaContestType:
            if contestType.toStr().lower() == text:
                return contestType

        raise ValueError(f'unknown PokepediaContestType: \"{text}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaContestType.BEAUTY: return 'Beauty'
            case PokepediaContestType.COOL: return 'Cool'
            case PokepediaContestType.CUTE: return 'Cute'
            case PokepediaContestType.SMART: return 'Smart'
            case PokepediaContestType.TOUGH: return 'Tough'
            case _: raise RuntimeError(f'unknown PokepediaContestType: \"{self}\"')
