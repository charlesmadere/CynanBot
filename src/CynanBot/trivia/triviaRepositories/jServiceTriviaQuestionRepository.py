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
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class JServiceTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface), f"malformed {triviaAnswerCompiler=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('JServiceTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://jservice.io/api/random?count=1')
        except GenericNetworkException as e:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('JServiceTriviaQuestionRepository', f'Encountered non-200 HTTP status code: \"{response.getStatusCode()}\"')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse: Optional[List[Dict[str, Any]]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('JServiceTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('JServiceTriviaQuestionRepository', f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting jService\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: Optional[Dict[str, Any]] = jsonResponse[0]

        if not utils.hasItems(triviaJson) or 'category' not in triviaJson:
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

        correctAnswers: List[str] = list()
        correctAnswers.append(utils.getStrFromDict(triviaJson, 'answer').encode('latin1').decode('utf-8'))

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        ):
            self.__timber.log('JServiceTriviaQuestionRepository', f'Added additional answers to question (triviaId=\"{triviaId}\")')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        cleanedCorrectAnswers: List[str] = list()
        cleanedCorrectAnswers.append(utils.getStrFromDict(triviaJson, 'answer').encode('latin1').decode('utf-8'))

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

        return QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = list(expandedCleanedCorrectAnswers),
            category = category,
            categoryId = None,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.J_SERVICE
        )

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.J_SERVICE

    async def hasQuestionSetAvailable(self) -> bool:
        return True
