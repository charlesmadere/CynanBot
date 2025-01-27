import random
from enum import Enum, auto

from frozenlist import FrozenList

from .booleanPokepediaTriviaQuestion import BooleanPokepediaTriviaQuestion
from .exceptions import UnsupportedPokepediaTriviaQuestionType
from .multipleChoicePokepediaTriviaQuestion import MultipleChoicePokepediaTriviaQuestion
from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from .pokepediaTriviaQuestionGeneratorInterface import PokepediaTriviaQuestionGeneratorInterface
from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
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
from ....pkmn.pokepediaStat import PokepediaStat
from ....timber.timberInterface import TimberInterface


class PokepediaTriviaQuestionGenerator(PokepediaTriviaQuestionGeneratorInterface):

    class MoveQuestionType(Enum):
        CONTEST = auto()
        DAMAGE_CLASS = auto()
        IS_AVAILABLE_AS_MACHINE = auto()
        IS_AVAILABLE_AS_WHICH_MACHINE = auto()

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

    async def __createMoveQuestion(self) -> PokepediaTriviaQuestion:
        # TODO
        raise RuntimeError()

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
            pokepediaTriviaType = PokepediaTriviaQuestionType.STAT_OR_NATURE,
            correctAnswer = correctAnswer,
            question = f'Pokémon with the {nature.toStr()} nature {likeOrDislikeStr} ONE of the following flavors.'
        )

    async def __createPhysicalOrSpecialDamageClassQuestion(self) -> PokepediaTriviaQuestion:
        actualDamageClass = random.choice([ PokepediaDamageClass.PHYSICAL, PokepediaDamageClass.SPECIAL ])

        applicableElementTypes: FrozenList[PokepediaElementType] = FrozenList([
            PokepediaElementType.BUG, PokepediaElementType.DARK, PokepediaElementType.DRAGON,
            PokepediaElementType.ELECTRIC, PokepediaElementType.FIGHTING, PokepediaElementType.FIRE,
            PokepediaElementType.FLYING, PokepediaElementType.GHOST, PokepediaElementType.GRASS,
            PokepediaElementType.GROUND, PokepediaElementType.ICE, PokepediaElementType.NORMAL,
            PokepediaElementType.POISON, PokepediaElementType.PSYCHIC, PokepediaElementType.ROCK,
            PokepediaElementType.STEEL, PokepediaElementType.WATER
        ])
        applicableElementTypes.freeze()

        actualElementType: PokepediaElementType | None = None
        while actualElementType is None or PokepediaDamageClass.getTypeBasedDamageClass(actualElementType) is not actualDamageClass:
            actualElementType = random.choice(applicableElementTypes)

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
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

        frozenFalseElementTypesStrs: FrozenList[str] = FrozenList(falseElementTypesStrs)
        frozenFalseElementTypesStrs.freeze()

        # It reads sort of strangely that the below question specifically mentions only Pokemon
        # generations 1 through 3, however, this is intentional. This is because those generations
        # of Pokemon games had their element types hard-coded to particular damage classes, which
        # is the purpose of this trivia question.

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = frozenFalseElementTypesStrs,
            pokepediaTriviaType = PokepediaTriviaQuestionType.STAT_OR_NATURE,
            correctAnswer = actualElementType.toStr(),
            question = f'In Pokémon generations 1 through 3, which of the following types has a {actualDamageClass.toStr().lower()} damage class?',
        )

    async def __createPokemonQuestion(self) -> PokepediaTriviaQuestion:
        pokemon = await self.__pokepediaRepository.fetchRandomPokemon(maxGeneration = self.__maxGeneration)
        randomGeneration = await self.__selectRandomGeneration(pokemon.getInitialGeneration())
        correctTypes = pokemon.getCorrespondingGenerationElementTypes(randomGeneration)
        correctType = random.choice(correctTypes)

        falseTypes = await self.__selectRandomFalseElementTypes(correctTypes)

        falseTypesStrs: FrozenList[str] = FrozenList()
        for falseType in falseTypes:
            falseTypesStrs.append(falseType.toStr())

        falseTypesStrs.freeze()

        return MultipleChoicePokepediaTriviaQuestion(
            incorrectAnswers = falseTypesStrs,
            correctAnswer = correctType.toStr(),
            pokepediaTriviaType = PokepediaTriviaQuestionType.POKEMON,
            question = f'In Pokémon {randomGeneration.toLongStr()}, {pokemon.getName()} is which of the following types?',
        )

    async def __createStatIncreasingNaturesQuestion(self, stat: PokepediaStat) -> PokepediaTriviaQuestion:
        if not isinstance(stat, PokepediaStat):
            raise TypeError(f'stat argument is malformed: \"{stat}\"')

        increasingNatures = stat.increasingNatures
        randomNature = random.choice(list(PokepediaNature))

        return BooleanPokepediaTriviaQuestion(
            correctAnswer = increasingNatures is not None and randomNature in increasingNatures,
            pokepediaTriviaType = PokepediaTriviaQuestionType.STAT_OR_NATURE,
            question = f'In Pokémon, the {stat.toStr()} stat is positively impacted by the {randomNature.toStr()} nature.'
        )

    async def __createStatOrNatureQuestion(self) -> PokepediaTriviaQuestion:
        # TODO
        raise RuntimeError()

    async def fetchTriviaQuestion(self) -> PokepediaTriviaQuestion:
        # TODO this should be weighted to prioritize certain question types
        pokepediaTriviaQuestionType = random.choice(list(PokepediaTriviaQuestionType))

        match pokepediaTriviaQuestionType:
            case PokepediaTriviaQuestionType.MOVE:
                return await self.__createMoveQuestion()

            case PokepediaTriviaQuestionType.POKEMON:
                return await self.__createPokemonQuestion()

            case PokepediaTriviaQuestionType.STAT_OR_NATURE:
                return await self.__createStatOrNatureQuestion()

        raise UnsupportedPokepediaTriviaQuestionType(f'Encountered unsupported PokepediaTriviaQuestionType: ({pokepediaTriviaQuestionType=})')

    async def __selectRandomFalseBerryFlavors(
        self,
        actualFlavor: PokepediaBerryFlavor | None
    ) -> frozenset[PokepediaBerryFlavor]:
        if actualFlavor is not None and not isinstance(actualFlavor, PokepediaBerryFlavor):
            raise TypeError(f'actualFlavor argument is malformed: \"{actualFlavor}\"')

        allFlavors: FrozenList[PokepediaBerryFlavor] = FrozenList(PokepediaBerryFlavor)
        allFlavors.freeze()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaBerryFlavor) - 1)
        responses = random.randint(minResponses, maxResponses)

        falseFlavors: set[PokepediaBerryFlavor] = set()

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

        allTypes: FrozenList[PokepediaContestType] = FrozenList(PokepediaContestType)
        allTypes.freeze()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
        maxResponses = min(maxResponses, len(PokepediaContestType) - 1)
        responses = random.randint(minResponses, maxResponses)

        falseTypes: set[PokepediaContestType] = set()

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

        allTypes: FrozenList[PokepediaElementType] = FrozenList(PokepediaElementType)
        allTypes.freeze()

        minResponses = await self.__triviaSettingsRepository.getMinMultipleChoiceResponses()
        maxResponses = await self.__triviaSettingsRepository.getMaxMultipleChoiceResponses()
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
