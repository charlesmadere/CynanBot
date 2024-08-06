from typing import Any

from .booleanOpenTriviaDatabaseQuestion import BooleanOpenTriviaDatabaseQuestion
from .multipleOpenTriviaDatabaseQuestion import MultipleOpenTriviaDatabaseQuestion
from .openTriviaDatabaseJsonParserInterface import OpenTriviaDatabaseJsonParserInterface
from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseSessionToken import OpenTriviaDatabaseSessionToken
from ...misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from ...misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from ...questions.triviaQuestionType import TriviaQuestionType
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class OpenTriviaDatabaseJsonParser(OpenTriviaDatabaseJsonParserInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaDifficultyParser: TriviaDifficultyParserInterface,
        triviaQuestionTypeParser: TriviaQuestionTypeParserInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaDifficultyParser, TriviaDifficultyParserInterface):
            raise TypeError(f'triviaDifficultyParser argument is malformed: \"{triviaDifficultyParser}\"')
        elif not isinstance(triviaQuestionTypeParser, TriviaQuestionTypeParserInterface):
            raise TypeError(f'triviaQuestionTypeParser argument is malformed: \"{triviaQuestionTypeParser}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDifficultyParser: TriviaDifficultyParserInterface = triviaDifficultyParser
        self.__triviaQuestionTypeParser: TriviaQuestionTypeParserInterface = triviaQuestionTypeParser

    async def __parseBooleanTriviaQuestion(
        self,
        jsonContents: dict[str, Any]
    ) -> BooleanOpenTriviaDatabaseQuestion:
        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category')

        correctAnswer = utils.getBoolFromDict(jsonContents, 'correct_answer')
        question = utils.getStrFromDict(jsonContents, 'question')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        return BooleanOpenTriviaDatabaseQuestion(
            correctAnswer = correctAnswer,
            category = category,
            question = question,
            difficulty = difficulty
        )

    async def __parseMultipleTriviaQuestion(
        self,
        jsonContents: dict[str, Any]
    ) -> MultipleOpenTriviaDatabaseQuestion | None:
        incorrectAnswersArray: list[str | Any | None] | None = jsonContents.get('incorrect_answers')
        if not isinstance(incorrectAnswersArray, list) or len(incorrectAnswersArray) == 0:
            self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered missing/invalid \"incorrect_answers\" field in JSON data: ({jsonContents=})')
            return None

        incorrectAnswers: list[str] = list()
        for index, incorrectAnswer in enumerate(incorrectAnswersArray):
            if utils.isValidStr(incorrectAnswer):
                incorrectAnswers.append(incorrectAnswer)
            else:
                self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered malformed value at index {index} for \"incorrect_answers\" field in JSON data: ({jsonContents=}) ({incorrectAnswer=})')

        if len(incorrectAnswers) == 0:
            self.__timber.log('OpenTriviaDatabaseJsonParser', f'Unable to build up any incorrect answers from JSON data: ({jsonContents=})')
            return None

        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category')

        correctAnswer = utils.getStrFromDict(jsonContents, 'correct_answer')
        question = utils.getStrFromDict(jsonContents, 'question')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        return MultipleOpenTriviaDatabaseQuestion(
            incorrectAnswers = incorrectAnswers,
            category = category,
            correctAnswer = correctAnswer,
            question = question,
            difficulty = difficulty
        )

    async def parseSessionToken(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseSessionToken | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        responseCode = utils.getIntFromDict(jsonContents, 'response_code')
        responseMessage = utils.getStrFromDict(jsonContents, 'response_message')
        token = utils.getStrFromDict(jsonContents, 'token')

        return OpenTriviaDatabaseSessionToken(
            responseCode = responseCode,
            responseMessage = responseMessage,
            token = token
        )

    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseQuestion | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        questionType = await self.__triviaQuestionTypeParser.parse(utils.getStrFromDict(jsonContents, 'type'))

        match questionType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                return await self.__parseMultipleTriviaQuestion(jsonContents)

            case TriviaQuestionType.TRUE_FALSE:
                return await self.__parseBooleanTriviaQuestion(jsonContents)

            case _:
                self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered unexpected TriviaQuestionType when trying to parse AbsOpenTriviaDatabaseQuestion ({questionType=}) ({jsonContents=})')
                return None
