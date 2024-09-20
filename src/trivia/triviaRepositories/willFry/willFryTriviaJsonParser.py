from typing import Any

from frozenlist import FrozenList

from .willFryTriviaJsonParserInterface import WillFryTriviaJsonParserInterface
from .willFryTriviaQuestion import WillFryTriviaQuestion
from .willFryTriviaQuestionText import WillFryTriviaQuestionText
from .willFryTriviaQuestionType import WillFryTriviaQuestionType
from ...misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class WillFryTriviaJsonParser(WillFryTriviaJsonParserInterface):

    def __init__(
        self,
        timber: TimberInterface,
        triviaDifficultyParser: TriviaDifficultyParserInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaDifficultyParser, TriviaDifficultyParserInterface):
            raise TypeError(f'triviaDifficultyParser argument is malformed: \"{triviaDifficultyParser}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDifficultyParser: TriviaDifficultyParserInterface = triviaDifficultyParser

    async def parseQuestionText(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> WillFryTriviaQuestionText | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        text = utils.getStrFromDict(jsonContents, 'text')

        return WillFryTriviaQuestionText(
            text = text
        )

    async def parseQuestionType(
        self,
        questionType: str | Any | None
    ) -> WillFryTriviaQuestionType | None:
        if not utils.isValidStr(questionType):
            return None

        questionType = questionType.lower()

        match questionType:
            case 'text_choice': return WillFryTriviaQuestionType.TEXT_CHOICE
            case _:
                self.__timber.log('WillFryTriviaJsonParser', f'Encountered unknown GoogleVoiceAudioEncoding value: \"{questionType}\"')
                return None

    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> WillFryTriviaQuestion | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        isNiche = utils.getBoolFromDict(jsonContents, 'isNiche', fallback = False)

        incorrectAnswersArray: list[str] | Any | None = jsonContents.get('incorrectAnswers')
        incorrectAnswers: list[str] = list()

        if isinstance(incorrectAnswersArray, list) and len(incorrectAnswersArray) >= 1:
            for index, incorrectAnswer in enumerate(incorrectAnswersArray):
                if utils.isValidStr(incorrectAnswer):
                    incorrectAnswers.append(incorrectAnswer)
                else:
                    self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid string at index {index} for \"incorrectAnswers\" field in JSON data: ({jsonContents=})')

        if len(incorrectAnswers) == 0:
            return None

        incorrectAnswers.sort(key = lambda incorrectAnswer: incorrectAnswer.casefold())
        frozenIncorrectAnswers: FrozenList[str] = FrozenList(incorrectAnswers)
        frozenIncorrectAnswers.freeze()

        regionsArray: list[str] | Any | None = jsonContents.get('regions')
        regions: set[str] = set()

        if isinstance(regionsArray, list) and len(regionsArray) >= 1:
            for index, region in enumerate(regionsArray):
                if utils.isValidStr(region):
                    regions.add(region)
                else:
                    self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid string at index {index} for \"regions\" field in JSON data: ({jsonContents=})')

        tagsArray: list[str] | Any | None = jsonContents.get('tags')
        tags: set[str] = set()

        if isinstance(tagsArray, list) and len(tagsArray) >= 1:
            for index, tag in enumerate(tagsArray):
                if utils.isValidStr(tag):
                    tags.add(tag)
                else:
                    self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid string at index {index} for \"tags\" field in JSON data: ({jsonContents=})')

        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category')

        correctAnswer = utils.getStrFromDict(jsonContents, 'correctAnswer')
        triviaId = utils.getStrFromDict(jsonContents, 'id')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        question = await self.parseQuestionText(jsonContents.get('question'))
        if question is None:
            self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid \"question\" field in JSON data: ({jsonContents=})')
            return None

        questionType = await self.parseQuestionType(utils.getStrFromDict(jsonContents, 'type'))
        if questionType is None:
            self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid \"type\" field in JSON data: ({jsonContents=})')
            return None

        return WillFryTriviaQuestion(
            isNiche = isNiche,
            incorrectAnswers = frozenIncorrectAnswers,
            regions = frozenset(regions),
            tags = frozenset(tags),
            category = category,
            correctAnswer = correctAnswer,
            triviaId = triviaId,
            difficulty = difficulty,
            question = question,
            questionType = questionType
        )

    async def parseTriviaQuestions(
        self,
        jsonContents: list[dict[str, Any] | Any | None] | None
    ) -> FrozenList[WillFryTriviaQuestion] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        questions: FrozenList[WillFryTriviaQuestion] = FrozenList()

        for index, questionJson in enumerate(jsonContents):
            question = await self.parseTriviaQuestion(questionJson)

            if question is None:
                self.__timber.log('WillFryTriviaJsonParser', f'Encountered invalid trivia question at index {index} in JSON data: ({jsonContents=})')
            else:
                questions.append(question)

        questions.freeze()
        return questions
