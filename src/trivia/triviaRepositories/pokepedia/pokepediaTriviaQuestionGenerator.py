import random

from frozenlist import FrozenList

from .booleanPokepediaTriviaQuestion import BooleanPokepediaTriviaQuestion
from .exceptions import UnsupportedPokepediaMoveTriviaQuestionType, UnsupportedPokepediaTriviaQuestionType
from .multipleChoicePokepediaTriviaQuestion import MultipleChoicePokepediaTriviaQuestion
from .pokepediaMoveTriviaQuestionType import PokepediaMoveTriviaQuestionType
from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from .pokepediaTriviaQuestionGeneratorInterface import PokepediaTriviaQuestionGeneratorInterface
from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
from ...settings.triviaSettingsInterface import TriviaSettingsInterface
from ....misc import utils as utils
from ....pkmn.pokepediaDamageClass import PokepediaDamageClass
from ....pkmn.pokepediaElementType import PokepediaElementType
from ....pkmn.pokepediaGeneration import PokepediaGeneration
from ....pkmn.pokepediaMachine import PokepediaMachine
from ....pkmn.pokepediaMachineType import PokepediaMachineType
from ....pkmn.pokepediaMove import PokepediaMove
from ....pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface


class PokepediaTriviaQuestionGenerator(PokepediaTriviaQuestionGeneratorInterface):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        triviaSettings: TriviaSettingsInterface
    ):
        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')

        self.__pokepediaRepository: PokepediaRepositoryInterface = pokepediaRepository
        self.__triviaSettings: TriviaSettingsInterface = triviaSettings

    async def __createMoveIsAvailableAsMachineQuestion(
        self,
        maxGeneration: PokepediaGeneration,
        move: PokepediaMove,
        generationMachines: dict[PokepediaGeneration, list[PokepediaMachine]] | None
    ) -> PokepediaTriviaQuestion:
        randomGeneration = await self.__selectRandomGeneration(
            initialGeneration = move.getInitialGeneration(),
            maxGeneration = maxGeneration
        )

        machinesStrs: list[str] = list()
        for machineType in PokepediaMachineType:
            machinesStrs.append(machineType.toStr())
        machinesStr = '/'.join(machinesStrs)

        return BooleanPokepediaTriviaQuestion(
            correctAnswer = generationMachines is not None and randomGeneration in generationMachines.keys(),
            pokepediaTriviaType = PokepediaTriviaQuestionType.MOVE,
            question = f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via {machinesStr}.',
        )

    async def __createMoveIsAvailableAsWhichMachineQuestion(
        self,
        maxGeneration: PokepediaGeneration,
        move: PokepediaMove,
        generationMachines: dict[PokepediaGeneration, list[PokepediaMachine]]
    ) -> PokepediaTriviaQuestion:
        randomGeneration = await self.__selectRandomGeneration(
            initialGeneration = move.getInitialGeneration(),
            maxGeneration = maxGeneration
        )

        machine = random.choice(generationMachines[randomGeneration])
        correctMachineNumber = machine.machineNumber
        machinePrefix = machine.machineType.toStr()

        falseMachineNumbers = await self.__selectRandomFalseMachineNumbers(
            actualMachineNumber = correctMachineNumber,
            actualMachineType = machine.machineType
        )

        falseMachineNumbersStrs: list[str] = list()

        for falseMachineNumber in falseMachineNumbers:
            falseMachineNumbersStrs.append(f'{machinePrefix}{falseMachineNumber}')

        falseMachineNumbersStrs.sort(key = lambda falseMachineNumber: falseMachineNumber.casefold())
        frozenFalseMachineNumbersStrs: FrozenList[str] = FrozenList(falseMachineNumbersStrs)
        frozenFalseMachineNumbersStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenFalseMachineNumbersStrs,
            pokepediaTriviaType = PokepediaTriviaQuestionType.MOVE,
            correctAnswer = machine.machineName,
            question = f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via which {machinePrefix}?',
        )

    async def __createMoveIsWhichDamageClassQuestion(
        self,
        move: PokepediaMove
    ) -> PokepediaTriviaQuestion:
        damageClassStrs: list[str] = list()

        for damageClass in PokepediaDamageClass:
            damageClassStrs.append(damageClass.toStr())

        damageClassStrs.sort(key = lambda damageClass: damageClass.casefold())
        frozenDamageClassStrs: FrozenList[str] = FrozenList(damageClassStrs)
        frozenDamageClassStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenDamageClassStrs,
            pokepediaTriviaType = PokepediaTriviaQuestionType.MOVE,
            correctAnswer = move.getDamageClass().toStr(),
            question = f'In Pokémon, the move {move.getName()} has which damage class?'
        )

    async def __createMoveQuestion(self, maxGeneration: PokepediaGeneration) -> PokepediaTriviaQuestion:
        move = await self.__pokepediaRepository.fetchRandomMove(
            maxGeneration = maxGeneration
        )

        generationMachines = move.getGenerationMachines()

        if generationMachines is None:
            return await self.__createMoveIsWhichDamageClassQuestion(
                move = move
            )

        moveQuestionType = random.choice(list(PokepediaMoveTriviaQuestionType))

        match moveQuestionType:
            case PokepediaMoveTriviaQuestionType.IS_AVAILABLE_AS_MACHINE:
                return await self.__createMoveIsAvailableAsMachineQuestion(
                    maxGeneration = maxGeneration,
                    move = move,
                    generationMachines = generationMachines
                )

            case PokepediaMoveTriviaQuestionType.IS_AVAILABLE_AS_WHICH_MACHINE:
                return await self.__createMoveIsAvailableAsWhichMachineQuestion(
                    maxGeneration = maxGeneration,
                    move = move,
                    generationMachines = generationMachines
                )

            case PokepediaMoveTriviaQuestionType.IS_WHICH_DAMAGE_CLASS:
                return await self.__createMoveIsWhichDamageClassQuestion(
                    move = move
                )

        raise UnsupportedPokepediaMoveTriviaQuestionType(f'Encountered unsupported PokepediaMoveTriviaQuestionType: ({moveQuestionType=})')

    async def __createPokemonQuestion(self, maxGeneration: PokepediaGeneration) -> PokepediaTriviaQuestion:
        pokemon = await self.__pokepediaRepository.fetchRandomPokemon(
            maxGeneration = maxGeneration
        )

        randomGeneration = await self.__selectRandomGeneration(
            maxGeneration = maxGeneration,
            initialGeneration = pokemon.getInitialGeneration()
        )

        correctTypes = pokemon.getCorrespondingGenerationElementTypes(
            generation = randomGeneration
        )

        correctType = random.choice(correctTypes)

        falseTypes = await self.__selectRandomFalseElementTypes(
            actualTypes = correctTypes
        )

        falseTypesStrs: list[str] = list()

        for falseType in falseTypes:
            falseTypesStrs.append(falseType.toStr())

        falseTypesStrs.sort(key = lambda falseTypeStr: falseTypeStr.casefold())
        frozenFalseTypeStrs: FrozenList[str] = FrozenList(falseTypesStrs)
        frozenFalseTypeStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenFalseTypeStrs,
            correctAnswer = correctType.toStr(),
            pokepediaTriviaType = PokepediaTriviaQuestionType.POKEMON,
            question = f'In Pokémon {randomGeneration.toLongStr()}, {pokemon.getName()} is which of the following types?',
        )

    async def fetchTriviaQuestion(
        self,
        maxGeneration: PokepediaGeneration
    ) -> PokepediaTriviaQuestion:
        if not isinstance(maxGeneration, PokepediaGeneration):
            raise TypeError(f'maxGeneration argument is malformed: \"{maxGeneration}\"')

        pokepediaTriviaQuestionType = random.choice(list(PokepediaTriviaQuestionType))

        match pokepediaTriviaQuestionType:
            case PokepediaTriviaQuestionType.MOVE:
                return await self.__createMoveQuestion(
                    maxGeneration = maxGeneration
                )

            case PokepediaTriviaQuestionType.POKEMON:
                return await self.__createPokemonQuestion(
                    maxGeneration = maxGeneration
                )

        raise UnsupportedPokepediaTriviaQuestionType(f'Encountered unsupported PokepediaTriviaQuestionType: ({pokepediaTriviaQuestionType=})')

    async def __selectRandomFalseElementTypes(
        self,
        actualTypes: list[PokepediaElementType]
    ) -> frozenset[PokepediaElementType]:
        if not isinstance(actualTypes, list) or len(actualTypes) == 0:
            raise TypeError(f'actualTypes argument is malformed: \"{actualTypes}\"')

        allTypes: FrozenList[PokepediaElementType] = FrozenList(PokepediaElementType)
        allTypes.freeze()

        minResponses = await self.__triviaSettings.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettings.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaElementType) - 1)
        responses = random.randint(minResponses, maxResponses)

        falseTypes: set[PokepediaElementType] = set()

        while len(falseTypes) < responses:
            randomType = random.choice(allTypes)

            if randomType not in actualTypes and randomType is not PokepediaElementType.UNKNOWN:
                falseTypes.add(randomType)

        return frozenset(falseTypes)

    async def __selectRandomFalseMachineNumbers(
        self,
        actualMachineNumber: int,
        actualMachineType: PokepediaMachineType
    ) -> frozenset[int]:
        if not utils.isValidInt(actualMachineNumber):
            raise TypeError(f'actualMachineNumber argument is malformed: \"{actualMachineNumber}\"')
        elif not isinstance(actualMachineType, PokepediaMachineType):
            raise TypeError(f'actualMachineType argument is malformed: \"{actualMachineType}\"')

        minResponses = await self.__triviaSettings.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettings.getMaxMultipleChoiceResponses()
        responses = random.randint(minResponses, maxResponses)
        maxMachineNumber = actualMachineType.getMaxMachineNumber()

        falseMachineNumbers: set[int] = set()

        while len(falseMachineNumbers) < responses:
            randomInt = random.randint(1, maxMachineNumber)

            if randomInt != actualMachineNumber:
                falseMachineNumbers.add(randomInt)

        return frozenset(falseMachineNumbers)

    async def __selectRandomGeneration(
        self,
        initialGeneration: PokepediaGeneration,
        maxGeneration: PokepediaGeneration
    ) -> PokepediaGeneration:
        if not isinstance(initialGeneration, PokepediaGeneration):
            raise TypeError(f'initialGeneration argument is malformed: \"{initialGeneration}\"')
        elif not isinstance(maxGeneration, PokepediaGeneration):
            raise TypeError(f'maxGeneration argument is malformed: \"{maxGeneration}\"')

        allGenerations: FrozenList[PokepediaGeneration] = FrozenList(PokepediaGeneration)
        allGenerations.freeze()

        indexOfMax = allGenerations.index(maxGeneration)
        indexOfMin = allGenerations.index(initialGeneration)

        if indexOfMax < indexOfMin:
            raise RuntimeError(f'indexOfMax ({indexOfMax}) or indexOfMin ({indexOfMin}) is incompatible with an initial generation of {initialGeneration}! ({maxGeneration=})')

        return allGenerations[random.randint(indexOfMin, indexOfMax)]
