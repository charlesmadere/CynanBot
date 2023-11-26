from enum import Enum, auto

import CynanBot.misc.utils as utils


class PokepediaBerryFlavor(Enum):

    BITTER = auto()
    DRY = auto()
    SOUR = auto()
    SPICY = auto()
    SWEET = auto()

    @classmethod
    def fromInt(cls, number: int):
        if not utils.isValidInt(number):
            raise ValueError(f'number argument is malformed: \"{number}\"')

        for berryFlavor in PokepediaBerryFlavor:
            if berryFlavor.getBerryFlavorId() == number:
                return berryFlavor

        raise ValueError(f'number argument does not match any PokepediaBerryFlavor: {number}')

    def getBerryFlavorId(self) -> int:
        if self is PokepediaBerryFlavor.BITTER:
            return 4
        elif self is PokepediaBerryFlavor.DRY:
            return 2
        elif self is PokepediaBerryFlavor.SOUR:
            return 5
        elif self is PokepediaBerryFlavor.SPICY:
            return 1
        elif self is PokepediaBerryFlavor.SWEET:
            return 3
        else:
            raise RuntimeError(f'unknown PokepediaBerryFlavor: \"{self}\"')

    def toStr(self) -> str:
        if self is PokepediaBerryFlavor.BITTER:
            return 'Bitter'
        elif self is PokepediaBerryFlavor.DRY:
            return 'Dry'
        elif self is PokepediaBerryFlavor.SOUR:
            return 'Sour'
        elif self is PokepediaBerryFlavor.SPICY:
            return 'Spicy'
        elif self is PokepediaBerryFlavor.SWEET:
            return 'Sweet'
        else:
            raise RuntimeError(f'unknown PokepediaBerryFlavor: \"{self}\"')
