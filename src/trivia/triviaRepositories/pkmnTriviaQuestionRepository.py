import random
import traceback
from typing import Any

from ...network.exceptions import GenericNetworkException
from ...pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from ...pkmn.pokepediaContestType import PokepediaContestType
from ...pkmn.pokepediaDamageClass import PokepediaDamageClass
from ...pkmn.pokepediaElementType import PokepediaElementType
from ...pkmn.pokepediaGeneration import PokepediaGeneration
from ...pkmn.pokepediaMachineType import PokepediaMachineType
from ...pkmn.pokepediaMove import PokepediaMove
from ...pkmn.pokepediaNature import PokepediaNature
from ...pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from ...pkmn.pokepediaStat import PokepediaStat
from ...timber.timberInterface import TimberInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (GenericTriviaNetworkException,
                                     MalformedTriviaJsonException,
                                     UnsupportedTriviaTypeException)
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from ..triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ...misc import utils as utils


class PkmnTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        maxGeneration: PokepediaGeneration = PokepediaGeneration.GENERATION_3
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(maxGeneration, PokepediaGeneration):
            raise TypeError(f'maxGeneration argument is malformed: \"{maxGeneration}\"')

        self.__pokepediaRepository: PokepediaRepositoryInterface = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__maxGeneration: PokepediaGeneration = maxGeneration

    async def __createMoveContestTypeQuestion(self, move: PokepediaMove) -> dict[str, Any] | None:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        contestType = move.getContestType()
        if contestType is None:
            return None

        falseContestTypes = await self.__selectRandomFalseContestTypes(contestType)

        falseContestTypeStrs: list[str] = list()
        for falseContestType in falseContestTypes:
            falseContestTypeStrs.append(falseContestType.toStr())

        return {
            'correctAnswer': contestType.toStr(),
            'incorrectAnswers': falseContestTypeStrs,
            'question': f'In Pokémon, what is the contest type of {move.getName()}?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveDamageClassQuestion(self, move: PokepediaMove) -> dict[str, Any]:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        damageClassStrs: list[str] = list()
        for damageClass in PokepediaDamageClass:
            damageClassStrs.append(damageClass.toStr())

        return {
            'correctAnswer': move.getDamageClass().toStr(),
            'incorrectAnswers': damageClassStrs,
            'question': f'In Pokémon, the move {move.getName()} has which damage class?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveIsAvailableAsMachineQuestion(self, move: PokepediaMove) -> dict[str, Any]:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        randomGeneration = await self.__selectRandomGeneration(move.getInitialGeneration())

        machinesStrs: list[str] = list()
        for machineType in PokepediaMachineType:
            machinesStrs.append(machineType.toStr())

        machinesStr = '/'.join(machinesStrs)

        machines = move.getGenerationMachines()

        return {
            'correctAnswer': machines is not None and randomGeneration in machines,
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via {machinesStr}.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def __createMoveIsAvailableAsWhichMachineQuestion(self, move: PokepediaMove) -> dict[str, Any] | None:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        machines = move.getGenerationMachines()

        if machines is None:
            return None

        randomGeneration = await self.__selectRandomGeneration(move.getInitialGeneration())
        machine = machines[randomGeneration][0]
        correctMachineNumber = machine.getMachineNumber()
        machinePrefix = machine.getMachineType().toStr()

        falseMachineNumbers = await self.__selectRandomFalseMachineNumbers(
            actualMachineNumber = correctMachineNumber,
            actualMachineType = machine.getMachineType()
        )

        falseMachineNumbersStrs: list[str] = list()
        for falseMachineNumber in falseMachineNumbers:
            falseMachineNumbersStrs.append(f'{machinePrefix}{falseMachineNumber}')

        return {
            'correctAnswer': machine.getMachineName(),
            'incorrectAnswers': falseMachineNumbersStrs,
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via which {machinePrefix}?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveQuestion(self) -> dict[str, Any]:
        try:
            move = await self.__pokepediaRepository.fetchRandomMove(maxGeneration = self.__maxGeneration)
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: dict[str, Any] | None = None

        while triviaDict is None:
            randomTriviaType = random.randint(0, 3)

            if randomTriviaType == 0:
                triviaDict = await self.__createMoveContestTypeQuestion(move)
            elif randomTriviaType == 1:
                triviaDict = await self.__createMoveDamageClassQuestion(move)
            elif randomTriviaType == 2:
                triviaDict = await self.__createMoveIsAvailableAsMachineQuestion(move)
            elif randomTriviaType == 3:
                triviaDict = await self.__createMoveIsAvailableAsWhichMachineQuestion(move)
            else:
                raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

        return triviaDict

    async def __createNatureQuestion(self) -> dict[str, Any]:
        try:
            nature = await self.__pokepediaRepository.fetchRandomNature()
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: dict[str, Any] | None = None

        while triviaDict is None:
            randomTriviaType = random.randint(0, 1)

            if randomTriviaType == 0:
                triviaDict = await self.__createNatureBerryFlavorQuestion(
                    nature = nature,
                    berryFlavor = nature.getLikesFlavor(),
                    likeOrDislikeStr = 'like'
                )
            elif randomTriviaType == 1:
                triviaDict = await self.__createNatureBerryFlavorQuestion(
                    nature = nature,
                    berryFlavor = nature.getHatesFlavor(),
                    likeOrDislikeStr = 'dislike'
                )
            else:
                raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

        return triviaDict

    async def __createNatureBerryFlavorQuestion(
        self,
        nature: PokepediaNature,
        berryFlavor: PokepediaBerryFlavor | None,
        likeOrDislikeStr: str
    ) -> dict[str, Any]:
        if not isinstance(nature, PokepediaNature):
            raise TypeError(f'nature argument is malformed: \"{nature}\"')
        elif berryFlavor is not None and not isinstance(berryFlavor, PokepediaBerryFlavor):
            raise TypeError(f'berryFlavor argument is malformed: \"{berryFlavor}\"')
        elif not utils.isValidStr(likeOrDislikeStr):
            raise TypeError(f'likeOrDislikeStr argument is malformed: \"{likeOrDislikeStr}\"')

        randomFlavors = await self.__selectRandomFalseBerryFlavors(berryFlavor)

        flavorsStrs: list[str] = list()
        for randomFlavor in randomFlavors:
            flavorsStrs.append(randomFlavor.toStr())

        noneOfThese = 'None of these'
        flavorsStrs.append(noneOfThese)

        correctAnswer = ''
        if berryFlavor is None:
            correctAnswer = noneOfThese
        else:
            correctAnswer = berryFlavor.toStr()

        return {
            'correctAnswer': correctAnswer,
            'incorrectAnswers': flavorsStrs,
            'question': f'Pokémon with the {nature.toStr()} nature {likeOrDislikeStr} ONE of the following flavors.',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createPhysicalOrSpecialDamageClassQuestion(self) -> dict[str, Any]:
        applicableDamageClasses: list[PokepediaDamageClass] = [
            PokepediaDamageClass.PHYSICAL, PokepediaDamageClass.SPECIAL
        ]

        actualDamageClass = random.choice(applicableDamageClasses)

        applicableElementTypes: list[PokepediaElementType] = [
            PokepediaElementType.BUG, PokepediaElementType.DARK, PokepediaElementType.DRAGON,
            PokepediaElementType.ELECTRIC, PokepediaElementType.FIGHTING, PokepediaElementType.FIRE,
            PokepediaElementType.FLYING, PokepediaElementType.GHOST, PokepediaElementType.GRASS,
            PokepediaElementType.GROUND, PokepediaElementType.ICE, PokepediaElementType.NORMAL,
            PokepediaElementType.POISON, PokepediaElementType.PSYCHIC, PokepediaElementType.ROCK,
            PokepediaElementType.STEEL, PokepediaElementType.WATER
        ]

        actualElementType: PokepediaElementType | None = None
        while actualElementType is None or PokepediaDamageClass.getTypeBasedDamageClass(actualElementType) is not actualDamageClass:
            actualElementType = random.choice(applicableElementTypes)

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaElementType) - 1)
        responses = random.randint(minResponses, maxResponses)

        falseElementTypes: set[PokepediaElementType] = set()
        while len(falseElementTypes) < responses:
            falseElementType = random.choice(applicableElementTypes)

            if PokepediaDamageClass.getTypeBasedDamageClass(falseElementType) is not actualDamageClass:
                falseElementTypes.add(falseElementType)

        falseElementTypesStrs: list[str] = list()
        for falseElementType in falseElementTypes:
            falseElementTypesStrs.append(falseElementType.toStr())

        # It reads sort of strangely that the below question specifically mentions only Pokemon
        # generations 1 through 3, however, this is intentional. This is because those generations
        # of Pokemon games had their element types hard-coded to particular damage classes, which
        # is the purpose of this trivia question.

        return {
            'correctAnswer': actualElementType.toStr(),
            'incorrectAnswers': falseElementTypesStrs,
            'question': f'In Pokémon generations 1 through 3, which of the following types has a {actualDamageClass.toStr().lower()} damage class?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createPokemonQuestion(self) -> dict[str, Any]:
        try:
            pokemon = await self.__pokepediaRepository.fetchRandomPokemon(maxGeneration = self.__maxGeneration)
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        randomGeneration = await self.__selectRandomGeneration(pokemon.getInitialGeneration())
        correctTypes = pokemon.getCorrespondingGenerationElementTypes(randomGeneration)
        correctType = random.choice(correctTypes)

        falseTypes = await self.__selectRandomFalseElementTypes(correctTypes)

        falseTypesStrs: list[str] = list()
        for falseType in falseTypes:
            falseTypesStrs.append(falseType.toStr())

        return {
            'correctAnswer': correctType.toStr(),
            'incorrectAnswers': falseTypesStrs,
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {pokemon.getName()} is which of the following types?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createStatOrNatureQuestion(self) -> dict[str, Any]:
        randomTriviaType = random.randint(0, 1)

        if randomTriviaType == 0:
            return await self.__createStatQuestion()
        elif randomTriviaType == 1:
            return await self.__createNatureQuestion()
        else:
            raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

    async def __createStatQuestion(self) -> dict[str, Any]:
        try:
            stat = await self.__pokepediaRepository.fetchRandomStat()
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: dict[str, Any] | None = None

        while triviaDict is None:
            randomTriviaType = random.randint(0, 1)

            if randomTriviaType == 0:
                triviaDict = await self.__createStatDecreasingNaturesQuestion(stat)
            elif randomTriviaType == 1:
                triviaDict = await self.__createStatIncreasingNaturesQuestion(stat)
            else:
                raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

        return triviaDict

    async def __createStatDecreasingNaturesQuestion(self, stat: PokepediaStat) -> dict[str, Any]:
        if not isinstance(stat, PokepediaStat):
            raise TypeError(f'stat argument is malformed: \"{stat}\"')

        decreasingNatures = stat.decreasingNatures
        randomNature = random.choice(list(PokepediaNature))

        return {
            'correctAnswer': decreasingNatures is not None and randomNature in decreasingNatures,
            'question': f'In Pokémon, the {stat.toStr()} stat is negatively impacted by the {randomNature.toStr()} nature.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def __createStatIncreasingNaturesQuestion(self, stat: PokepediaStat) -> dict[str, Any]:
        if not isinstance(stat, PokepediaStat):
            raise TypeError(f'stat argument is malformed: \"{stat}\"')

        increasingNatures = stat.increasingNatures
        randomNature = random.choice(list(PokepediaNature))

        return {
            'correctAnswer': increasingNatures is not None and randomNature in increasingNatures,
            'question': f'In Pokémon, the {stat.toStr()} stat is positively impacted by the {randomNature.toStr()} nature.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('PkmnTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        randomTriviaType = random.randint(0, 6)
        triviaDict: dict[str, Any] | None = None

        if randomTriviaType <= 2:
            triviaDict = await self.__createPokemonQuestion()
        elif randomTriviaType <= 4:
            triviaDict = await self.__createMoveQuestion()
        elif randomTriviaType == 5:
            triviaDict = await self.__createStatOrNatureQuestion()
        elif randomTriviaType == 6:
            triviaDict = await self.__createPhysicalOrSpecialDamageClassQuestion()
        else:
            raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

        if not utils.hasItems(triviaDict):
            raise MalformedTriviaJsonException(f'PkmnTriviaQuestionRepository\'s triviaDict is null/empty: \"{triviaDict}\"!')

        category = 'Pokémon'
        triviaDifficulty = TriviaDifficulty.UNKNOWN
        triviaType: TriviaQuestionType = triviaDict['triviaType']
        question = utils.getStrFromDict(triviaDict, 'question')

        triviaId = await self.__triviaIdGenerator.generateQuestionId(
            question = question,
            category = category,
            difficulty = triviaDifficulty.toStr()
        )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswerStrings: list[str] = list()
            correctAnswerStrings.append(utils.getStrFromDict(triviaDict, 'correctAnswer'))
            incorrectAnswers: list[str] = triviaDict['incorrectAnswers']

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = incorrectAnswers
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = None,
                triviaSource = self.getTriviaSource()
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer= utils.getBoolFromDict(triviaDict, 'correctAnswer')

            return TrueFalseTriviaQuestion(
                correctAnswer = correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = None,
                triviaSource = self.getTriviaSource()
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Pkmn Trivia: {triviaDict}')

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.POKE_API

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    async def __selectRandomFalseBerryFlavors(
        self,
        actualFlavor: PokepediaBerryFlavor | None
    ) -> set[PokepediaBerryFlavor]:
        if actualFlavor is not None and not isinstance(actualFlavor, PokepediaBerryFlavor):
            raise ValueError(f'actualFlavor argument is malformed: \"{actualFlavor}\"')

        allFlavors: list[PokepediaBerryFlavor] = list(PokepediaBerryFlavor)
        falseFlavors: set[PokepediaBerryFlavor] = set()

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaBerryFlavor) - 1)
        responses = random.randint(minResponses, maxResponses)

        while len(falseFlavors) < responses:
            randomFlavor = random.choice(allFlavors)

            if randomFlavor is not actualFlavor:
                falseFlavors.add(randomFlavor)

        return falseFlavors

    async def __selectRandomFalseContestTypes(
        self,
        actualType: PokepediaContestType
    ) -> set[PokepediaContestType]:
        if not isinstance(actualType, PokepediaContestType):
            raise TypeError(f'actualType argument is malformed: \"{actualType}\"')

        allTypes: list[PokepediaContestType] = list(PokepediaContestType)
        falseTypes: set[PokepediaContestType] = set()

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaContestType) - 1)
        responses = random.randint(minResponses, maxResponses)

        while len(falseTypes) < responses:
            randomType = random.choice(allTypes)

            if randomType is not actualType:
                falseTypes.add(randomType)

        return falseTypes

    async def __selectRandomFalseElementTypes(
        self,
        actualTypes: list[PokepediaElementType]
    ) -> set[PokepediaElementType]:
        if not utils.hasItems(actualTypes):
            raise ValueError(f'actualTypes argument is malformed: \"{actualTypes}\"')

        allTypes: list[PokepediaElementType] = list(PokepediaElementType)
        falseTypes: set[PokepediaElementType] = set()

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaElementType) - 1)
        responses = random.randint(minResponses, maxResponses)

        while len(falseTypes) < responses:
            randomType = random.choice(allTypes)

            if randomType not in actualTypes and randomType is not PokepediaElementType.UNKNOWN:
                falseTypes.add(randomType)

        return falseTypes

    async def __selectRandomFalseMachineNumbers(
        self,
        actualMachineNumber: int,
        actualMachineType: PokepediaMachineType
    ) -> set[int]:
        if not utils.isValidInt(actualMachineNumber):
            raise ValueError(f'actualMachineNumber argument is malformed: \"{actualMachineNumber}\"')
        elif not isinstance(actualMachineType, PokepediaMachineType):
            raise ValueError(f'actualMachineType argument is malformed: \"{actualMachineType}\"')

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        responses = random.randint(minResponses, maxResponses)
        maxMachineNumber = actualMachineType.getMaxMachineNumber()

        falseMachineNumbers: set[int] = set()

        while len(falseMachineNumbers) < responses:
            randomInt = random.randint(1, maxMachineNumber)

            if randomInt != actualMachineNumber:
                falseMachineNumbers.add(randomInt)

        return falseMachineNumbers

    async def __selectRandomGeneration(
        self,
        initialGeneration: PokepediaGeneration
    ) -> PokepediaGeneration:
        if not isinstance(initialGeneration, PokepediaGeneration):
            raise ValueError(f'initialGeneration argument is malformed: \"{initialGeneration}\"')

        allGenerations: list[PokepediaGeneration] = list(PokepediaGeneration)
        indexOfMax = allGenerations.index(self.__maxGeneration)
        indexOfMin = allGenerations.index(initialGeneration)

        if indexOfMax < indexOfMin:
            raise RuntimeError(f'indexOfMax ({indexOfMax}) or indexOfMin ({indexOfMin}) is incompatible with an initial generation of {initialGeneration}! (maxGeneration={self.__maxGeneration})')

        return allGenerations[random.randint(indexOfMin, indexOfMax)]
