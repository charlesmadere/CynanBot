from typing import Any

from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import BadTriviaOriginalCorrectAnswersException, NoTriviaCorrectAnswersException
from ...misc import utils as utils


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        compiledCorrectAnswers: list[str],
        correctAnswers: list[str],
        originalCorrectAnswers: list[str],
        category: str | None,
        categoryId: str | None,
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource
    ):
        super().__init__(
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            triviaSource = triviaSource,
            originalTriviaSource = originalTriviaSource
        )

        if not isinstance(compiledCorrectAnswers, list) or len(compiledCorrectAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'compiledCorrectAnswers argument is malformed: \"{compiledCorrectAnswers}\"')
        elif not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(originalCorrectAnswers, list) or len(originalCorrectAnswers) == 0:
            raise BadTriviaOriginalCorrectAnswersException(f'originalCorrectAnswers argument is malformed: \"{originalCorrectAnswers}\"')

        self.__compiledCorrectAnswers: list[str] = compiledCorrectAnswers
        self.__correctAnswers: list[str] = correctAnswers
        self.__originalCorrectAnswers: list[str] = originalCorrectAnswers

    @property
    def compiledCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__compiledCorrectAnswers)

    @property
    def correctAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)

    @property
    def originalCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__originalCorrectAnswers)

    @property
    def responses(self) -> list[str]:
        return list()

    def toDictionary(self) -> dict[str, Any]:
        return {
            'category': self.category,
            'categoryId': self.categoryId,
            'compiled': self.__compiledCorrectAnswers,
            'correctAnswers': self.__correctAnswers,
            'originalCorrectAnswers': self.__originalCorrectAnswers,
            'originalTriviaSource': self.originalTriviaSource,
            'question': self.question,
            'triviaDifficulty': self.triviaDifficulty,
            'triviaId': self.triviaId,
            'triviaSource': self.triviaSource,
            'triviaType': self.triviaType
        }

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.QUESTION_ANSWER
