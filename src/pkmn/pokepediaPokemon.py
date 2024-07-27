import locale

from .pokepediaDamageMultiplier import PokepediaDamageMultiplier
from .pokepediaElementType import PokepediaElementType
from .pokepediaGeneration import PokepediaGeneration
from .pokepediaTypeChart import PokepediaTypeChart
from ..misc import utils as utils


class PokepediaPokemon:

    def __init__(
        self,
        generationElementTypes: dict[PokepediaGeneration, list[PokepediaElementType]],
        initialGeneration: PokepediaGeneration,
        height: int,
        pokedexId: int,
        weight: int,
        name: str
    ):
        if not isinstance(generationElementTypes, dict):
            raise TypeError(f'generationElementTypes argument is malformed: \"{generationElementTypes}\"')
        elif not isinstance(initialGeneration, PokepediaGeneration):
            raise TypeError(f'initialGeneration argument is malformed: \"{initialGeneration}\"')
        elif not utils.isValidInt(height):
            raise TypeError(f'height argument is malformed: \"{height}\"')
        elif not utils.isValidInt(pokedexId):
            raise TypeError(f'pokedexId argument is malformed: \"{pokedexId}\"')
        elif not utils.isValidInt(weight):
            raise TypeError(f'weight argument is malformed: \"{weight}\"')
        elif not utils.isValidStr(name):
            raise TypeError(f'name argument is malformed: \"{name}\"')

        self.__generationElementTypes: dict[PokepediaGeneration, list[PokepediaElementType]] = generationElementTypes
        self.__initialGeneration: PokepediaGeneration = initialGeneration
        self.__height: int = height
        self.__pokedexId: int = pokedexId
        self.__weight: int = weight
        self.__name: str = name

    def __buildGenerationElementTypesWeaknessesAndResistancesStr(
        self,
        weaknessesAndResistances: dict[PokepediaDamageMultiplier, list[PokepediaElementType]],
        damageMultiplier: PokepediaDamageMultiplier,
        delimiter: str
    ) -> str | None:
        if not isinstance(weaknessesAndResistances, dict):
            raise TypeError(f'weaknessesAndResistances argument is malformed: \"{weaknessesAndResistances}\"')
        elif not isinstance(damageMultiplier, PokepediaDamageMultiplier):
            raise TypeError(f'damageMultiplier argument is malformed: \"{damageMultiplier}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if damageMultiplier not in weaknessesAndResistances or not utils.hasItems(weaknessesAndResistances[damageMultiplier]):
            return None

        elementTypesStrings: list[str] = list()
        for elementType in weaknessesAndResistances[damageMultiplier]:
            elementTypesStrings.append(elementType.getEmojiOrStr().lower())

        elementTypesString = delimiter.join(elementTypesStrings)
        return f'{damageMultiplier.toStr()} {damageMultiplier.getEffectDescription()} {elementTypesString}.'

    def getCorrespondingGenerationElementTypes(
        self,
        generation: PokepediaGeneration
    ) -> list[PokepediaElementType]:
        if not isinstance(generation, PokepediaGeneration):
            raise TypeError(f'generation argument is malformed: \"{generation}\"')

        allGenerations = list(PokepediaGeneration)
        index = allGenerations.index(generation)

        while index >= 0:
            if allGenerations[index] in self.__generationElementTypes:
                return self.__generationElementTypes[allGenerations[index]]

            index = index - 1

        raise KeyError(f'No corresponding generation element types for \"{generation}\"!')

    def getGenerationElementTypes(self) -> dict[PokepediaGeneration, list[PokepediaElementType]]:
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

    def toStrList(self, delimiter: str = ', ') -> list[str]:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        strings: list[str] = list()
        strings.append(f'{self.__name} (#{self.getPokedexIdStr()}) — introduced in {self.__initialGeneration.toShortStr()}, weight is {self.getWeightStr()} and height is {self.getHeightStr()}.')

        for gen in PokepediaGeneration:
            if gen in self.__generationElementTypes:
                genElementTypes = self.__generationElementTypes[gen]

                genElementTypesStrings: list[str] = list()
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
