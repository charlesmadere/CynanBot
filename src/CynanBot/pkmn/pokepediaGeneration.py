from __future__ import annotations

from enum import Enum, auto
from typing import Any

import CynanBot.misc.utils as utils


class PokepediaGeneration(Enum):

    GENERATION_1 = auto()
    GENERATION_2 = auto()
    GENERATION_3 = auto()
    GENERATION_4 = auto()
    GENERATION_5 = auto()
    GENERATION_6 = auto()
    GENERATION_7 = auto()
    GENERATION_8 = auto()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, PokepediaGeneration):
            return self is other
        else:
            raise ValueError(f'`other` is an unsupported type: \"{other}\"')

    @classmethod
    def fromMoveId(cls, moveId: int) -> PokepediaGeneration:
        if not utils.isValidInt(moveId):
            raise TypeError(f'moveId argument is malformed: \"{moveId}\"')
        elif moveId < 0 or moveId > utils.getIntMaxSafeSize():
            raise ValueError(f'moveId argument is out of bounds: {moveId}')

        if moveId <= PokepediaGeneration.GENERATION_1.getMaxMoveId():
            return PokepediaGeneration.GENERATION_1
        elif moveId <= PokepediaGeneration.GENERATION_2.getMaxMoveId():
            return PokepediaGeneration.GENERATION_2
        elif moveId <= PokepediaGeneration.GENERATION_3.getMaxMoveId():
            return PokepediaGeneration.GENERATION_3
        elif moveId <= PokepediaGeneration.GENERATION_4.getMaxMoveId():
            return PokepediaGeneration.GENERATION_4
        elif moveId <= PokepediaGeneration.GENERATION_5.getMaxMoveId():
            return PokepediaGeneration.GENERATION_5
        elif moveId <= PokepediaGeneration.GENERATION_6.getMaxMoveId():
            return PokepediaGeneration.GENERATION_6
        elif moveId <= PokepediaGeneration.GENERATION_7.getMaxMoveId():
            return PokepediaGeneration.GENERATION_7
        else:
            return PokepediaGeneration.GENERATION_8

    @classmethod
    def fromPokedexId(cls, pokedexId: int) -> PokepediaGeneration:
        if not utils.isValidInt(pokedexId):
            raise TypeError(f'pokedexId argument is malformed: \"{pokedexId}\"')
        elif pokedexId < 0 or pokedexId > utils.getIntMaxSafeSize():
            raise ValueError(f'pokedexId argument is out of bounds: {pokedexId}')

        if pokedexId <= PokepediaGeneration.GENERATION_1.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_1
        elif pokedexId <= PokepediaGeneration.GENERATION_2.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_2
        elif pokedexId <= PokepediaGeneration.GENERATION_3.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_3
        elif pokedexId <= PokepediaGeneration.GENERATION_4.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_4
        elif pokedexId <= PokepediaGeneration.GENERATION_5.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_5
        elif pokedexId <= PokepediaGeneration.GENERATION_6.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_6
        elif pokedexId <= PokepediaGeneration.GENERATION_7.getMaxPokedexId():
            return PokepediaGeneration.GENERATION_7
        else:
            return PokepediaGeneration.GENERATION_8

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text in ('red', 'blue', 'red-blue', 'yellow', 'green', 'generation-i'):
            return PokepediaGeneration.GENERATION_1
        elif text in ('gold', 'silver', 'gold-silver', 'crystal', 'generation-ii'):
            return PokepediaGeneration.GENERATION_2
        elif text in ('ruby', 'sapphire', 'ruby-sapphire', 'emerald', 'firered', 'leafgreen', 'firered-leafgreen', 'colosseum', 'xd', 'generation-iii'):
            return PokepediaGeneration.GENERATION_3
        elif text in ('diamond', 'pearl', 'diamond-pearl', 'platinum', 'heartgold', 'soulsilver', 'heartgold-soulsilver', 'generation-iv'):
            return PokepediaGeneration.GENERATION_4
        elif text in ('black', 'white', 'black-white', 'black-2', 'white-2', 'black-2-white-2', 'generation-v'):
            return PokepediaGeneration.GENERATION_5
        elif text in ('x', 'y', 'x-y', 'omega-ruby', 'alpha-sapphire', 'omega-ruby-alpha-sapphire', 'generation-vi'):
            return PokepediaGeneration.GENERATION_6
        elif text in ('sun', 'moon', 'sun-moon', 'ultra-sun', 'ultra-moon', 'ultra-sun-ultra-moon', 'lets-go-eevee', 'lets-go-pikachu', 'lets-go-pikachu-lets-go-eevee', 'generation-vii'):
            return PokepediaGeneration.GENERATION_7
        elif text in ('sword', 'shield', 'sword-shield', 'brilliant-diamond', 'shining-pearl', 'brilliant-diamond-shining-pearl', 'the-isle-of-armor', 'the-crown-tundra', 'legends-arceus', 'generation-viii'):
            return PokepediaGeneration.GENERATION_8
        else:
            raise ValueError(f'unknown PokepediaGeneration: \"{text}\"')

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, PokepediaGeneration):
            all = list(PokepediaGeneration)
            return all.index(self) >= all.index(other)
        else:
            raise ValueError(f'`other` is an unsupported type: \"{other}\"')

    def getId(self) -> int:
        if self is PokepediaGeneration.GENERATION_1:
            return 1
        elif self is PokepediaGeneration.GENERATION_2:
            return 2
        elif self is PokepediaGeneration.GENERATION_3:
            return 3
        elif self is PokepediaGeneration.GENERATION_4:
            return 4
        elif self is PokepediaGeneration.GENERATION_5:
            return 5
        elif self is PokepediaGeneration.GENERATION_6:
            return 6
        elif self is PokepediaGeneration.GENERATION_7:
            return 7
        elif self is PokepediaGeneration.GENERATION_8:
            return 8
        else:
            raise RuntimeError(f'unknown PokepediaGeneration: \"{self}\"')

    def getMaxMoveId(self) -> int:
        if self is PokepediaGeneration.GENERATION_1:
            return 165
        elif self is PokepediaGeneration.GENERATION_2:
            return 251
        elif self is PokepediaGeneration.GENERATION_3:
            return 354
        elif self is PokepediaGeneration.GENERATION_4:
            return 467
        elif self is PokepediaGeneration.GENERATION_5:
            return 559
        elif self is PokepediaGeneration.GENERATION_6:
            return 621
        elif self is PokepediaGeneration.GENERATION_7:
            return 742
        elif self is PokepediaGeneration.GENERATION_8:
            return 826
        else:
            raise RuntimeError(f'unknown PokepediaGeneration: \"{self}\"')

    def getMaxPokedexId(self) -> int:
        if self is PokepediaGeneration.GENERATION_1:
            return 151
        elif self is PokepediaGeneration.GENERATION_2:
            return 251
        elif self is PokepediaGeneration.GENERATION_3:
            return 386
        elif self is PokepediaGeneration.GENERATION_4:
            return 493
        elif self is PokepediaGeneration.GENERATION_5:
            return 649
        elif self is PokepediaGeneration.GENERATION_6:
            return 721
        elif self is PokepediaGeneration.GENERATION_7:
            return 809
        elif self is PokepediaGeneration.GENERATION_8:
            return 905
        else:
            raise RuntimeError(f'unknown PokepediaGeneration: \"{self}\"')

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, PokepediaGeneration):
            all = list(PokepediaGeneration)
            return all.index(self) > all.index(other)
        else:
            raise ValueError(f'`other` is an unsupported type: \"{other}\"')

    def __hash__(self) -> int:
        all = list(PokepediaGeneration)
        return all.index(self)

    def isEarlyGeneration(self) -> bool:
        return self is PokepediaGeneration.GENERATION_1 or self is PokepediaGeneration.GENERATION_2 or self is PokepediaGeneration.GENERATION_3

    def __le__(self, other: Any) -> bool:
        if isinstance(other, PokepediaGeneration):
            all = list(PokepediaGeneration)
            return all.index(self) <= all.index(other)
        else:
            raise ValueError(f'`other` is an unsupported type: \"{other}\"')

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, PokepediaGeneration):
            all = list(PokepediaGeneration)
            return all.index(self) < all.index(other)
        else:
            raise ValueError(f'`other` is an unsupported type: \"{other}\"')

    def toLongStr(self) -> str:
        if self is PokepediaGeneration.GENERATION_1:
            return 'generation 1'
        elif self is PokepediaGeneration.GENERATION_2:
            return 'generation 2'
        elif self is PokepediaGeneration.GENERATION_3:
            return 'generation 3'
        elif self is PokepediaGeneration.GENERATION_4:
            return 'generation 4'
        elif self is PokepediaGeneration.GENERATION_5:
            return 'generation 5'
        elif self is PokepediaGeneration.GENERATION_6:
            return 'generation 6'
        elif self is PokepediaGeneration.GENERATION_7:
            return 'generation 7'
        elif self is PokepediaGeneration.GENERATION_8:
            return 'generation 8'
        else:
            raise RuntimeError(f'unknown PokepediaGeneration: \"{self}\"')

    def toShortStr(self) -> str:
        if self is PokepediaGeneration.GENERATION_1:
            return 'G1'
        elif self is PokepediaGeneration.GENERATION_2:
            return 'G2'
        elif self is PokepediaGeneration.GENERATION_3:
            return 'G3'
        elif self is PokepediaGeneration.GENERATION_4:
            return 'G4'
        elif self is PokepediaGeneration.GENERATION_5:
            return 'G5'
        elif self is PokepediaGeneration.GENERATION_6:
            return 'G6'
        elif self is PokepediaGeneration.GENERATION_7:
            return 'G7'
        elif self is PokepediaGeneration.GENERATION_8:
            return 'G8'
        else:
            raise RuntimeError(f'unknown PokepediaGeneration: \"{self}\"')
