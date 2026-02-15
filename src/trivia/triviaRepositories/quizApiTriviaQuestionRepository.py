import traceback
from typing import Any

from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (GenericTriviaNetworkException,
                                MalformedTriviaJsonException,
                                NoTriviaCorrectAnswersException,
                                UnsupportedTriviaTypeException)
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class QuizApiTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        quizApiKey: str,
        timber: TimberInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaSettings: TriviaSettingsInterface,
    ):
        super().__init__(
            triviaSettings = triviaSettings,
        )

        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not utils.isValidStr(quizApiKey):
            raise TypeError(f'quizApiKey argument is malformed: \"{quizApiKey}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__quizApiKey: str = quizApiKey
        self.__timber: TimberInterface = timber
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('QuizApiTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://quizapi.io/api/v1/questions?apiKey={self.__quizApiKey}&limit=1',
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0'  # LOOOOL
                }
            )
        except GenericNetworkException as e:
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Encountered network error when fetching trivia question: {e}', e, traceback.format_exc())
            raise GenericTriviaNetworkException(self.triviaSource, e)

        if response.statusCode != 200:
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Encountered non-200 HTTP status code when fetching trivia question: \"{response.statusCode}\"')
            raise GenericTriviaNetworkException(self.triviaSource)

        jsonResponse = await response.json()
        await response.close()

        if await self._triviaSettings.isDebugLoggingEnabled():
            self.__timber.log('QuizApiTriviaQuestionRepository', f'{jsonResponse}')

        if not utils.hasItems(jsonResponse) or not isinstance(jsonResponse, list):
            self.__timber.log('QuizApiTriviaQuestionRepository', f'Rejecting Quiz API\'s JSON data due to null/empty contents: {jsonResponse}')
            raise MalformedTriviaJsonException(f'Rejecting Quiz API JSON data due to null/empty contents: {jsonResponse}')

        triviaJson: dict[str, Any] | None = jsonResponse[0]
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

        answersJson: dict[str, str] = triviaJson['answers']
        answersList: list[tuple[str, str]] = list(answersJson.items())
        answersList.sort(key = lambda entry: entry[0].lower())

        correctAnswersJson: dict[str, str] = triviaJson['correct_answers']
        correctAnswersList: list[tuple[str, str]] = list(correctAnswersJson.items())
        correctAnswersList.sort(key = lambda entry: entry[0].lower())

        if not utils.hasItems(answersList) or not utils.hasItems(correctAnswersList) or len(answersList) != len(correctAnswersList):
            raise MalformedTriviaJsonException(f'Rejecting Quiz API\'s data due to malformed \"answers\" and/or \"correct_answers\" data: {jsonResponse}')

        correctAnswers: list[str] = list()
        filteredAnswers: list[str] = list()

        for index, pair in enumerate(answersList):
            if utils.isValidStr(pair[0]) and utils.isValidStr(pair[1]):
                filteredAnswers.append(pair[1])
                correctAnswerPair: tuple[str, str] = correctAnswersList[index]

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
                multipleChoiceResponses = multipleChoiceResponses,
            ):
                return MultipleChoiceTriviaQuestion(
                    correctAnswers = correctAnswers,
                    multipleChoiceResponses = multipleChoiceResponses,
                    category = category,
                    categoryId = None,
                    question = question,
                    triviaId = triviaId,
                    triviaDifficulty = triviaDifficulty,
                    originalTriviaSource = None,
                    triviaSource = self.triviaSource
                )
            else:
                self.__timber.log('QuizApiTriviaQuestionRepository', 'Encountered a multiple choice question that is better suited for true/false')
                triviaType = TriviaQuestionType.TRUE_FALSE

        if triviaType is TriviaQuestionType.TRUE_FALSE:
            return TrueFalseTriviaQuestion(
                correctAnswer = utils.strictStrToBool(correctAnswers[0]),
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = triviaDifficulty,
                originalTriviaSource = None,
                triviaSource = self.triviaSource
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Quiz API: {jsonResponse}')

    async def hasQuestionSetAvailable(self) -> bool:
        return True

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.QUIZ_API
