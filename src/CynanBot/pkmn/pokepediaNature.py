from __future__ import annotations

from enum import Enum, auto

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor


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
    def fromInt(cls, number: int) -> PokepediaNature:
        if not utils.isValidInt(number):
            raise ValueError(f'number argument is malformed: \"{number}\"')

        for nature in PokepediaNature:
            if nature.getNatureId() == number:
                return nature

        raise ValueError(f'number argument does not match any PokepediaNature: {number}')

    def getHatesFlavor(self) -> PokepediaBerryFlavor | None:
        match self:
            case PokepediaNature.HARDY: return None
            case PokepediaNature.LONELY: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.BRAVE: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.ADAMANT: return PokepediaBerryFlavor.DRY
            case PokepediaNature.NAUGHTY: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.BOLD: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.DOCILE: return None
            case PokepediaNature.RELAXED: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.IMPISH: return PokepediaBerryFlavor.DRY
            case PokepediaNature.LAX: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.TIMID: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.HASTY: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.SERIOUS: return None
            case PokepediaNature.JOLLY: return PokepediaBerryFlavor.DRY
            case PokepediaNature.NAIVE: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.MODEST: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.MILD: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.QUIET: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.BASHFUL: return None
            case PokepediaNature.RASH: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.CALM: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.GENTLE: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.SASSY: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.CAREFUL: return PokepediaBerryFlavor.DRY
            case PokepediaNature.QUIRKY: return None
            case _: raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def getLikesFlavor(self) -> PokepediaBerryFlavor | None:
        match self:
            case PokepediaNature.HARDY: return None
            case PokepediaNature.LONELY: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.BRAVE: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.ADAMANT: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.NAUGHTY: return PokepediaBerryFlavor.SPICY
            case PokepediaNature.BOLD: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.DOCILE: return None
            case PokepediaNature.RELAXED: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.IMPISH: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.LAX: return PokepediaBerryFlavor.SOUR
            case PokepediaNature.TIMID: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.HASTY: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.SERIOUS: return None
            case PokepediaNature.JOLLY: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.NAIVE: return PokepediaBerryFlavor.SWEET
            case PokepediaNature.MODEST: return PokepediaBerryFlavor.DRY
            case PokepediaNature.MILD: return PokepediaBerryFlavor.DRY
            case PokepediaNature.QUIET: return PokepediaBerryFlavor.DRY
            case PokepediaNature.BASHFUL: return None
            case PokepediaNature.RASH: return PokepediaBerryFlavor.DRY
            case PokepediaNature.CALM: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.GENTLE: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.SASSY: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.CAREFUL: return PokepediaBerryFlavor.BITTER
            case PokepediaNature.QUIRKY: return None
            case _: raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def getNatureId(self) -> int:
        match self:
            case PokepediaNature.HARDY: return 1
            case PokepediaNature.LONELY: return 2
            case PokepediaNature.BRAVE: return 3
            case PokepediaNature.ADAMANT: return 4
            case PokepediaNature.NAUGHTY: return 5
            case PokepediaNature.BOLD: return 6
            case PokepediaNature.DOCILE: return 7
            case PokepediaNature.RELAXED: return 8
            case PokepediaNature.IMPISH: return 9
            case PokepediaNature.LAX: return 10
            case PokepediaNature.TIMID: return 11
            case PokepediaNature.HASTY: return 12
            case PokepediaNature.SERIOUS: return 13
            case PokepediaNature.JOLLY: return 14
            case PokepediaNature.NAIVE: return 15
            case PokepediaNature.MODEST: return 16
            case PokepediaNature.MILD: return 17
            case PokepediaNature.QUIET: return 18
            case PokepediaNature.BASHFUL: return 19
            case PokepediaNature.RASH: return 20
            case PokepediaNature.CALM: return 21
            case PokepediaNature.GENTLE: return 22
            case PokepediaNature.SASSY: return 23
            case PokepediaNature.CAREFUL: return 24
            case PokepediaNature.QUIRKY: return 25
            case _: raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaNature.HARDY: return 'Hardy'
            case PokepediaNature.LONELY: return 'Lonely'
            case PokepediaNature.BRAVE: return 'Brave'
            case PokepediaNature.ADAMANT: return 'Adamant'
            case PokepediaNature.NAUGHTY: return 'Naughty'
            case PokepediaNature.BOLD: return 'Bold'
            case PokepediaNature.DOCILE: return 'Docile'
            case PokepediaNature.RELAXED: return 'Relaxed'
            case PokepediaNature.IMPISH: return 'Impish'
            case PokepediaNature.LAX: return 'Lax'
            case PokepediaNature.TIMID: return 'Timid'
            case PokepediaNature.HASTY: return 'Hasty'
            case PokepediaNature.SERIOUS: return 'Serious'
            case PokepediaNature.JOLLY: return 'Jolly'
            case PokepediaNature.NAIVE: return 'Naive'
            case PokepediaNature.MODEST: return 'Modest'
            case PokepediaNature.MILD: return 'Mild'
            case PokepediaNature.QUIET: return 'Quiet'
            case PokepediaNature.BASHFUL: return 'Bashful'
            case PokepediaNature.RASH: return 'Rash'
            case PokepediaNature.CALM: return 'Calm'
            case PokepediaNature.GENTLE: return 'Gentle'
            case PokepediaNature.SASSY: return 'Sassy'
            case PokepediaNature.CAREFUL: return 'Careful'
            case PokepediaNature.QUIRKY: return 'Quirky'
            case _: raise RuntimeError(f'unknown PokepediaNature: \"{self}\"')
