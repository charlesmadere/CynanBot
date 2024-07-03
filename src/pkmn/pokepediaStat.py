from __future__ import annotations

from enum import Enum, auto

from .pokepediaNature import PokepediaNature
from ..misc import utils as utils


class PokepediaStat(Enum):

    ACCURACY = auto()
    ATTACK = auto()
    DEFENSE = auto()
    EVASION = auto()
    HP = auto()
    SPECIAL_ATTACK = auto()
    SPECIAL_DEFENSE = auto()
    SPEED = auto()

    @classmethod
    def fromInt(cls, number: int) -> PokepediaStat:
        if not utils.isValidInt(number):
            raise TypeError(f'number argument is malformed: \"{number}\"')

        for stat in PokepediaStat:
            if stat.statId == number:
                return stat

        raise ValueError(f'number argument does not match any PokepediaStat: {number}')

    @property
    def decreasingNatures(self) -> set[PokepediaNature] | None:
        if self is PokepediaStat.HP:
            return None
        elif self is PokepediaStat.ATTACK:
            return { PokepediaNature.BOLD, PokepediaNature.CALM, PokepediaNature.MODEST, PokepediaNature.TIMID }
        elif self is PokepediaStat.DEFENSE:
            return { PokepediaNature.GENTLE, PokepediaNature.HASTY, PokepediaNature.LONELY, PokepediaNature.MILD }
        elif self is PokepediaStat.SPECIAL_ATTACK:
            return { PokepediaNature.CAREFUL, PokepediaNature.ADAMANT, PokepediaNature.IMPISH, PokepediaNature.JOLLY }
        elif self is PokepediaStat.SPECIAL_DEFENSE:
            return { PokepediaNature.LAX, PokepediaNature.NAIVE, PokepediaNature.NAUGHTY, PokepediaNature.RASH }
        elif self is PokepediaStat.SPEED:
            return { PokepediaNature.BRAVE, PokepediaNature.QUIET, PokepediaNature.RELAXED, PokepediaNature.SASSY }
        elif self is PokepediaStat.ACCURACY:
            return None
        elif self is PokepediaStat.EVASION:
            return None
        else:
            raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')

    @property
    def increasingNatures(self) -> set[PokepediaNature] | None:
        if self is PokepediaStat.HP:
            return None
        elif self is PokepediaStat.ATTACK:
            return { PokepediaNature.ADAMANT, PokepediaNature.BRAVE, PokepediaNature.LONELY, PokepediaNature.NAUGHTY }
        elif self is PokepediaStat.DEFENSE:
            return { PokepediaNature.BOLD, PokepediaNature.IMPISH, PokepediaNature.LAX, PokepediaNature.RELAXED }
        elif self is PokepediaStat.SPECIAL_ATTACK:
            return { PokepediaNature.MODEST, PokepediaNature.MILD, PokepediaNature.QUIET, PokepediaNature.RASH }
        elif self is PokepediaStat.SPECIAL_DEFENSE:
            return { PokepediaNature.CALM, PokepediaNature.CAREFUL, PokepediaNature.GENTLE, PokepediaNature.SASSY }
        elif self is PokepediaStat.SPEED:
            return { PokepediaNature.HASTY, PokepediaNature.JOLLY, PokepediaNature.NAIVE, PokepediaNature.TIMID }
        elif self is PokepediaStat.ACCURACY:
            return None
        elif self is PokepediaStat.EVASION:
            return None
        else:
            raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')

    @property
    def statId(self) -> int:
        match self:
            case PokepediaStat.HP: return 1
            case PokepediaStat.ATTACK: return 2
            case PokepediaStat.DEFENSE: return 3
            case PokepediaStat.SPECIAL_ATTACK: return 4
            case PokepediaStat.SPECIAL_DEFENSE: return 5
            case PokepediaStat.SPEED: return 6
            case PokepediaStat.ACCURACY: return 7
            case PokepediaStat.EVASION: return 8
            case _: raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case PokepediaStat.HP: return 'HP'
            case PokepediaStat.ATTACK: return 'Attack'
            case PokepediaStat.DEFENSE: return 'Defense'
            case PokepediaStat.SPECIAL_ATTACK: return 'Special Attack'
            case PokepediaStat.SPECIAL_DEFENSE: return 'Special Defense'
            case PokepediaStat.SPEED: return 'Speed'
            case PokepediaStat.ACCURACY: return 'Accuracy'
            case PokepediaStat.EVASION: return 'Evasion'
            case _: raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')
