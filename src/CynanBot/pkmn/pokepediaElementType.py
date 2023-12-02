from enum import auto
from typing import Optional

from typing_extensions import override

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr
import CynanBot.misc.utils as utils


class PokepediaElementType(EnumWithToFromStr):

    BUG = auto()
    DARK = auto()
    DRAGON = auto()
    ELECTRIC = auto()
    FAIRY = auto()
    FIGHTING = auto()
    FIRE = auto()
    FLYING = auto()
    GHOST = auto()
    GRASS = auto()
    GROUND = auto()
    ICE = auto()
    NORMAL = auto()
    POISON = auto()
    PSYCHIC = auto()
    ROCK = auto()
    STEEL = auto()
    UNKNOWN = auto()
    WATER = auto()

    @override
    @classmethod
    def fromStr(cls, text: str):
        if text == '???':
            return PokepediaElementType.UNKNOWN
        return super().fromStr(text)

    def getEmoji(self) -> Optional[str]:
        if self is PokepediaElementType.BUG:
            return '🐛'
        elif self is PokepediaElementType.DRAGON:
            return '🐲'
        elif self is PokepediaElementType.ELECTRIC:
            return '⚡'
        elif self is PokepediaElementType.FIGHTING:
            return '🥊'
        elif self is PokepediaElementType.FIRE:
            return '🔥'
        elif self is PokepediaElementType.FLYING:
            return '🐦'
        elif self is PokepediaElementType.GHOST:
            return '👻'
        elif self is PokepediaElementType.GRASS:
            return '🍃'
        elif self is PokepediaElementType.ICE:
            return '❄'
        elif self is PokepediaElementType.POISON:
            return '🧪'
        elif self is PokepediaElementType.PSYCHIC:
            return '🧠'
        elif self is PokepediaElementType.WATER:
            return '🌊'
        else:
            return None

    def getEmojiOrStr(self) -> str:
        emoji = self.getEmoji()

        if utils.isValidStr(emoji):
            return emoji
        else:
            return self.toStr()

    @override
    def toStr(self) -> str:
        return super().toStr().title()
