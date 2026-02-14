import traceback

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .openTriviaDatabase.booleanOpenTriviaDatabaseQuestion import BooleanOpenTriviaDatabaseQuestion
from .openTriviaDatabase.multipleOpenTriviaDatabaseQuestion import MultipleOpenTriviaDatabaseQuestion
from .openTriviaDatabase.openTriviaDatabaseQuestionFetcherInterface import OpenTriviaDatabaseQuestionFetcherInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaExceptions import GenericTriviaNetworkException, UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class OpenTriviaDatabaseTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        openTriviaDatabaseQuestionFetcher: OpenTriviaDatabaseQuestionFetcherInterface,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(openTriviaDatabaseQuestionFetcher, OpenTriviaDatabaseQuestionFetcherInterface):
            raise TypeError(f'openTriviaDatabaseQuestionFetcher argument is malformed: \"{openTriviaDatabaseQuestionFetcher}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__openTriviaDatabaseQuestionFetcher: OpenTriviaDatabaseQuestionFetcherInterface = openTriviaDatabaseQuestionFetcher
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        try:
            openTriviaQuestion = await self.__openTriviaDatabaseQuestionFetcher.fetchTriviaQuestion(
                twitchChannelId = fetchOptions.twitchChannelId
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenTriviaDatabaseTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        category = await self.__triviaQuestionCompiler.compileCategory(openTriviaQuestion.category)
        question = await self.__triviaQuestionCompiler.compileQuestion(openTriviaQuestion.question)

        triviaId = await self.__triviaIdGenerator.generateQuestionId(
            question = openTriviaQuestion.question,
            category = openTriviaQuestion.category,
            difficulty = openTriviaQuestion.difficulty.toStr()
        )

        if isinstance(openTriviaQuestion, BooleanOpenTriviaDatabaseQuestion):
            return TrueFalseTriviaQuestion(
                correctAnswer = openTriviaQuestion.correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = openTriviaQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        elif isinstance(openTriviaQuestion, MultipleOpenTriviaDatabaseQuestion):
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = openTriviaQuestion.correctAnswer
            )
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = openTriviaQuestion.incorrectAnswers
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
                triviaDifficulty = openTriviaQuestion.difficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        else:
            raise UnsupportedTriviaTypeException(f'Encountered unknown OpenTriviaDatabaseQuestion instance: ({openTriviaQuestion=})')

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.OPEN_TRIVIA_DATABASE
