from typing import Any

from frozenlist import FrozenList

from .bongoJsonParserInterface import BongoJsonParserInterface
from .bongoTriviaQuestion import BongoTriviaQuestion
from .booleanBongoTriviaQuestion import BooleanBongoTriviaQuestion
from .multipleBongoTriviaQuestion import MultipleBongoTriviaQuestion
from ...misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from ...misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from ...questions.triviaQuestionType import TriviaQuestionType
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class BongoJsonParser(BongoJsonParserInterface):

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
    ) -> BooleanBongoTriviaQuestion:
        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category', clean = True, htmlUnescape = True)

        correctAnswer = utils.getBoolFromDict(jsonContents, 'correct_answer')
        question = utils.getStrFromDict(jsonContents, 'question', clean = True, htmlUnescape = True)
        triviaId = utils.getStrFromDict(jsonContents, 'id')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        return BooleanBongoTriviaQuestion(
            correctAnswer = correctAnswer,
            category = category,
            question = question,
            triviaId = triviaId,
            difficulty = difficulty
        )

    async def __parseMultipleTriviaQuestion(
        self,
        jsonContents: dict[str, Any]
    ) -> MultipleBongoTriviaQuestion | None:
        incorrectAnswersArray: list[str | Any | None] | None = jsonContents.get('incorrect_answers')
        if not isinstance(incorrectAnswersArray, list) or len(incorrectAnswersArray) == 0:
            self.__timber.log('BongoJsonParser', f'Encountered missing/invalid \"incorrect_answers\" field in JSON data: ({jsonContents=})')
            return None

        incorrectAnswers: FrozenList[str] = FrozenList()
        for index, incorrectAnswer in enumerate(incorrectAnswersArray):
            if utils.isValidStr(incorrectAnswer):
                incorrectAnswers.append(utils.cleanStr(incorrectAnswer, htmlUnescape = True))
            else:
                self.__timber.log('BongoJsonParser', f'Encountered malformed value at index {index} for \"incorrect_answers\" field in JSON data: ({jsonContents=}) ({incorrectAnswer=})')

        incorrectAnswers.freeze()

        if len(incorrectAnswers) == 0:
            self.__timber.log('BongoJsonParser', f'Unable to build up any incorrect answers from JSON data: ({jsonContents=})')
            return None

        category: str | None = None
        if 'category' in jsonContents and utils.isValidStr(jsonContents.get('category')):
            category = utils.getStrFromDict(jsonContents, 'category', clean = True, htmlUnescape = True)

        correctAnswer = utils.getStrFromDict(jsonContents, 'correct_answer', clean = True, htmlUnescape = True)
        question = utils.getStrFromDict(jsonContents, 'question', clean = True, htmlUnescape = True)
        triviaId = utils.getStrFromDict(jsonContents, 'id')
        difficulty = await self.__triviaDifficultyParser.parse(utils.getStrFromDict(jsonContents, 'difficulty'))

        return MultipleBongoTriviaQuestion(
            incorrectAnswers = incorrectAnswers,
            category = category,
            correctAnswer = correctAnswer,
            question = question,
            triviaId = triviaId,
            difficulty = difficulty
        )

    async def parseTriviaQuestion(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> BongoTriviaQuestion | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        triviaType = await self.__triviaQuestionTypeParser.parse(utils.getStrFromDict(jsonContents, 'type'))

        match triviaType:
            case TriviaQuestionType.MULTIPLE_CHOICE:
                return await self.__parseMultipleTriviaQuestion(jsonContents)

            case TriviaQuestionType.TRUE_FALSE:
                return await self.__parseBooleanTriviaQuestion(jsonContents)

            case _:
                self.__timber.log('BongoJsonParser', f'Encountered unexpected TriviaQuestionType when trying to parse BongoTriviaQuestion ({triviaType=}) ({jsonContents=})')
                return None

    async def parseTriviaQuestions(
        self,
        jsonContents: list[dict[str, Any] | None] | Any | None
    ) -> FrozenList[BongoTriviaQuestion] | None:
        if not isinstance(jsonContents, list) or len(jsonContents) == 0:
            return None

        questions: FrozenList[BongoTriviaQuestion] = FrozenList()

        for index, questionJson in enumerate(jsonContents):
            question = await self.parseTriviaQuestion(questionJson)

            if question is None:
                self.__timber.log('BongoJsonParser', f'Encountered malformed value at index {index} in JSON data: ({jsonContents=})')
            else:
                questions.append(question)

        questions.freeze()
        return questions
