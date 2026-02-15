from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .triviaDatabase.booleanTriviaDatabaseTriviaQuestion import BooleanTriviaDatabaseTriviaQuestion
from .triviaDatabase.multipleChoiceTriviaDatabaseTriviaQuestion import MultipleChoiceTriviaDatabaseTriviaQuestion
from .triviaDatabase.triviaDatabaseQuestionStorageInterface import TriviaDatabaseQuestionStorageInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaExceptions import UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions


class TriviaDatabaseTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        triviaDatabaseQuestionStorage: TriviaDatabaseQuestionStorageInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(triviaDatabaseQuestionStorage, TriviaDatabaseQuestionStorageInterface):
            raise TypeError(f'triviaDatabaseQuestionStorage argument is malformed: \"{triviaDatabaseQuestionStorage}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__triviaDatabaseQuestionStorage: TriviaDatabaseQuestionStorageInterface = triviaDatabaseQuestionStorage
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        triviaDatabaseQuestion = await self.__triviaDatabaseQuestionStorage.fetchTriviaQuestion()

        category = await self.__triviaQuestionCompiler.compileCategory(triviaDatabaseQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(triviaDatabaseQuestion.question)

        if isinstance(triviaDatabaseQuestion, BooleanTriviaDatabaseTriviaQuestion):
            return TrueFalseTriviaQuestion(
                correctAnswer = triviaDatabaseQuestion.correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaDatabaseQuestion.triviaId,
                triviaDifficulty = triviaDatabaseQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        elif isinstance(triviaDatabaseQuestion, MultipleChoiceTriviaDatabaseTriviaQuestion):
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = triviaDatabaseQuestion.correctAnswer
            )
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = triviaDatabaseQuestion.incorrectAnswers
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
                triviaId = triviaDatabaseQuestion.triviaId,
                triviaDifficulty = triviaDatabaseQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        else:
            raise UnsupportedTriviaTypeException(f'triviaType \"{triviaDatabaseQuestion.triviaType}\" is not supported for Trivia Database: {triviaDatabaseQuestion}')

    async def hasQuestionSetAvailable(self) -> bool:
        return await self.__triviaDatabaseQuestionStorage.hasQuestionSetAvailable()

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.TRIVIA_DATABASE
