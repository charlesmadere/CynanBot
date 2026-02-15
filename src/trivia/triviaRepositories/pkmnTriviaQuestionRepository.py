from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .pokepedia.booleanPokepediaTriviaQuestion import BooleanPokepediaTriviaQuestion
from .pokepedia.multipleChoicePokepediaTriviaQuestion import MultipleChoicePokepediaTriviaQuestion
from .pokepedia.pokepediaTriviaQuestionGeneratorInterface import PokepediaTriviaQuestionGeneratorInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...pkmn.pokepediaGeneration import PokepediaGeneration


class PkmnTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        pokepediaTriviaQuestionGenerator: PokepediaTriviaQuestionGeneratorInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
        maxGeneration: PokepediaGeneration = PokepediaGeneration.GENERATION_3,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(pokepediaTriviaQuestionGenerator, PokepediaTriviaQuestionGeneratorInterface):
            raise TypeError(f'pokepediaTriviaQuestionGenerator argument is malformed: \"{pokepediaTriviaQuestionGenerator}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(maxGeneration, PokepediaGeneration):
            raise TypeError(f'maxGeneration argument is malformed: \"{maxGeneration}\"')

        self.__pokepediaTriviaQuestionGenerator: PokepediaTriviaQuestionGeneratorInterface = pokepediaTriviaQuestionGenerator
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__maxGeneration: PokepediaGeneration = maxGeneration

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        pokepediaTriviaQuestion = await self.__pokepediaTriviaQuestionGenerator.fetchTriviaQuestion(
            maxGeneration = self.__maxGeneration
        )

        category = await self.__triviaQuestionCompiler.compileCategory('Pokémon')
        question = await self.__triviaQuestionCompiler.compileQuestion(pokepediaTriviaQuestion.question)

        triviaId = await self.__triviaIdGenerator.generateQuestionId(
            question = question,
            category = category,
            difficulty = TriviaDifficulty.UNKNOWN.toStr()
        )

        if isinstance(pokepediaTriviaQuestion, BooleanPokepediaTriviaQuestion):
            return TrueFalseTriviaQuestion(
                correctAnswer = pokepediaTriviaQuestion.correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        elif isinstance(pokepediaTriviaQuestion, MultipleChoicePokepediaTriviaQuestion):
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = pokepediaTriviaQuestion.correctAnswer
            )
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = pokepediaTriviaQuestion.incorrectAnswers
            )

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
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        else:
            raise UnsupportedTriviaTypeException(f'Encountered unknown PokepediaTriviaQuestion instance: ({pokepediaTriviaQuestion=})')

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.POKE_API
