import traceback

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .bongo.bongoApiServiceInterface import BongoApiServiceInterface
from .bongo.booleanBongoTriviaQuestion import BooleanBongoTriviaQuestion
from .bongo.multipleBongoTriviaQuestion import MultipleBongoTriviaQuestion
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaExceptions import GenericTriviaNetworkException, UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class BongoTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        bongoApiService: BongoApiServiceInterface,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(bongoApiService, BongoApiServiceInterface):
            raise TypeError(f'bongoApiService argument is malformed: \"{bongoApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__bongoApiService: BongoApiServiceInterface = bongoApiService
        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        try:
            bongoTriviaQuestion = await self.__bongoApiService.fetchTriviaQuestion()
        except GenericNetworkException as e:
            self.__timber.log('BongoTriviaQuestionRepository', f'Encountered network error', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        category = await self.__triviaQuestionCompiler.compileCategory(bongoTriviaQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(bongoTriviaQuestion.question)

        if isinstance(bongoTriviaQuestion, BooleanBongoTriviaQuestion):
            return TrueFalseTriviaQuestion(
                correctAnswer = bongoTriviaQuestion.correctAnswer,
                category = category,
                categoryId = None,
                question = bongoTriviaQuestion.question,
                triviaId = bongoTriviaQuestion.triviaId,
                triviaDifficulty = bongoTriviaQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource,
            )

        elif isinstance(bongoTriviaQuestion, MultipleBongoTriviaQuestion):
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = bongoTriviaQuestion.correctAnswer,
            )
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = bongoTriviaQuestion.incorrectAnswers,
            )

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = incorrectAnswers,
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = bongoTriviaQuestion.triviaId,
                triviaDifficulty = bongoTriviaQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource,
            )

        else:
            raise UnsupportedTriviaTypeException(f'Encountered unknown BongoTriviaQuestion instance: ({bongoTriviaQuestion=})')

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.BONGO
