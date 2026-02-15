import traceback

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .willFry.willFryTriviaApiServiceInterface import WillFryTriviaApiServiceInterface
from .willFry.willFryTriviaQuestionType import WillFryTriviaQuestionType
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaExceptions import GenericTriviaNetworkException, UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class WillFryTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
        willFryTriviaApiService: WillFryTriviaApiServiceInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not isinstance(willFryTriviaApiService, WillFryTriviaApiServiceInterface):
            raise TypeError(f'willFryTriviaApiService argument is malformed: \"{willFryTriviaApiService}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__willFryTriviaApiService: WillFryTriviaApiServiceInterface = willFryTriviaApiService

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        try:
            willFryTriviaQuestion = await self.__willFryTriviaApiService.fetchTriviaQuestion()
        except GenericNetworkException as e:
            self.__timber.log('WillFryTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        category = await self.__triviaQuestionCompiler.compileCategory(willFryTriviaQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(willFryTriviaQuestion.question.text)

        match willFryTriviaQuestion.questionType:
            case WillFryTriviaQuestionType.TEXT_CHOICE:
                correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                    response = willFryTriviaQuestion.correctAnswer
                )
                correctAnswers: list[str] = list()
                correctAnswers.append(correctAnswer)

                incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                    responses = willFryTriviaQuestion.incorrectAnswers
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
                    triviaId = willFryTriviaQuestion.triviaId,
                    triviaDifficulty = willFryTriviaQuestion.difficulty,
                    originalTriviaSource = None,
                    triviaSource = self.triviaSource
                )

            case _:
                raise UnsupportedTriviaTypeException(f'triviaType \"{willFryTriviaQuestion.questionType}\" is not supported for Will Fry Trivia: {willFryTriviaQuestion}')

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.WILL_FRY_TRIVIA
