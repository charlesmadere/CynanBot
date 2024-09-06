import random

from frozenlist import FrozenList

from .exceptions import UnsupportedPokepediaTriviaQuestionType
from .multipleChoicePokepediaTriviaQuestion import MultipleChoicePokepediaTriviaQuestion
from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from .pokepediaTriviaQuestionGeneratorInterface import PokepediaTriviaQuestionGeneratorInterface
from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ....misc import utils as utils
from ....pkmn.pokepediaBerryFlavor import PokepediaBerryFlavor
from ....pkmn.pokepediaContestType import PokepediaContestType
from ....pkmn.pokepediaDamageClass import PokepediaDamageClass
from ....pkmn.pokepediaElementType import PokepediaElementType
from ....pkmn.pokepediaGeneration import PokepediaGeneration
from ....pkmn.pokepediaMachineType import PokepediaMachineType
from ....pkmn.pokepediaMove import PokepediaMove
from ....pkmn.pokepediaNature import PokepediaNature
from ....pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from ....timber.timberInterface import TimberInterface


class PokepediaTriviaQuestionGenerator(PokepediaTriviaQuestionGeneratorInterface):

    def __init__(
        self,
        pokepediaRepository: PokepediaRepositoryInterface,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        enabledQuestionTypes: frozenset[PokepediaTriviaQuestionType] = frozenset(PokepediaTriviaQuestionType),
        maxGeneration: PokepediaGeneration = PokepediaGeneration.GENERATION_3
    ):
        if not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(enabledQuestionTypes, frozenset):
            raise TypeError(f'enabledQuestionTypes argument is malformed: \"{enabledQuestionTypes}\"')
        elif len(enabledQuestionTypes) == 0:
            raise ValueError(f'enabledQuestionsTypes argument is empty: \"{enabledQuestionTypes}\"')
        elif not isinstance(maxGeneration, PokepediaGeneration):
            raise TypeError(f'maxGeneration argument is malformed: \"{maxGeneration}\"')

        self.__pokepediaRepository: PokepediaRepositoryInterface = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__enabledQuestionTypes: frozenset[PokepediaTriviaQuestionType] = enabledQuestionTypes
        self.__maxGeneration: PokepediaGeneration = maxGeneration

    async def __createMoveContestTypeQuestion(self, move: PokepediaMove) -> PokepediaTriviaQuestion | None:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        contestType = move.getContestType()
        if contestType is None:
            return None

        falseContestTypes = await self.__selectRandomFalseContestTypes(contestType)
        falseContestTypeStrs: list[str] = list()

        for falseContestType in falseContestTypes:
            falseContestTypeStrs.append(falseContestType.toStr())

        falseContestTypeStrs.sort(key = lambda falseContestType: falseContestType.casefold())
        frozenFalseContestTypeStrs: FrozenList[str] = FrozenList(falseContestTypeStrs)
        frozenFalseContestTypeStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenFalseContestTypeStrs,
            pokepediaTriviaType = PokepediaTriviaQuestionType.MOVE,
            correctAnswer = contestType.toStr(),
            question = f'In Pokémon, what is the contest type of {move.getName()}?'
        )

    async def __createMoveDamageClassQuestion(self, move: PokepediaMove) -> PokepediaTriviaQuestion:
        if not isinstance(move, PokepediaMove):
            raise TypeError(f'move argument is malformed: \"{move}\"')

        damageClassStrs: list[str] = list()

        for damageClass in PokepediaDamageClass:
            damageClassStrs.append(damageClass.toStr())

        damageClassStrs.sort(key = lambda damageClass: damageClass.casefold())
        frozenDamageClassStrs: FrozenList[str] = FrozenList(damageClassStrs)
        frozenDamageClassStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenDamageClassStrs,
            pokepediaTriviaType = PokepediaTriviaQuestionType.DAMAGE_CLASS,
            correctAnswer = move.getDamageClass().toStr(),
            question = f'In Pokémon, the move {move.getName()} has which damage class?'
        )

    async def __createNatureBerryFlavorQuestion(
        self,
        nature: PokepediaNature,
        berryFlavor: PokepediaBerryFlavor | None,
        likeOrDislikeStr: str
    ) -> PokepediaTriviaQuestion:
        if not isinstance(nature, PokepediaNature):
            raise TypeError(f'nature argument is malformed: \"{nature}\"')
        elif berryFlavor is not None and not isinstance(berryFlavor, PokepediaBerryFlavor):
            raise TypeError(f'berryFlavor argument is malformed: \"{berryFlavor}\"')
        elif not utils.isValidStr(likeOrDislikeStr):
            raise TypeError(f'likeOrDislikeStr argument is malformed: \"{likeOrDislikeStr}\"')

        randomFlavors = await self.__selectRandomFalseBerryFlavors(berryFlavor)
        flavorStrs: list[str] = list()

        for randomFlavor in randomFlavors:
            flavorStrs.append(randomFlavor.toStr())

        flavorStrs.sort(key = lambda flavor: flavor.casefold())

        noneOfThese = 'None of these'
        flavorStrs.append(noneOfThese)

        frozenFlavorStrs: FrozenList[str] = FrozenList(flavorStrs)
        frozenFlavorStrs.freeze()

        correctAnswer: str
        if berryFlavor is None:
            correctAnswer = noneOfThese
        else:
            correctAnswer = berryFlavor.toStr()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenFlavorStrs,
            pokepediaTriviaType = TriviaQuestionType.MULTIPLE_CHOICE,
            correctAnswer = correctAnswer,
            question = f'Pokémon with the {nature.toStr()} nature {likeOrDislikeStr} ONE of the following flavors.'
        )

    async def __determinePokepediaTriviaType(self) -> PokepediaTriviaQuestionType:
        # TODO this should be weighted
        enabledQuestionTypes = list(self.__enabledQuestionTypes)
        return random.choice(enabledQuestionTypes)

    async def fetchTriviaQuestion(self) -> PokepediaTriviaQuestion:
        pokepediaTriviaType = await self.__determinePokepediaTriviaType()

        match pokepediaTriviaType:
            case PokepediaTriviaQuestionType.DAMAGE_CLASS:
                pass

            case PokepediaTriviaQuestionType.MOVE:
                pass

            case PokepediaTriviaQuestionType.POKEMON:
                pass

            case PokepediaTriviaQuestionType.STAT_OR_NATURE:
                pass

            case _:
                pass

        raise UnsupportedPokepediaTriviaQuestionType(f'Encountered unsupported PokepediaTriviaQuestionType: ({pokepediaTriviaType=})')

    async def __selectRandomFalseBerryFlavors(
        self,
        actualFlavor: PokepediaBerryFlavor | None
    ) -> frozenset[PokepediaBerryFlavor]:
        if actualFlavor is not None and not isinstance(actualFlavor, PokepediaBerryFlavor):
            raise TypeError(f'actualFlavor argument is malformed: \"{actualFlavor}\"')

        allFlavors: list[PokepediaBerryFlavor] = list(PokepediaBerryFlavor)
        falseFlavors: set[PokepediaBerryFlavor] = set()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaBerryFlavor) - 1)
        responses = random.randint(minResponses, maxResponses)

        while len(falseFlavors) < responses:
            randomFlavor = random.choice(allFlavors)

            if randomFlavor is not actualFlavor:
                falseFlavors.add(randomFlavor)

        return frozenset(falseFlavors)

    async def __selectRandomFalseContestTypes(
        self,
        actualType: PokepediaContestType
    ) -> frozenset[PokepediaContestType]:
        if not isinstance(actualType, PokepediaContestType):
            raise TypeError(f'actualType argument is malformed: \"{actualType}\"')

        allTypes: list[PokepediaContestType] = list(PokepediaContestType)
        falseTypes: set[PokepediaContestType] = set()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaContestType) - 1)
        responses = random.randint(minResponses, maxResponses)

        while len(falseTypes) < responses:
            randomType = random.choice(allTypes)

            if randomType is not actualType:
                falseTypes.add(randomType)

        return frozenset(falseTypes)

    async def __selectRandomFalseElementTypes(
        self,
        actualTypes: list[PokepediaElementType]
    ) -> frozenset[PokepediaElementType]:
        if not isinstance(actualTypes, list) or len(actualTypes) == 0:
            raise TypeError(f'actualTypes argument is malformed: \"{actualTypes}\"')

        allTypes: list[PokepediaElementType] = list(PokepediaElementType)
        falseTypes: set[PokepediaElementType] = set()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaElementType) - 1)
        responses = random.randint(minResponses, maxResponses)

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

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
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
        initialGeneration: PokepediaGeneration
    ) -> PokepediaGeneration:
        if not isinstance(initialGeneration, PokepediaGeneration):
            raise TypeError(f'initialGeneration argument is malformed: \"{initialGeneration}\"')

        allGenerations: list[PokepediaGeneration] = list(PokepediaGeneration)
        indexOfMax = allGenerations.index(self.__maxGeneration)
        indexOfMin = allGenerations.index(initialGeneration)

        if indexOfMax < indexOfMin:
            raise RuntimeError(f'indexOfMax ({indexOfMax}) or indexOfMin ({indexOfMin}) is incompatible with an initial generation of {initialGeneration}! ({self.__maxGeneration=})')

        return allGenerations[random.randint(indexOfMin, indexOfMax)]
