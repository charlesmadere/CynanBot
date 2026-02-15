import traceback
from typing import Any

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from ..additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import GenericTriviaNetworkException, MalformedTriviaJsonException
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class JServiceTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('JServiceTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://jservice.io/api/random?count=1')
        except GenericNetworkException as e:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Encountered network error ({fetchOptions=}): {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        if response.statusCode != 200:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Encountered non-200 HTTP status code: \"{response.statusCode}\" ({response=}) ({fetchOptions=})')
            raise GenericTriviaNetworkException(self.triviaSource)

        jsonResponse = await response.json()
        await response.close()

        if await self._triviaSettings.isDebugLoggingEnabled():
            self.__timber.log('JServiceTriviaQuestionRepository', f'{jsonResponse}')

        if not isinstance(jsonResponse, list) or len(jsonResponse) == 0:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: dict[str, Any] | None = jsonResponse[0]

        if not isinstance(triviaJson, dict) or len(triviaJson) == 0 or 'category' not in triviaJson:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')

        category = utils.getStrFromDict(triviaJson['category'], 'title', fallback = '').encode('latin1').decode('utf-8')
        category = await self.__triviaQuestionCompiler.compileCategory(category)

        question = utils.getStrFromDict(triviaJson, 'question').encode('latin1').decode('utf-8')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        triviaId = utils.getStrFromDict(triviaJson, 'id', fallback = '')

        if not utils.isValidStr(triviaId):
            triviaId = await self.__triviaIdGenerator.generateQuestionId(
                question = question,
                category = category
            )

        originalCorrectAnswers: list[str] = list()
        originalCorrectAnswers.append(utils.getStrFromDict(triviaJson, 'answer').encode('latin1').decode('utf-8'))

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = originalCorrectAnswers,
            triviaId = triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.triviaSource
        ):
            self.__timber.log('JServiceTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(originalCorrectAnswers)

        compiledCorrectAnswers: list[str] = list()
        compiledCorrectAnswers.append(utils.getStrFromDict(triviaJson, 'answer').encode('latin1').decode('utf-8'))

        await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = compiledCorrectAnswers,
            triviaId = triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.triviaSource
        )

        compiledCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(compiledCorrectAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for answer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return QuestionAnswerTriviaQuestion(
            allWords = None,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = correctAnswers,
            category = category,
            categoryId = None,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.triviaSource
        )

    async def hasQuestionSetAvailable(self) -> bool:
        return False

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.J_SERVICE
