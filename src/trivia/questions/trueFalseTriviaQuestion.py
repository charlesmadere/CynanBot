from typing import Any, Final

from frozenlist import FrozenList

from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import NoTriviaCorrectAnswersException
from ...misc import utils as utils


class TrueFalseTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswer: bool,
        category: str | None,
        categoryId: str | None,
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource,
    ):
        super().__init__(
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            originalTriviaSource = originalTriviaSource,
            triviaSource = triviaSource,
        )

        if not utils.isValidBool(correctAnswer):
            raise NoTriviaCorrectAnswersException(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__correctAnswer: Final[bool] = correctAnswer

    @property
    def correctAnswer(self) -> bool:
        return self.__correctAnswer

    @property
    def correctAnswers(self) -> FrozenList[str]:
        correctAnswers: FrozenList[str] = FrozenList()
        correctAnswers.append(str(self.__correctAnswer).lower())
        correctAnswers.freeze()
        return correctAnswers

    @property
    def responses(self) -> FrozenList[str]:
        responses: FrozenList[str] = FrozenList([ str(True).lower(), str(False).lower() ])
        responses.freeze()
        return responses

    def toDictionary(self) -> dict[str, Any]:
        return {
            'category': self.category,
            'categoryId': self.categoryId,
            'correctAnswer': self.__correctAnswer,
            'correctAnswers': self.correctAnswers,
            'originalTriviaSource': self.originalTriviaSource,
            'question': self.question,
            'responses': self.responses,
            'triviaDifficulty': self.triviaDifficulty,
            'triviaId': self.triviaId,
            'triviaSource': self.triviaSource,
            'triviaType': self.triviaType,
        }

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.TRUE_FALSE
