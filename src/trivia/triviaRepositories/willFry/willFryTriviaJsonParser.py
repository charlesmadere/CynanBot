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

        incorrectAnswers: FrozenList[str] = FrozenList()
        incorrectAnswers.freeze()

        regions: FrozenList[str] = FrozenList()
        regions.freeze()

        tags: FrozenList[str] = FrozenList()
        tags.freeze()

        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category')

        correctAnswer = utils.getStrFromDict(jsonContents, 'correctAnswer')
        triviaId = utils.getStrFromDict(jsonContents, 'id')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))
        question = await self.parseQuestionText(jsonContents.get('question'))
        questionType = await self.parseQuestionType(utils.getStrFromDict(jsonContents, 'type'))

        return WillFryTriviaQuestion(
            isNiche = isNiche,
            incorrectAnswers = incorrectAnswers,
            regions = regions,
            tags = tags,
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
        questions.freeze()

        return questions
