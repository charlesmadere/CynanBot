from .openTriviaDatabaseQuestion import OpenTriviaDatabaseQuestion

from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty
from ....misc import utils as utils


class MultipleOpenTriviaDatabaseQuestion(OpenTriviaDatabaseQuestion):

    def __init__(
        self,
        incorrectAnswers: list[str],
        category: str | None,
        correctAnswer: str,
        question: str,
        difficulty: TriviaDifficulty
    ):
        super().__init__(
            category = category,
            question = question,
            difficulty = difficulty
        )

        if not isinstance(incorrectAnswers, list) or len(incorrectAnswers) == 0:
            raise TypeError(f'incorrectAnswers argument is malformed: \"{incorrectAnswers}\"')
        elif not utils.isValidStr(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__incorrectAnswers: list[str] = incorrectAnswers
        self.__correctAnswer: str = correctAnswer

    @property
    def correctAnswer(self) -> str:
        return self.__correctAnswer

    @property
    def incorrectAnswers(self) -> list[str]:
        return self.__incorrectAnswers

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.MULTIPLE_CHOICE
