from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .openTriviaQa.booleanOpenTriviaQaTriviaQuestion import BooleanOpenTriviaQaTriviaQuestion
from .openTriviaQa.multipleChoiceOpenTriviaQaTriviaQuestion import MultipleChoiceOpenTriviaQaTriviaQuestion
from .openTriviaQa.openTriviaQaQuestionStorageInterface import OpenTriviaQaQuestionStorageInterface
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


class OpenTriviaQaTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        openTriviaQaQuestionStorage: OpenTriviaQaQuestionStorageInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(openTriviaQaQuestionStorage, OpenTriviaQaQuestionStorageInterface):
            raise TypeError(f'openTriviaQaQuestionStorage argument is malformed: \"{openTriviaQaQuestionStorage}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__openTriviaQaQuestionStorage: OpenTriviaQaQuestionStorageInterface = openTriviaQaQuestionStorage
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        openTriviaQaQuestion = await self.__openTriviaQaQuestionStorage.fetchTriviaQuestion()

        category = await self.__triviaQuestionCompiler.compileCategory(openTriviaQaQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(openTriviaQaQuestion.question)

        if isinstance(openTriviaQaQuestion, BooleanOpenTriviaQaTriviaQuestion):
            return TrueFalseTriviaQuestion(
                correctAnswer = openTriviaQaQuestion.correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = openTriviaQaQuestion.questionId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        elif isinstance(openTriviaQaQuestion, MultipleChoiceOpenTriviaQaTriviaQuestion):
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = openTriviaQaQuestion.correctAnswer
            )
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = openTriviaQaQuestion.incorrectAnswers
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
                triviaId = openTriviaQaQuestion.questionId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        else:
            raise UnsupportedTriviaTypeException(f'triviaType \"{openTriviaQaQuestion.questionType}\" is not supported for OpenTriviaQaTriviaQuestionRepository: {openTriviaQaQuestion}')

    async def hasQuestionSetAvailable(self) -> bool:
        return await self.__openTriviaQaQuestionStorage.hasQuestionSetAvailable()

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.OPEN_TRIVIA_QA
