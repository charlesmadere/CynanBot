from enum import Enum, auto

from ...misc import utils as utils


class TriviaQuestionType(Enum):

    MULTIPLE_CHOICE = auto()
    QUESTION_ANSWER = auto()
    TRUE_FALSE = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text in { 'bool', 'boolean', 'true-false', 'true_false', 'true false' }:
            return TriviaQuestionType.TRUE_FALSE
        elif text in { 'multiple', 'multiple-choice', 'multiple_choice', 'multiple choice' }:
            return TriviaQuestionType.MULTIPLE_CHOICE
        elif text in { 'question-answer', 'question_answer', 'question answer' }:
            return TriviaQuestionType.QUESTION_ANSWER
        else:
            raise ValueError(f'unknown TriviaQuestionType: \"{text}\"')

    def toStr(self) -> str:
        match self:
            case TriviaQuestionType.MULTIPLE_CHOICE: return 'multiple-choice'
            case TriviaQuestionType.QUESTION_ANSWER: return 'question-answer'
            case TriviaQuestionType.TRUE_FALSE: return 'true-false'
            case _: raise RuntimeError(f'unknown TriviaQuestionType: \"{self}\"')
