import traceback

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (GenericTriviaNetworkException,
                                              MalformedTriviaJsonException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class FuntoonTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('FuntoonTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://funtoon.party/api/trivia/random')
        except GenericNetworkException as e:
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Encountered non-200 HTTP status code: \"{response.getStatusCode()}\"')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse: dict[str, object] | None = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('FuntoonTriviaQuestionRepository', f'{jsonResponse}')

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Rejecting Funtoon\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Funtoon\'s JSON data due to null/empty contents: {jsonResponse}')

        category = utils.getStrFromDict(jsonResponse, 'category', fallback = '')
        category = await self.__triviaQuestionCompiler.compileCategory(category)

        categoryId = utils.getStrFromDict(jsonResponse, 'category_id')

        question = utils.getStrFromDict(jsonResponse, 'clue')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        triviaId = utils.getStrFromDict(jsonResponse, 'id')

        correctAnswers: list[str] = list()
        correctAnswers.append(utils.getStrFromDict(jsonResponse, 'answer'))

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        ):
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Added additional answers to question ({triviaId=})')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        cleanedCorrectAnswers: list[str] = list()
        cleanedCorrectAnswers.append(utils.getStrFromDict(jsonResponse, 'answer'))

        await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = cleanedCorrectAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        )

        cleanedCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(cleanedCorrectAnswers)

        expandedCleanedCorrectAnswers: set[str] = set()
        for answer in cleanedCorrectAnswers:
            expandedCleanedCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        # TODO In the future, we will also check some additional fields (`formatted_answer` and
        # `format_type`). These will assist in providing computer-readable answer logic.

        return QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = list(expandedCleanedCorrectAnswers),
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = TriviaSource.FUNTOON
        )

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.FUNTOON

    async def hasQuestionSetAvailable(self) -> bool:
        return True
