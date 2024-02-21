import random
import traceback
from typing import Any, Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from CynanBot.pkmn.pokepediaContestType import PokepediaContestType
from CynanBot.pkmn.pokepediaDamageClass import PokepediaDamageClass
from CynanBot.pkmn.pokepediaElementType import PokepediaElementType
from CynanBot.pkmn.pokepediaGeneration import PokepediaGeneration
from CynanBot.pkmn.pokepediaMachineType import PokepediaMachineType
from CynanBot.pkmn.pokepediaMove import PokepediaMove
from CynanBot.pkmn.pokepediaNature import PokepediaNature
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.pkmn.pokepediaStat import PokepediaStat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (GenericTriviaNetworkException,
                                              MalformedTriviaJsonException,
                                              UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class PkmnTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepository,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        maxGeneration: PokepediaGeneration = PokepediaGeneration.GENERATION_3
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(pokepediaRepository, PokepediaRepository), f"malformed {pokepediaRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(maxGeneration, PokepediaGeneration), f"malformed {maxGeneration=}"

        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__maxGeneration: PokepediaGeneration = maxGeneration

    async def __createMoveContestTypeQuestion(self, move: PokepediaMove) -> Optional[Dict[str, Any]]:
        assert isinstance(move, PokepediaMove), f"malformed {move=}"

        if not move.hasContestType():
            return None

        falseContestTypes = await self.__selectRandomFalseContestTypes(move.getContestType())

        falseContestTypeStrs: List[str] = list()
        for falseContestType in falseContestTypes:
            falseContestTypeStrs.append(falseContestType.toStr())

        return {
            'correctAnswer': move.getContestType().toStr(),
            'incorrectAnswers': falseContestTypeStrs,
            'question': f'In Pokémon, what is the contest type of {move.getName()}?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveDamageClassQuestion(self, move: PokepediaMove) -> Dict[str, Any]:
        assert isinstance(move, PokepediaMove), f"malformed {move=}"

        damageClassStrs: List[str] = list()
        for damageClass in PokepediaDamageClass:
            damageClassStrs.append(damageClass.toStr())

        return {
            'correctAnswer': move.getDamageClass().toStr(),
            'incorrectAnswers': damageClassStrs,
            'question': f'In Pokémon, the move {move.getName()} has which damage class?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveIsAvailableAsMachineQuestion(self, move: PokepediaMove) -> Dict[str, Any]:
        assert isinstance(move, PokepediaMove), f"malformed {move=}"

        randomGeneration = await self.__selectRandomGeneration(move.getInitialGeneration())

        machinesStrs: List[str] = list()
        for machineType in PokepediaMachineType:
            machinesStrs.append(machineType.toStr())

        machinesStr = '/'.join(machinesStrs)

        return {
            'correctAnswer': move.hasMachines() and randomGeneration in move.getGenerationMachines(),
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via {machinesStr}.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def __createMoveIsAvailableAsWhichMachineQuestion(self, move: PokepediaMove) -> Optional[Dict[str, Any]]:
        assert isinstance(move, PokepediaMove), f"malformed {move=}"

        if not move.hasMachines():
            return None

        randomGeneration = await self.__selectRandomGeneration(move.getInitialGeneration())
        machine = move.getGenerationMachines()[randomGeneration][0]
        correctMachineNumber = machine.getMachineNumber()
        machinePrefix = machine.getMachineType().toStr()

        falseMachineNumbers = await self.__selectRandomFalseMachineNumbers(
            actualMachineNumber = correctMachineNumber,
            actualMachineType = machine.getMachineType()
        )

        falseMachineNumbersStrs: List[str] = list()
        for falseMachineNumber in falseMachineNumbers:
            falseMachineNumbersStrs.append(f'{machinePrefix}{falseMachineNumber}')

        return {
            'correctAnswer': machine.getMachineName(),
            'incorrectAnswers': falseMachineNumbersStrs,
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {move.getName()} can be taught via which {machinePrefix}?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createMoveQuestion(self) -> Dict[str, Any]:
        try:
            move = await self.__pokepediaRepository.fetchRandomMove(maxGeneration = self.__maxGeneration)
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: Optional[Dict[str, Any]] = None

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

    async def __createNatureQuestion(self) -> Dict[str, Any]:
        try:
            nature = await self.__pokepediaRepository.fetchRandomNature()
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: Optional[Dict[str, Any]] = None

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
        berryFlavor: Optional[PokepediaBerryFlavor],
        likeOrDislikeStr: str
    ) -> Dict[str, Any]:
        assert isinstance(nature, PokepediaNature), f"malformed {nature=}"
        assert berryFlavor is None or isinstance(berryFlavor, PokepediaBerryFlavor), f"malformed {berryFlavor=}"
        if not utils.isValidStr(likeOrDislikeStr):
            raise ValueError(f'likeOrDislikeStr argument is malformed: \"{likeOrDislikeStr}\"')

        randomFlavors = await self.__selectRandomFalseBerryFlavors(berryFlavor)

        flavorsStrs: List[str] = list()
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

    async def __createPhysicalOrSpecialDamageClassQuestion(self) -> Dict[str, Any]:
        applicableDamageClasses: List[PokepediaDamageClass] = [
            PokepediaDamageClass.PHYSICAL, PokepediaDamageClass.SPECIAL
        ]

        actualDamageClass = random.choice(applicableDamageClasses)

        applicableElementTypes: List[PokepediaElementType] = [
            PokepediaElementType.BUG, PokepediaElementType.DARK, PokepediaElementType.DRAGON,
            PokepediaElementType.ELECTRIC, PokepediaElementType.FIGHTING, PokepediaElementType.FIRE,
            PokepediaElementType.FLYING, PokepediaElementType.GHOST, PokepediaElementType.GRASS,
            PokepediaElementType.GROUND, PokepediaElementType.ICE, PokepediaElementType.NORMAL,
            PokepediaElementType.POISON, PokepediaElementType.PSYCHIC, PokepediaElementType.ROCK,
            PokepediaElementType.STEEL, PokepediaElementType.WATER
        ]

        actualElementType: Optional[PokepediaElementType] = None
        while actualElementType is None or PokepediaDamageClass.getTypeBasedDamageClass(actualElementType) is not actualDamageClass:
            actualElementType = random.choice(applicableElementTypes)

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaElementType) - 1)
        responses = random.randint(minResponses, maxResponses)

        falseElementTypes: Set[PokepediaElementType] = set()
        while len(falseElementTypes) < responses:
            falseElementType = random.choice(applicableElementTypes)

            if PokepediaDamageClass.getTypeBasedDamageClass(falseElementType) is not actualDamageClass:
                falseElementTypes.add(falseElementType)

        falseElementTypesStrs: List[str] = list()
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

    async def __createPokemonQuestion(self) -> Dict[str, Any]:
        try:
            pokemon = await self.__pokepediaRepository.fetchRandomPokemon(maxGeneration = self.__maxGeneration)
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        randomGeneration = await self.__selectRandomGeneration(pokemon.getInitialGeneration())
        correctTypes = pokemon.getCorrespondingGenerationElementTypes(randomGeneration)
        correctType = random.choice(correctTypes)

        falseTypes = await self.__selectRandomFalseElementTypes(correctTypes)

        falseTypesStrs: List[str] = list()
        for falseType in falseTypes:
            falseTypesStrs.append(falseType.toStr())

        return {
            'correctAnswer': correctType.toStr(),
            'incorrectAnswers': falseTypesStrs,
            'question': f'In Pokémon {randomGeneration.toLongStr()}, {pokemon.getName()} is which of the following types?',
            'triviaType': TriviaQuestionType.MULTIPLE_CHOICE
        }

    async def __createStatOrNatureQuestion(self) -> Dict[str, Any]:
        randomTriviaType = random.randint(0, 1)

        if randomTriviaType == 0:
            return await self.__createStatQuestion()
        elif randomTriviaType == 1:
            return await self.__createNatureQuestion()
        else:
            raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

    async def __createStatQuestion(self) -> Dict[str, Any]:
        try:
            stat = await self.__pokepediaRepository.fetchRandomStat()
        except GenericNetworkException as e:
            self.__timber.log('PkmnTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        triviaDict: Optional[Dict[str, Any]] = None

        while triviaDict is None:
            randomTriviaType = random.randint(0, 1)

            if randomTriviaType == 0:
                triviaDict = await self.__createStatDecreasingNaturesQuestion(stat)
            elif randomTriviaType == 1:
                triviaDict = await self.__createStatIncreasingNaturesQuestion(stat)
            else:
                raise RuntimeError(f'PkmnTriviaQuestionRepository\'s randomTriviaType value is out of bounds: \"{randomTriviaType}\"!')

        return triviaDict

    async def __createStatDecreasingNaturesQuestion(self, stat: PokepediaStat) -> Dict[str, Any]:
        assert isinstance(stat, PokepediaStat), f"malformed {stat=}"

        decreasingNatures = stat.getDecreasingNatures()
        randomNature = random.choice(list(PokepediaNature))

        return {
            'correctAnswer': decreasingNatures is not None and randomNature in decreasingNatures,
            'question': f'In Pokémon, the {stat.toStr()} stat is negatively impacted by the {randomNature.toStr()} nature.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def __createStatIncreasingNaturesQuestion(self, stat: PokepediaStat) -> Dict[str, Any]:
        assert isinstance(stat, PokepediaStat), f"malformed {stat=}"

        increasingNatures = stat.getIncreasingNatures()
        randomNature = random.choice(list(PokepediaNature))

        return {
            'correctAnswer': increasingNatures is not None and randomNature in increasingNatures,
            'question': f'In Pokémon, the {stat.toStr()} stat is positively impacted by the {randomNature.toStr()} nature.',
            'triviaType': TriviaQuestionType.TRUE_FALSE
        }

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('PkmnTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        randomTriviaType = random.randint(0, 6)
        triviaDict: Optional[Dict[str, Any]] = None

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
            correctAnswers: List[str] = list()
            correctAnswers.append(utils.getStrFromDict(triviaDict, 'correctAnswer'))
            incorrectAnswers: List[str] = triviaDict['incorrectAnswers']

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = incorrectAnswers
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.POKE_API
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswers: List[bool] = list()
            correctAnswers.append(utils.getBoolFromDict(triviaDict, 'correctAnswer'))

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswers,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.POKE_API
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Pkmn Trivia: {triviaDict}')

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.POKE_API

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    async def __selectRandomFalseBerryFlavors(
        self,
        actualFlavor: Optional[PokepediaBerryFlavor]
    ) -> Set[PokepediaBerryFlavor]:
        assert actualFlavor is None or isinstance(actualFlavor, PokepediaBerryFlavor), f"malformed {actualFlavor=}"

        allFlavors: List[PokepediaBerryFlavor] = list(PokepediaBerryFlavor)
        falseFlavors: Set[PokepediaBerryFlavor] = set()

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
    ) -> Set[PokepediaContestType]:
        assert isinstance(actualType, PokepediaContestType), f"malformed {actualType=}"

        allTypes: List[PokepediaContestType] = list(PokepediaContestType)
        falseTypes: Set[PokepediaContestType] = set()

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
        actualTypes: List[PokepediaElementType]
    ) -> Set[PokepediaElementType]:
        if not utils.hasItems(actualTypes):
            raise ValueError(f'actualTypes argument is malformed: \"{actualTypes}\"')

        allTypes: List[PokepediaElementType] = list(PokepediaElementType)
        falseTypes: Set[PokepediaElementType] = set()

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
    ) -> Set[int]:
        if not utils.isValidInt(actualMachineNumber):
            raise ValueError(f'actualMachineNumber argument is malformed: \"{actualMachineNumber}\"')
        assert isinstance(actualMachineType, PokepediaMachineType), f"malformed {actualMachineType=}"

        minResponses = await self._triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self._triviaSettingsRepository.getMaxMultipleChoiceResponses()
        responses = random.randint(minResponses, maxResponses)
        maxMachineNumber = actualMachineType.getMaxMachineNumber()

        falseMachineNumbers: Set[int] = set()

        while len(falseMachineNumbers) < responses:
            randomInt = random.randint(1, maxMachineNumber)

            if randomInt != actualMachineNumber:
                falseMachineNumbers.add(randomInt)

        return falseMachineNumbers

    async def __selectRandomGeneration(
        self,
        initialGeneration: PokepediaGeneration
    ) -> PokepediaGeneration:
        assert isinstance(initialGeneration, PokepediaGeneration), f"malformed {initialGeneration=}"

        allGenerations: List[PokepediaGeneration] = list(PokepediaGeneration)
        indexOfMax = allGenerations.index(self.__maxGeneration)
        indexOfMin = allGenerations.index(initialGeneration)

        if indexOfMax < indexOfMin:
            raise RuntimeError(f'indexOfMax ({indexOfMax}) or indexOfMin ({indexOfMin}) is incompatible with an initial generation of {initialGeneration}! (maxGeneration={self.__maxGeneration})')

        return allGenerations[random.randint(indexOfMin, indexOfMax)]
