from enum import auto

from typing_extensions import override

from ..misc import utils as utils
from ..misc.enumWithToFromStr import EnumWithToFromStr


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

    def getEmoji(self) -> str | None:
        match self:
            case PokepediaElementType.BUG: return '🐛'
            case PokepediaElementType.DRAGON: return '🐲'
            case PokepediaElementType.ELECTRIC: return '⚡'
            case PokepediaElementType.FIGHTING: return '🥊'
            case PokepediaElementType.FIRE: return '🔥'
            case PokepediaElementType.FLYING: return '🐦'
            case PokepediaElementType.GHOST: return '👻'
            case PokepediaElementType.GRASS: return '🍃'
            case PokepediaElementType.ICE: return '❄'
            case PokepediaElementType.POISON: return '🧪'
            case PokepediaElementType.PSYCHIC: return '🧠'
            case PokepediaElementType.WATER: return '🌊'
            case _: return None

    def getEmojiOrStr(self) -> str:
        emoji = self.getEmoji()

        if utils.isValidStr(emoji):
            return emoji
        else:
            return self.toStr()

    @override
    def toStr(self) -> str:
        return super().toStr().title()
