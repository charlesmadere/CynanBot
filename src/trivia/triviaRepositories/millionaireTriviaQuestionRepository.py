from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .millionaire.millionaireTriviaQuestionStorageInterface import MillionaireTriviaQuestionStorageInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaFetchOptions import TriviaFetchOptions


class MillionaireTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        millionaireTriviaQuestionStorage: MillionaireTriviaQuestionStorageInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(millionaireTriviaQuestionStorage, MillionaireTriviaQuestionStorageInterface):
            raise TypeError(f'millionaireTriviaQuestionStorage argument is malformed: \"{millionaireTriviaQuestionStorage}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__millionaireTriviaQuestionStorage: MillionaireTriviaQuestionStorageInterface = millionaireTriviaQuestionStorage
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        millionaireTriviaQuestion = await self.__millionaireTriviaQuestionStorage.fetchTriviaQuestion()

        correctAnswer = await self.__triviaQuestionCompiler.compileResponse(millionaireTriviaQuestion.correctAnswer)
        question = await self.__triviaQuestionCompiler.compileResponse(millionaireTriviaQuestion.question)

        correctAnswers: list[str] = list()
        correctAnswers.append(correctAnswer)

        multipleChoiceResponses = await self.__triviaQuestionCompiler.compileResponses(
            responses = millionaireTriviaQuestion.incorrectAnswers,
        )

        multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
        )

        return MultipleChoiceTriviaQuestion(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = multipleChoiceResponses,
            category = None,
            categoryId = None,
            question = question,
            triviaId = millionaireTriviaQuestion.questionId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.triviaSource,
        )

    async def hasQuestionSetAvailable(self) -> bool:
        return await self.__millionaireTriviaQuestionStorage.hasQuestionSetAvailable()

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.MILLIONAIRE
