import traceback
from typing import Any, Dict, List, Optional, Set, Tuple

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
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
                                              NoTriviaCorrectAnswersException,
                                              UnsupportedTriviaTypeException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class QuizApiTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        quizApiKey: str,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        if not utils.isValidStr(quizApiKey):
            raise ValueError(f'quizApiKey argument is malformed: \"{quizApiKey}\"')
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__quizApiKey: str = quizApiKey
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('QuizApiTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://quizapi.io/api/v1/questions?apiKey={self.__quizApiKey}&limit=1',
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0' # LOOOOL
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.getTriviaSource(), e)

        if response.getStatusCode() != 200:
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Encountered non-200 HTTP status code when fetching trivia question: \"{response.getStatusCode()}\"')
            raise GenericTriviaNetworkException(self.getTriviaSource())

        jsonResponse: Optional[List[Dict[str, Any]]] = await response.json()
        await response.close()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('QuizApiTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse):
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Rejecting Quiz API\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Quiz API JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: Optional[Dict[str, Any]] = jsonResponse[0]
        if not utils.hasItems(triviaJson):
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Rejecting Quiz API\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Quiz API\'s JSON data due to null/empty contents: {jsonResponse}')

        triviaDifficulty = TriviaDifficulty.fromStr(utils.getStrFromDict(triviaJson, 'difficulty', fallback = ''))
        category = utils.getStrFromDict(triviaJson, 'category', fallback = '', clean = True)
        question = utils.getStrFromDict(triviaJson, 'question', clean = True)

        # this API seems to only ever give multiple choice, so for now, we're just hardcoding this
        triviaType = TriviaQuestionType.MULTIPLE_CHOICE

        triviaId = utils.getStrFromDict(triviaJson, 'id', fallback = '')
        if not utils.isValidStr(triviaId):
            triviaId = await self.__triviaIdGenerator.generateQuestionId(
                question = question,
                category = category,
                difficulty = triviaDifficulty.toStr()
            )

        answersJson: Dict[str, str] = triviaJson['answers']
        answersList: List[Tuple[str, str]] = list(answersJson.items())
        answersList.sort(key = lambda entry: entry[0].lower())

        correctAnswersJson: Dict[str, str] = triviaJson['correct_answers']
        correctAnswersList: List[Tuple[str, str]] = list(correctAnswersJson.items())
        correctAnswersList.sort(key = lambda entry: entry[0].lower())

        if not utils.hasItems(answersList) or not utils.hasItems(correctAnswersList) or len(answersList) != len(correctAnswersList):
            raise MalformedTriviaJsonException(f'Rejecting Quiz API\'s data due to malformed \"answers\" and/or \"correct_answers\" data: {jsonResponse}')

        correctAnswers: List[str] = list()
        filteredAnswers: List[str] = list()

        for index, pair in enumerate(answersList):
            if utils.isValidStr(pair[0]) and utils.isValidStr(pair[1]):
                filteredAnswers.append(pair[1])
                correctAnswerPair: Tuple[str, str] = correctAnswersList[index]

                if utils.strToBool(correctAnswerPair[1]):
                    correctAnswers.append(pair[1])

        if not utils.hasItems(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'Rejecting Quiz API\'s JSON data due to there being no correct answers: {jsonResponse}')

        multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
            correctAnswers = correctAnswers,
            multipleChoiceResponses = filteredAnswers
        )

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            if await self._verifyIsActuallyMultipleChoiceQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses
            ):
                return MultipleChoiceTriviaQuestion(
                    correctAnswers = correctAnswers,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    triviaSource = TriviaSource.QUIZ_API
                )
            else:
                self.__timber.log('QuizApiTriviaQuestionRepository', f'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            return TrueFalseTriviaQuestion(
                correctAnswers = utils.strsToBools(correctAnswers),
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.QUIZ_API
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Quiz API: {jsonResponse}')

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.QUIZ_API

    async def hasQuestionSetAvailable(self) -> bool:
        return True
