import locale
from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.pkmn.pokepediaDamageMultiplier import PokepediaDamageMultiplier
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBot.pkmn.pokepediaTypeChart import PokepediaTypeChart


class PokepediaPokemon():

    def __init__(
        self,
        generationElementTypes: Dict[PokepediaGeneration, List[PokepediaElementType]],
        initialGeneration: PokepediaGeneration,
        height: int,
        pokedexId: int,
        weight: int,
        name: str
    ):
        if not utils.hasItems(generationElementTypes):
            raise ValueError(f'generationElementTypes argument is malformed: \"{generationElementTypes}\"')
        assert isinstance(initialGeneration, PokepediaGeneration), f"malformed {initialGeneration=}"
        if not utils.isValidNum(height):
            raise ValueError(f'height argument is malformed: \"{height}\"')
        if not utils.isValidNum(pokedexId):
            raise ValueError(f'pokedexId argument is malformed: \"{pokedexId}\"')
        if not utils.isValidNum(weight):
            raise ValueError(f'weight argument is malformed: \"{weight}\"')
        if not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')

        self.__generationElementTypes: Dict[PokepediaGeneration, List[PokepediaElementType]] = generationElementTypes
        self.__initialGeneration: PokepediaGeneration = initialGeneration
        self.__height: int = height
        self.__pokedexId: int = pokedexId
        self.__weight: int = weight
        self.__name: str = name

    def __buildGenerationElementTypesWeaknessesAndResistancesStr(
        self,
        weaknessesAndResistances: Dict[PokepediaDamageMultiplier, List[PokepediaElementType]],
        damageMultiplier: PokepediaDamageMultiplier,
        delimiter: str
    ) -> Optional[str]:
        if not utils.hasItems(weaknessesAndResistances):
            raise ValueError(f'weaknessesAndResistances argument is malformed: \"{weaknessesAndResistances}\"')
        assert isinstance(damageMultiplier, PokepediaDamageMultiplier), f"malformed {damageMultiplier=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        if damageMultiplier not in weaknessesAndResistances or not utils.hasItems(weaknessesAndResistances[damageMultiplier]):
            return None

        elementTypesStrings: List[str] = list()
        for elementType in weaknessesAndResistances[damageMultiplier]:
            elementTypesStrings.append(elementType.getEmojiOrStr().lower())

        elementTypesString = delimiter.join(elementTypesStrings)
        return f'{damageMultiplier.toStr()} {damageMultiplier.getEffectDescription()} {elementTypesString}.'

    def getCorrespondingGenerationElementTypes(
        self,
        generation: PokepediaGeneration
    ) -> List[PokepediaElementType]:
        assert isinstance(generation, PokepediaGeneration), f"malformed {generation=}"

        allGenerations = list(PokepediaGeneration)
        index = allGenerations.index(generation)

        while index >= 0:
            if allGenerations[index] in self.__generationElementTypes:
                return self.__generationElementTypes[allGenerations[index]]

            index = index - 1

        raise KeyError(f'No corresponding generation element types for \"{generation}\"!')

    def getGenerationElementTypes(self) -> Dict[PokepediaGeneration, List[PokepediaElementType]]:
        return self.__generationElementTypes

    def getHeight(self) -> int:
        return self.__height

    def getHeightStr(self) -> str:
        return locale.format_string("%d", self.__height, grouping = True)

    def getInitialGeneration(self) -> PokepediaGeneration:
        return self.__initialGeneration

    def getName(self) -> str:
        return self.__name

    def getPokedexId(self) -> int:
        return self.__pokedexId

    def getPokedexIdStr(self) -> str:
        return locale.format_string("%d", self.__pokedexId, grouping = True)

    def getWeight(self) -> int:
        return self.__weight

    def getWeightStr(self) -> str:
        return locale.format_string("%d", self.__weight, grouping = True)

    def toStrList(self, delimiter: str = ', ') -> List[str]:
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        strings: List[str] = list()
        strings.append(f'{self.__name} (#{self.getPokedexIdStr()}) — introduced in {self.__initialGeneration.toShortStr()}, weight is {self.getWeightStr()} and height is {self.getHeightStr()}.')

        for gen in PokepediaGeneration:
            if gen in self.__generationElementTypes:
                genElementTypes = self.__generationElementTypes[gen]

                genElementTypesStrings: List[str] = list()
                for genElementType in genElementTypes:
                    genElementTypesStrings.append(genElementType.toStr().lower())

                genElementTypesString = delimiter.join(genElementTypesStrings)
                message = f'{gen.toShortStr()} ({genElementTypesString}):'

                typeChart = PokepediaTypeChart.fromPokepediaGeneration(gen)
                weaknessesAndResistances = typeChart.getWeaknessesAndResistancesFor(genElementTypes)

                for damageMultiplier in PokepediaDamageMultiplier:
                    if damageMultiplier is PokepediaDamageMultiplier.ONE:
                        continue

                    damageMultiplierMessage = self.__buildGenerationElementTypesWeaknessesAndResistancesStr(
                        weaknessesAndResistances = weaknessesAndResistances,
                        damageMultiplier = damageMultiplier,
                        delimiter = delimiter
                    )

                    if utils.isValidStr(damageMultiplierMessage):
                        message = f'{message} {damageMultiplierMessage}'

                strings.append(message)

        return strings
