from typing import Final

from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion
from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty
from ....misc import utils as utils


class BooleanOpenTriviaDatabaseQuestion(OpenTriviaDatabaseQuestion):

    def __init__(
        self,
        correctAnswer: bool,
        category: str | None,
        question: str,
        difficulty: TriviaDifficulty,
    ):
        super().__init__(
            category = category,
            question = question,
            difficulty = difficulty,
        )

        if not utils.isValidBool(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__correctAnswer: Final[bool] = correctAnswer

    @property
    def correctAnswer(self) -> bool:
        return self.__correctAnswer

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.TRUE_FALSE
