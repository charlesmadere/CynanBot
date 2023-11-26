from enum import Enum, auto
from typing import Optional

import misc.utils as utils


class PokepediaElementType(Enum):

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

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'bug':
            return PokepediaElementType.BUG
        elif text == 'dark':
            return PokepediaElementType.DARK
        elif text == 'dragon':
            return PokepediaElementType.DRAGON
        elif text == 'electric':
            return PokepediaElementType.ELECTRIC
        elif text == 'fairy':
            return PokepediaElementType.FAIRY
        elif text == 'fighting':
            return PokepediaElementType.FIGHTING
        elif text == 'fire':
            return PokepediaElementType.FIRE
        elif text == 'flying':
            return PokepediaElementType.FLYING
        elif text == 'ghost':
            return PokepediaElementType.GHOST
        elif text == 'grass':
            return PokepediaElementType.GRASS
        elif text == 'ground':
            return PokepediaElementType.GROUND
        elif text == 'ice':
            return PokepediaElementType.ICE
        elif text == 'normal':
            return PokepediaElementType.NORMAL
        elif text == 'poison':
            return PokepediaElementType.POISON
        elif text == 'psychic':
            return PokepediaElementType.PSYCHIC
        elif text == 'rock':
            return PokepediaElementType.ROCK
        elif text == 'steel':
            return PokepediaElementType.STEEL
        elif text in ('unknown', '???'):
            return PokepediaElementType.UNKNOWN
        elif text == 'water':
            return PokepediaElementType.WATER
        else:
            raise ValueError(f'unknown PokepediaElementType: \"{text}\"')

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

    def toStr(self) -> str:
        if self is PokepediaElementType.BUG:
            return 'Bug'
        elif self is PokepediaElementType.DARK:
            return 'Dark'
        elif self is PokepediaElementType.DRAGON:
            return 'Dragon'
        elif self is PokepediaElementType.ELECTRIC:
            return 'Electric'
        elif self is PokepediaElementType.FAIRY:
            return 'Fairy'
        elif self is PokepediaElementType.FIGHTING:
            return 'Fighting'
        elif self is PokepediaElementType.FIRE:
            return 'Fire'
        elif self is PokepediaElementType.FLYING:
            return 'Flying'
        elif self is PokepediaElementType.GHOST:
            return 'Ghost'
        elif self is PokepediaElementType.GRASS:
            return 'Grass'
        elif self is PokepediaElementType.GROUND:
            return 'Ground'
        elif self is PokepediaElementType.ICE:
            return 'Ice'
        elif self is PokepediaElementType.NORMAL:
            return 'Normal'
        elif self is PokepediaElementType.POISON:
            return 'Poison'
        elif self is PokepediaElementType.PSYCHIC:
            return 'Psychic'
        elif self is PokepediaElementType.ROCK:
            return 'Rock'
        elif self is PokepediaElementType.STEEL:
            return 'Steel'
        elif self is PokepediaElementType.UNKNOWN:
            return 'Unknown'
        elif self is PokepediaElementType.WATER:
            return 'Water'
        else:
            raise RuntimeError(f'unknown PokepediaElementType: \"{self}\"')
