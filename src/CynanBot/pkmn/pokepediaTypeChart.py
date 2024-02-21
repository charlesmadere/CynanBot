from collections import Counter
from enum import Enum, auto
from typing import Dict, List

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaDamageMultiplier import PokepediaDamageMultiplier
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaGeneration import PokepediaGeneration


class PokepediaTypeChart(Enum):

    GENERATION_1 = auto()
    GENERATION_2_THRU_5 = auto()
    GENERATION_6_AND_ON = auto()

    def __buildDictionaryFromWeaknessesAndResistances(
        self,
        noEffect: List[PokepediaElementType],
        resistances: List[PokepediaElementType],
        weaknesses: List[PokepediaElementType]
    ) -> Dict[PokepediaDamageMultiplier, List[PokepediaElementType]]:
        if noEffect is None:
            raise ValueError(f'noEffect argument is malformed: \"{noEffect}\"')
        if resistances is None:
            raise ValueError(f'resistances argument is malformed: \"{resistances}\"')
        if weaknesses is None:
            raise ValueError(f'noEffect argument is malformed: \"{weaknesses}\"')

        for elementType in noEffect:
            while elementType in resistances:
                resistances.remove(elementType)

            while elementType in weaknesses:
                weaknesses.remove(elementType)

        noEffect.sort(key = lambda elementType: elementType.value)

        elementsToFullyRemove: List[PokepediaElementType] = list()
        for elementType in resistances:
            if elementType in weaknesses:
                elementsToFullyRemove.append(elementType)

        for elementToFullyRemove in elementsToFullyRemove:
            while elementToFullyRemove in resistances:
                resistances.remove(elementToFullyRemove)

            while elementToFullyRemove in weaknesses:
                weaknesses.remove(elementToFullyRemove)

        resistances.sort(key = lambda elementType: elementType.value)
        weaknesses.sort(key = lambda elementType: elementType.value)

        dictionary: Dict[PokepediaDamageMultiplier, List[PokepediaElementType]] = dict()

        if utils.hasItems(noEffect):
            dictionary[PokepediaDamageMultiplier.ZERO] = noEffect

        if utils.hasItems(resistances):
            counter = Counter(resistances)
            regularResistances: List[PokepediaElementType] = list()
            doubleResistances: List[PokepediaElementType] = list()

            for elementType in PokepediaElementType:
                if elementType in counter:
                    if counter[elementType] == 1:
                        regularResistances.append(elementType)
                    elif counter[elementType] == 2:
                        doubleResistances.append(elementType)
                    else:
                        raise RuntimeError(f'illegal counter value ({counter[elementType]}) for {elementType}')

            if utils.hasItems(regularResistances):
                dictionary[PokepediaDamageMultiplier.ZERO_POINT_FIVE] = regularResistances

            if utils.hasItems(doubleResistances):
                dictionary[PokepediaDamageMultiplier.ZERO_POINT_TWO_FIVE] = doubleResistances

        if utils.hasItems(weaknesses):
            counter = Counter(weaknesses)
            regularWeaknesses: List[PokepediaElementType] = list()
            doubleWeaknesses: List[PokepediaElementType] = list()

            for elementType in PokepediaElementType:
                if elementType in counter:
                    if counter[elementType] == 1:
                        regularWeaknesses.append(elementType)
                    elif counter[elementType] == 2:
                        doubleWeaknesses.append(elementType)
                    else:
                        raise RuntimeError(f'illegal counter value ({counter[elementType]}) for {elementType}')

            if utils.hasItems(regularWeaknesses):
                dictionary[PokepediaDamageMultiplier.TWO] = regularWeaknesses

            if utils.hasItems(doubleWeaknesses):
                dictionary[PokepediaDamageMultiplier.FOUR] = doubleWeaknesses

        return dictionary

    @classmethod
    def fromPokepediaGeneration(cls, pokepediaGeneration: PokepediaGeneration):
        assert isinstance(pokepediaGeneration, PokepediaGeneration), f"malformed {pokepediaGeneration=}"

        if pokepediaGeneration is PokepediaGeneration.GENERATION_1:
            return PokepediaTypeChart.GENERATION_1
        elif pokepediaGeneration is PokepediaGeneration.GENERATION_2 or pokepediaGeneration is PokepediaGeneration.GENERATION_3 or pokepediaGeneration is PokepediaGeneration.GENERATION_4 or pokepediaGeneration is PokepediaGeneration.GENERATION_5:
            return PokepediaTypeChart.GENERATION_2_THRU_5
        else:
            return PokepediaTypeChart.GENERATION_6_AND_ON

    def __getGenerationOneWeaknessesAndResistancesFor(
        self,
        types: List[PokepediaElementType]
    ) -> Dict[PokepediaDamageMultiplier, List[PokepediaElementType]]:
        if not utils.hasItems(types):
            raise ValueError(f'types argument is malformed: \"{types}\"')

        noEffect: List[PokepediaElementType] = list()
        resistances: List[PokepediaElementType] = list()
        weaknesses: List[PokepediaElementType] = list()

        for elementType in types:
            if elementType is PokepediaElementType.BUG:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.DARK:
                raise ValueError(f'illegal PokepediaElementType for this type chart ({self}): \"{elementType}\"')
            if elementType is PokepediaElementType.DRAGON:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.DRAGON)
                weaknesses.append(PokepediaElementType.ICE)
            elif elementType is PokepediaElementType.ELECTRIC:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.GROUND)
            elif elementType is PokepediaElementType.FAIRY:
                raise ValueError(f'illegal PokepediaElementType for this type chart ({self}): \"{elementType}\"')
            if elementType is PokepediaElementType.FIGHTING:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.FIRE:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.FLYING:
                noEffect.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.GHOST:
                noEffect.append(PokepediaElementType.FIGHTING)
                noEffect.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.GHOST)
            elif elementType is PokepediaElementType.GRASS:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.POISON)
            elif elementType is PokepediaElementType.GROUND:
                noEffect.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.POISON)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.ICE:
                resistances.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.NORMAL:
                noEffect.append(PokepediaElementType.GHOST)
                weaknesses.append(PokepediaElementType.FIGHTING)
            elif elementType is PokepediaElementType.POISON:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.PSYCHIC:
                noEffect.append(PokepediaElementType.GHOST)
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.PSYCHIC)
                weaknesses.append(PokepediaElementType.BUG)
            elif elementType is PokepediaElementType.ROCK:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.STEEL:
                raise ValueError(f'illegal PokepediaElementType for this type chart ({self}): \"{elementType}\"')
            if elementType is PokepediaElementType.UNKNOWN:
                raise ValueError(f'illegal PokepediaElementType for this type chart ({self}): \"{elementType}\"')
            if elementType is PokepediaElementType.WATER:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.GRASS)

        return self.__buildDictionaryFromWeaknessesAndResistances(
            noEffect = noEffect,
            resistances = resistances,
            weaknesses = weaknesses
        )

    def __getGenerationTwoThruFiveWeaknessesAndResistancesFor(
        self,
        types: List[PokepediaElementType]
    ) -> Dict[PokepediaDamageMultiplier, List[PokepediaElementType]]:
        if not utils.hasItems(types):
            raise ValueError(f'types argument is malformed: \"{types}\"')

        noEffect: List[PokepediaElementType] = list()
        resistances: List[PokepediaElementType] = list()
        weaknesses: List[PokepediaElementType] = list()

        for elementType in types:
            if elementType is PokepediaElementType.BUG:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.DARK:
                noEffect.append(PokepediaElementType.PSYCHIC)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.GHOST)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.FIGHTING)
            elif elementType is PokepediaElementType.DRAGON:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.DRAGON)
                weaknesses.append(PokepediaElementType.ICE)
            elif elementType is PokepediaElementType.ELECTRIC:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.GROUND)
            elif elementType is PokepediaElementType.FAIRY:
                raise ValueError(f'illegal PokepediaElementType for this type chart ({self}): \"{elementType}\"')
            if elementType is PokepediaElementType.FIGHTING:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.FIRE:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.FLYING:
                noEffect.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.GHOST:
                noEffect.append(PokepediaElementType.FIGHTING)
                noEffect.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.DARK)
                weaknesses.append(PokepediaElementType.GHOST)
            elif elementType is PokepediaElementType.GRASS:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.POISON)
            elif elementType is PokepediaElementType.GROUND:
                noEffect.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.POISON)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.ICE:
                resistances.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.STEEL)
            elif elementType is PokepediaElementType.NORMAL:
                noEffect.append(PokepediaElementType.GHOST)
                weaknesses.append(PokepediaElementType.FIGHTING)
            elif elementType is PokepediaElementType.POISON:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.PSYCHIC:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.PSYCHIC)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.DARK)
                weaknesses.append(PokepediaElementType.GHOST)
            elif elementType is PokepediaElementType.ROCK:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.STEEL:
                noEffect.append(PokepediaElementType.POISON)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.DRAGON)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.GHOST)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.PSYCHIC)
                resistances.append(PokepediaElementType.ROCK)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.GROUND)
            elif elementType is PokepediaElementType.WATER:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.STEEL)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.GRASS)

        return self.__buildDictionaryFromWeaknessesAndResistances(
            noEffect = noEffect,
            resistances = resistances,
            weaknesses = weaknesses
        )

    def __getGenerationSixAndOnWeaknessesAndResistancesFor(self, types: List[PokepediaElementType]) -> Dict[PokepediaDamageMultiplier, List[PokepediaElementType]]:
        if not utils.hasItems(types):
            raise ValueError(f'types argument is malformed: \"{types}\"')

        noEffect: List[PokepediaElementType] = list()
        resistances: List[PokepediaElementType] = list()
        weaknesses: List[PokepediaElementType] = list()

        for elementType in types:
            if elementType is PokepediaElementType.BUG:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.DARK:
                noEffect.append(PokepediaElementType.PSYCHIC)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.GHOST)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.FIGHTING)
            elif elementType is PokepediaElementType.DRAGON:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.DRAGON)
                weaknesses.append(PokepediaElementType.ICE)
            elif elementType is PokepediaElementType.ELECTRIC:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.GROUND)
            elif elementType is PokepediaElementType.FAIRY:
                noEffect.append(PokepediaElementType.DRAGON)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.STEEL)
            elif elementType is PokepediaElementType.FIGHTING:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.DARK)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.FIRE:
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.FLYING:
                noEffect.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.ROCK)
            elif elementType is PokepediaElementType.GHOST:
                noEffect.append(PokepediaElementType.FIGHTING)
                noEffect.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.DARK)
                weaknesses.append(PokepediaElementType.GHOST)
            elif elementType is PokepediaElementType.GRASS:
                resistances.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.GROUND)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.FLYING)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.POISON)
            elif elementType is PokepediaElementType.GROUND:
                noEffect.append(PokepediaElementType.ELECTRIC)
                resistances.append(PokepediaElementType.POISON)
                resistances.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.ICE:
                resistances.append(PokepediaElementType.ICE)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.ROCK)
                weaknesses.append(PokepediaElementType.STEEL)
            elif elementType is PokepediaElementType.NORMAL:
                noEffect.append(PokepediaElementType.GHOST)
                weaknesses.append(PokepediaElementType.FIGHTING)
            elif elementType is PokepediaElementType.POISON:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.PSYCHIC)
            elif elementType is PokepediaElementType.PSYCHIC:
                resistances.append(PokepediaElementType.FIGHTING)
                resistances.append(PokepediaElementType.PSYCHIC)
                weaknesses.append(PokepediaElementType.BUG)
                weaknesses.append(PokepediaElementType.DARK)
                weaknesses.append(PokepediaElementType.GHOST)
            elif elementType is PokepediaElementType.ROCK:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.POISON)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.GRASS)
                weaknesses.append(PokepediaElementType.GROUND)
                weaknesses.append(PokepediaElementType.WATER)
            elif elementType is PokepediaElementType.STEEL:
                noEffect.append(PokepediaElementType.POISON)
                resistances.append(PokepediaElementType.BUG)
                resistances.append(PokepediaElementType.DRAGON)
                resistances.append(PokepediaElementType.FLYING)
                resistances.append(PokepediaElementType.GRASS)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.NORMAL)
                resistances.append(PokepediaElementType.PSYCHIC)
                resistances.append(PokepediaElementType.ROCK)
                resistances.append(PokepediaElementType.STEEL)
                weaknesses.append(PokepediaElementType.FIGHTING)
                weaknesses.append(PokepediaElementType.FIRE)
                weaknesses.append(PokepediaElementType.GROUND)
            elif elementType is PokepediaElementType.WATER:
                resistances.append(PokepediaElementType.FIRE)
                resistances.append(PokepediaElementType.ICE)
                resistances.append(PokepediaElementType.STEEL)
                resistances.append(PokepediaElementType.WATER)
                weaknesses.append(PokepediaElementType.ELECTRIC)
                weaknesses.append(PokepediaElementType.GRASS)

        return self.__buildDictionaryFromWeaknessesAndResistances(
            noEffect = noEffect,
            resistances = resistances,
            weaknesses = weaknesses
        )

    def getWeaknessesAndResistancesFor(self, types: List[PokepediaElementType]) -> Dict[PokepediaDamageMultiplier, List[PokepediaElementType]]:
        if not utils.hasItems(types):
            raise ValueError(f'types argument is malformed: \"{types}\"')

        if self is PokepediaTypeChart.GENERATION_1:
            return self.__getGenerationOneWeaknessesAndResistancesFor(types)
        elif self is PokepediaTypeChart.GENERATION_2_THRU_5:
            return self.__getGenerationTwoThruFiveWeaknessesAndResistancesFor(types)
        elif self is PokepediaTypeChart.GENERATION_6_AND_ON:
            return self.__getGenerationSixAndOnWeaknessesAndResistancesFor(types)
        else:
            raise RuntimeError(f'unknown PokepediaTypeChart: \"{self}\"')
