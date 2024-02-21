import traceback
from typing import Any, Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (GenericTriviaNetworkException,
                                              MalformedTriviaJsonException,
                                              UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class WillFryTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('WillFryTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://the-trivia-api.com/api/questions?limit=1')
        except GenericNetworkException as e:
            self.__timber.log('WillFryTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('WillFryTriviaQuestionRepository', f'Encountered non-200 HTTP status code: \"{response.getStatusCode()}\"')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('WillFryTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('WillFryTriviaQuestionRepository', f'Rejecting Will Fry Trivia\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Will Fry Trivia\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: Dict[str, Any] = jsonResponse[0]
        if not utils.hasItems(triviaJson):
            self.__timber.log('WillFryTriviaQuestionRepository', f'Rejecting Will Fry Trivia\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Will Fry Trivia\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaJson, 'type'))
        category = await self.__triviaQuestionCompiler.compileCategory(utils.getStrFromDict(triviaJson, 'category', fallback = ''))
        question = await self.__triviaQuestionCompiler.compileQuestion(utils.getStrFromDict(triviaJson, 'question'))

        triviaId = utils.getStrFromDict(triviaJson, 'id', fallback = '')
        if not utils.isValidStr(triviaId):
            triviaId = await self.__triviaIdGenerator.generateQuestionId(
                question = question,
                category = category
            )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = utils.getStrFromDict(triviaJson, 'correctAnswer'),
                htmlUnescape = True
            )
            correctAnswerStrings: List[str] = list()
            correctAnswerStrings.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = triviaJson['incorrectAnswers'],
                htmlUnescape = True
            )

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = incorrectAnswers
            )

            if await self._verifyIsActuallyMultipleChoiceQuestion(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = multipleChoiceResponses
            ):
                return MultipleChoiceTriviaQuestion(
                    correctAnswers = correctAnswerStrings,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = TriviaDifficulty.UNKNOWN,
                    triviaSource = TriviaSource.WILL_FRY_TRIVIA
                )
            else:
                self.__timber.log('WillFryTriviaQuestionRepository', f'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaJson, 'correctAnswer')
            correctAnswerBools: List[bool] = list()
            correctAnswerBools.append(correctAnswer)

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswerBools,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                triviaSource = TriviaSource.WILL_FRY_TRIVIA
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Will Fry Trivia: {jsonResponse}')

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.WILL_FRY_TRIVIA

    async def hasQuestionSetAvailable(self) -> bool:
        return True
