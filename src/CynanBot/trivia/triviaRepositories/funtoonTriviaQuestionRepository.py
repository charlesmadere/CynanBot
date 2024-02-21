import traceback
from typing import Any, Dict, List, Optional, Set

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

        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface), f"malformed {triviaAnswerCompiler=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

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

        jsonResponse: Optional[List[Dict[str, Any]]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('FuntoonTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Rejecting Funtoon\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Funtoon\'s JSON data due to null/empty contents: {jsonResponse}')

        category = utils.getStrFromDict(jsonResponse, 'category', fallback = '')
        category = await self.__triviaQuestionCompiler.compileCategory(category)

        categoryId = utils.getStrFromDict(jsonResponse, 'category_id')

        question = utils.getStrFromDict(jsonResponse, 'clue')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        triviaId = utils.getStrFromDict(jsonResponse, 'id')

        correctAnswers: List[str] = list()
        correctAnswers.append(utils.getStrFromDict(jsonResponse, 'answer'))

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        ):
            self.__timber.log('FuntoonTriviaQuestionRepository', f'Added additional answers to question (triviaId=\"{triviaId}\")')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        cleanedCorrectAnswers: List[str] = list()
        cleanedCorrectAnswers.append(utils.getStrFromDict(jsonResponse, 'answer'))

        await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = cleanedCorrectAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        )

        cleanedCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(cleanedCorrectAnswers)

        expandedCleanedCorrectAnswers: Set[str] = set()
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
            triviaSource = TriviaSource.FUNTOON
        )

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.FUNTOON

    async def hasQuestionSetAvailable(self) -> bool:
        return True
