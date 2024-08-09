from typing import Any

from frozenlist import FrozenList

from .booleanOpenTriviaDatabaseQuestion import BooleanOpenTriviaDatabaseQuestion
from .multipleOpenTriviaDatabaseQuestion import MultipleOpenTriviaDatabaseQuestion
from .openTriviaDatabaseJsonParserInterface import OpenTriviaDatabaseJsonParserInterface
from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from .openTriviaDatabaseQuestionsResponse import OpenTriviaDatabaseQuestionsResponse
from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode
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
            category = utils.getStrFromDict(jsonContents, 'category', clean = True, htmlUnescape = True)

        correctAnswer = utils.getBoolFromDict(jsonContents, 'correct_answer')
        question = utils.getStrFromDict(jsonContents, 'question', clean = True, htmlUnescape = True)
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

        incorrectAnswers: FrozenList[str] = FrozenList()
        for index, incorrectAnswer in enumerate(incorrectAnswersArray):
            if utils.isValidStr(incorrectAnswer):
                incorrectAnswers.append(utils.cleanStr(incorrectAnswer, htmlUnescape = True))
            else:
                self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered malformed value at index {index} for \"incorrect_answers\" field in JSON data: ({jsonContents=}) ({incorrectAnswer=})')

        incorrectAnswers.freeze()

        if len(incorrectAnswers) == 0:
            self.__timber.log('OpenTriviaDatabaseJsonParser', f'Unable to build up any incorrect answers from JSON data: ({jsonContents=})')
            return None

        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category', clean = True, htmlUnescape = True)

        correctAnswer = utils.getStrFromDict(jsonContents, 'correct_answer', clean = True, htmlUnescape = True)
        question = utils.getStrFromDict(jsonContents, 'question', clean = True, htmlUnescape = True)
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        return MultipleOpenTriviaDatabaseQuestion(
            incorrectAnswers = incorrectAnswers,
            category = category,
            correctAnswer = correctAnswer,
            question = question,
            difficulty = difficulty
        )

    async def parseQuestionsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseQuestionsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        responseCode = await self.requireResponseCode(utils.getIntFromDict(jsonContents, 'response_code'))

        if responseCode is not OpenTriviaDatabaseResponseCode.SUCCESS:
            return OpenTriviaDatabaseQuestionsResponse(
                results = None,
                responseCode = responseCode
            )

        resultsArray: list[dict[str, Any] | None] | None = jsonContents.get('results')
        results: FrozenList[OpenTriviaDatabaseQuestion] | None = None

        if isinstance(resultsArray, list) and len(resultsArray) >= 1:
            results = FrozenList()

            for index, resultEntryJson in enumerate(resultsArray):
                triviaQuestion = await self.parseTriviaQuestion(resultEntryJson)

                if triviaQuestion is None:
                    self.__timber.log('OpenTriviaDatabaseJsonParser', f'Unable to parse value at index {index} for \"results\" field in JSON data: ({jsonContents=})')
                else:
                    results.append(triviaQuestion)

        results.freeze()

        return OpenTriviaDatabaseQuestionsResponse(
            results = results,
            responseCode = responseCode
        )

    async def parseResponseCode(
        self,
        responseCode: int | Any | None
    ) -> OpenTriviaDatabaseResponseCode | None:
        if not utils.isValidInt(responseCode):
            return None

        match responseCode:
            case 0: return OpenTriviaDatabaseResponseCode.SUCCESS
            case 1: return OpenTriviaDatabaseResponseCode.NO_RESULTS
            case 2: return OpenTriviaDatabaseResponseCode.INVALID_PARAMETER
            case 3: return OpenTriviaDatabaseResponseCode.TOKEN_NOT_FOUND
            case 4: return OpenTriviaDatabaseResponseCode.TOKEN_EMPTY
            case 5: return OpenTriviaDatabaseResponseCode.RATE_LIMIT
            case _:
                self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered unknown OpenTriviaDatabaseResponseCode value: \"{responseCode}\"')
                return None

    async def parseSessionToken(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenTriviaDatabaseSessionToken | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        responseCode = await self.requireResponseCode(utils.getIntFromDict(jsonContents, 'response_code'))

        responseMessage: str | None = None
        if 'response_message' in jsonContents and utils.isValidStr(jsonContents.get('response_message')):
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

        triviaType = await self.__triviaQuestionTypeParser.parse(utils.getStrFromDict(jsonContents, 'type'))

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                return await self.__parseMultipleTriviaQuestion(jsonContents)

            case TriviaQuestionType.TRUE_FALSE:
                return await self.__parseBooleanTriviaQuestion(jsonContents)

            case _:
                self.__timber.log('OpenTriviaDatabaseJsonParser', f'Encountered unexpected TriviaQuestionType when trying to parse OpenTriviaDatabaseQuestion ({triviaType=}) ({jsonContents=})')
                return None

    async def requireResponseCode(
        self,
        responseCode: int | Any | None
    ) -> OpenTriviaDatabaseResponseCode:
        result = await self.parseResponseCode(responseCode)

        if result is None:
            raise ValueError(f'Unable to parse \"{responseCode}\" into OpenTriviaDatabaseResponseCode value!')

        return result
