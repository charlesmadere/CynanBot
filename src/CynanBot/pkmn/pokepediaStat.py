from enum import Enum, auto

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaNature import PokepediaNature


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
    def fromInt(cls, number: int):
        if not utils.isValidInt(number):
            raise ValueError(f'number argument is malformed: \"{number}\"')

        for stat in PokepediaStat:
            if stat.getStatId() == number:
                return stat

        raise ValueError(f'number argument does not match any PokepediaStat: {number}')

    def getDecreasingNatures(self) -> set[PokepediaNature] | None:
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

    def getIncreasingNatures(self) -> set[PokepediaNature] | None:
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

    def getStatId(self) -> int:
        if self is PokepediaStat.HP:
            return 1
        elif self is PokepediaStat.ATTACK:
            return 2
        elif self is PokepediaStat.DEFENSE:
            return 3
        elif self is PokepediaStat.SPECIAL_ATTACK:
            return 4
        elif self is PokepediaStat.SPECIAL_DEFENSE:
            return 5
        elif self is PokepediaStat.SPEED:
            return 6
        elif self is PokepediaStat.ACCURACY:
            return 7
        elif self is PokepediaStat.EVASION:
            return 8
        else:
            raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')

    def toStr(self) -> str:
        if self is PokepediaStat.HP:
            return 'HP'
        elif self is PokepediaStat.ATTACK:
            return 'Attack'
        elif self is PokepediaStat.DEFENSE:
            return 'Defense'
        elif self is PokepediaStat.SPECIAL_ATTACK:
            return 'Special Attack'
        elif self is PokepediaStat.SPECIAL_DEFENSE:
            return 'Special Defense'
        elif self is PokepediaStat.SPEED:
            return 'Speed'
        elif self is PokepediaStat.ACCURACY:
            return 'Accuracy'
        elif self is PokepediaStat.EVASION:
            return 'Evasion'
        else:
            raise RuntimeError(f'unknown PokepediaStat: \"{self}\"')
