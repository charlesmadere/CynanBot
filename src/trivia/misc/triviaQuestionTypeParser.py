from typing import Any

from .triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from ..questions.triviaQuestionType import TriviaQuestionType
from ...misc import utils as utils


class TriviaQuestionTypeParser(TriviaQuestionTypeParserInterface):

    async def parse(
        self,
        triviaQuestionType: str | Any | None,
    ) -> TriviaQuestionType:
        if not utils.isValidStr(triviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')

        triviaQuestionType = triviaQuestionType.lower()

        if triviaQuestionType in { 'bool', 'boolean', 'true-false', 'true_false', 'true false' }:
            return TriviaQuestionType.TRUE_FALSE
        elif triviaQuestionType in { 'multiple', 'multiple-choice', 'multiple_choice', 'multiple choice' }:
            return TriviaQuestionType.MULTIPLE_CHOICE
        elif triviaQuestionType in { 'question-answer', 'question_answer', 'question answer' }:
            return TriviaQuestionType.QUESTION_ANSWER
        else:
            raise ValueError(f'Encountered unknown TriviaQuestionType: \"{triviaQuestionType}\"')

    async def serialize(
        self,
        triviaQuestionType: TriviaQuestionType,
    ) -> str:
        if not isinstance(triviaQuestionType, TriviaQuestionType):
            raise TypeError(f'triviaQuestionType argument is malformed: \"{triviaQuestionType}\"')

        match triviaQuestionType:
            case TriviaQuestionType.MULTIPLE_CHOICE: return 'multiple-choice'
            case TriviaQuestionType.QUESTION_ANSWER: return 'question-answer'
            case TriviaQuestionType.TRUE_FALSE: return 'true-false'
            case _: raise ValueError(f'Encountered unknown TriviaQuestionType: \"{triviaQuestionType}\"')
