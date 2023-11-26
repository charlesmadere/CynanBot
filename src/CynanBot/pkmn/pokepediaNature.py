from enum import Enum, auto
from typing import Optional

import misc.utils as utils
from pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


class PokepediaNature(Enum):

    ADAMANT = auto()
    BASHFUL = auto()
    BOLD = auto()
    BRAVE = auto()
    CALM = auto()
    CAREFUL = auto()
    DOCILE = auto()
    GENTLE = auto()
    HARDY = auto()
    HASTY = auto()
    IMPISH = auto()
    JOLLY = auto()
    LAX = auto()
    LONELY = auto()
    MILD = auto()
    MODEST = auto()
    NAIVE = auto()
    NAUGHTY = auto()
    QUIET = auto()
    QUIRKY = auto()
    RASH = auto()
    RELAXED = auto()
    SASSY = auto()
    SERIOUS = auto()
    TIMID = auto()

    @classmethod
    def fromInt(cls, number: int):
        if not utils.isValidInt(number):
            raise ValueError(f'number argument is malformed: \"{number}\"')

        for nature in PokepediaNature:
            if nature.getNatureId() == number:
                return nature

        raise ValueError(f'number argument does not match any PokepediaNature: {number}')

    def getHatesFlavor(self) -> Optional[PokepediaBerryFlavor]:
        if self is PokepediaNature.HARDY:
            return None
        elif self is PokepediaNature.LONELY:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.BRAVE:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.ADAMANT:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.NAUGHTY:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.BOLD:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.DOCILE:
            return None
        elif self is PokepediaNature.RELAXED:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.IMPISH:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.LAX:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.TIMID:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.HASTY:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.SERIOUS:
            return None
        elif self is PokepediaNature.JOLLY:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.NAIVE:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.MODEST:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.MILD:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.QUIET:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.BASHFUL:
            return None
        elif self is PokepediaNature.RASH:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.CALM:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.GENTLE:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.SASSY:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.CAREFUL:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.QUIRKY:
            return None
        else:
            raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def getLikesFlavor(self) -> Optional[PokepediaBerryFlavor]:
        if self is PokepediaNature.HARDY:
            return None
        elif self is PokepediaNature.LONELY:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.BRAVE:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.ADAMANT:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.NAUGHTY:
            return PokepediaBerryFlavor.SPICY
        elif self is PokepediaNature.BOLD:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.DOCILE:
            return None
        elif self is PokepediaNature.RELAXED:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.IMPISH:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.LAX:
            return PokepediaBerryFlavor.SOUR
        elif self is PokepediaNature.TIMID:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.HASTY:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.SERIOUS:
            return None
        elif self is PokepediaNature.JOLLY:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.NAIVE:
            return PokepediaBerryFlavor.SWEET
        elif self is PokepediaNature.MODEST:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.MILD:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.QUIET:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.BASHFUL:
            return None
        elif self is PokepediaNature.RASH:
            return PokepediaBerryFlavor.DRY
        elif self is PokepediaNature.CALM:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.GENTLE:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.SASSY:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.CAREFUL:
            return PokepediaBerryFlavor.BITTER
        elif self is PokepediaNature.QUIRKY:
            return None
        else:
            raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def getNatureId(self) -> int:
        if self is PokepediaNature.HARDY:
            return 1
        elif self is PokepediaNature.LONELY:
            return 2
        elif self is PokepediaNature.BRAVE:
            return 3
        elif self is PokepediaNature.ADAMANT:
            return 4
        elif self is PokepediaNature.NAUGHTY:
            return 5
        elif self is PokepediaNature.BOLD:
            return 6
        elif self is PokepediaNature.DOCILE:
            return 7
        elif self is PokepediaNature.RELAXED:
            return 8
        elif self is PokepediaNature.IMPISH:
            return 9
        elif self is PokepediaNature.LAX:
            return 10
        elif self is PokepediaNature.TIMID:
            return 11
        elif self is PokepediaNature.HASTY:
            return 12
        elif self is PokepediaNature.SERIOUS:
            return 13
        elif self is PokepediaNature.JOLLY:
            return 14
        elif self is PokepediaNature.NAIVE:
            return 15
        elif self is PokepediaNature.MODEST:
            return 16
        elif self is PokepediaNature.MILD:
            return 17
        elif self is PokepediaNature.QUIET:
            return 18
        elif self is PokepediaNature.BASHFUL:
            return 19
        elif self is PokepediaNature.RASH:
            return 20
        elif self is PokepediaNature.CALM:
            return 21
        elif self is PokepediaNature.GENTLE:
            return 22
        elif self is PokepediaNature.SASSY:
            return 23
        elif self is PokepediaNature.CAREFUL:
            return 24
        elif self is PokepediaNature.QUIRKY:
            return 25
        else:
            raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def toStr(self) -> str:
        if self is PokepediaNature.HARDY:
            return 'Hardy'
        elif self is PokepediaNature.LONELY:
            return 'Lonely'
        elif self is PokepediaNature.BRAVE:
            return 'Brave'
        elif self is PokepediaNature.ADAMANT:
            return 'Adamant'
        elif self is PokepediaNature.NAUGHTY:
            return 'Naughty'
        elif self is PokepediaNature.BOLD:
            return 'Bold'
        elif self is PokepediaNature.DOCILE:
            return 'Docile'
        elif self is PokepediaNature.RELAXED:
            return 'Relaxed'
        elif self is PokepediaNature.IMPISH:
            return 'Impish'
        elif self is PokepediaNature.LAX:
            return 'Lax'
        elif self is PokepediaNature.TIMID:
            return 'Timid'
        elif self is PokepediaNature.HASTY:
            return 'Hasty'
        elif self is PokepediaNature.SERIOUS:
            return 'Serious'
        elif self is PokepediaNature.JOLLY:
            return 'Jolly'
        elif self is PokepediaNature.NAIVE:
            return 'Naive'
        elif self is PokepediaNature.MODEST:
            return 'Modest'
        elif self is PokepediaNature.MILD:
            return 'Mild'
        elif self is PokepediaNature.QUIET:
            return 'Quiet'
        elif self is PokepediaNature.BASHFUL:
            return 'Bashful'
        elif self is PokepediaNature.RASH:
            return 'Rash'
        elif self is PokepediaNature.CALM:
            return 'Calm'
        elif self is PokepediaNature.GENTLE:
            return 'Gentle'
        elif self is PokepediaNature.SASSY:
            return 'Sassy'
        elif self is PokepediaNature.CAREFUL:
            return 'Careful'
        elif self is PokepediaNature.QUIRKY:
            return 'Quirky'
        else:
            raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')
