from __future__ import annotations
from enum import auto
from typing import Set
from typing_extensions import override

from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType


class PokepediaDamageClass(EnumWithToFromStr):

    PHYSICAL = auto()
    SPECIAL = auto()
    STATUS = auto()

    # gen 1-3 have damage classes based off element type
    @classmethod
    def getTypeBasedDamageClass(cls, elementType: PokepediaElementType):
        assert isinstance(elementType, PokepediaElementType), f"malformed {elementType=}"

        physicalElementTypes: Set[PokepediaElementType] = {
            PokepediaElementType.BUG, PokepediaElementType.FIGHTING, PokepediaElementType.FLYING,
            PokepediaElementType.GHOST, PokepediaElementType.GROUND, PokepediaElementType.NORMAL,
            PokepediaElementType.POISON, PokepediaElementType.ROCK, PokepediaElementType.STEEL
        }

        specialElementTypes: Set[PokepediaElementType] = {
            PokepediaElementType.DARK, PokepediaElementType.DRAGON, PokepediaElementType.ELECTRIC,
            PokepediaElementType.FIRE, PokepediaElementType.GRASS, PokepediaElementType.ICE,
            PokepediaElementType.PSYCHIC, PokepediaElementType.WATER
        }

        if elementType in physicalElementTypes:
            return PokepediaDamageClass.PHYSICAL
        elif elementType in specialElementTypes:
            return PokepediaDamageClass.SPECIAL
        else:
            raise ValueError(f'unknown PokepediaElementType: \"{elementType}\"')

    @override
    def toStr(self) -> str:
        return super().toStr().title()
