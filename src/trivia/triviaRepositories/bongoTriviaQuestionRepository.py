import traceback
from typing import Any

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (GenericTriviaNetworkException,
                                MalformedTriviaJsonException,
                                UnsupportedTriviaTypeException)
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ..triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class BongoTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('BongoTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get('https://beta-trivia.bongo.best/?limit=1')
        except GenericNetworkException as e:
            self.__timber.log('BongoTriviaQuestionRepository', f'Encountered network error: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('BongoTriviaQuestionRepository', f'Encountered non-200 HTTP status code: {response.getStatusCode()}')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse: list[dict[str, Any]] | None | Any = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('BongoTriviaQuestionRepository', f'{jsonResponse}')

        if not isinstance(jsonResponse, list) or len(jsonResponse) == 0:
            self.__timber.log('BongoTriviaQuestionRepository', f'Rejecting JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Bongo\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: dict[str, Any] | None = jsonResponse[0]
        if not isinstance(triviaJson, dict) or len(triviaJson) == 0:
            self.__timber.log('BongoTriviaQuestionRepository', f'Rejecting JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Bongo\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaDifficulty = TriviaDifficulty.fromStr(utils.getStrFromDict(triviaJson, 'difficulty', fallback = ''))
        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaJson, 'type'))

        category = await self.__triviaQuestionCompiler.compileCategory(
            category = utils.getStrFromDict(triviaJson, 'category', fallback = ''),
            htmlUnescape = True
        )

        question = await self.__triviaQuestionCompiler.compileQuestion(
            question = utils.getStrFromDict(triviaJson, 'question'),
            htmlUnescape = True
        )

        triviaId = utils.getStrFromDict(triviaJson, 'id', fallback = '')
        if not utils.isValidStr(triviaId):
            triviaId = await self.__triviaIdGenerator.generateQuestionId(
                question = question,
                category = category,
                difficulty = triviaDifficulty.toStr()
            )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(
                response = utils.getStrFromDict(triviaJson, 'correct_answer'),
                htmlUnescape = True
            )
            correctAnswerStrings: list[str] = list()
            correctAnswerStrings.append(correctAnswer)

            incorrectAnswers = await self.__triviaQuestionCompiler.compileResponses(
                responses = triviaJson['incorrect_answers'],
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
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = None,
                    triviaSource = TriviaSource.BONGO
                )
            else:
                self.__timber.log('BongoTriviaQuestionRepository', 'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaJson, 'correct_answer')

            return TrueFalseTriviaQuestion(
                correctAnswer = correctAnswer,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = None,
                triviaSource = TriviaSource.BONGO
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Bongo: {jsonResponse}')

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.BONGO

    async def hasQuestionSetAvailable(self) -> bool:
        return True
