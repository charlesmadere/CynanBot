from typing import Any

from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (BadTriviaAnswerAddendumException,
                                BadTriviaOriginalCorrectAnswersException,
                                NoTriviaCorrectAnswersException)
from ...misc import utils as utils


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[str],
        cleanedCorrectAnswers: list[str],
        category: str | None,
        categoryId: str | None,
        question: str,
        originalCorrectAnswers: list[str],
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource,
        answerAddendum: str | None = None
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

        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(cleanedCorrectAnswers, list) or len(cleanedCorrectAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'cleanedCorrectAnswers argument is malformed: \"{cleanedCorrectAnswers}\"')
        elif not isinstance(originalCorrectAnswers, list) or len(originalCorrectAnswers) == 0:
            raise BadTriviaOriginalCorrectAnswersException(f'originalCorrectAnswers argument is malformed: \"{originalCorrectAnswers}\"')
        elif answerAddendum is not None and not isinstance(answerAddendum, str):
            raise BadTriviaAnswerAddendumException(f'answerAddendum argument is malformed: \"{answerAddendum}\"')

        self.__correctAnswers: list[str] = correctAnswers
        self.__cleanedCorrectAnswers: list[str] = cleanedCorrectAnswers
        self.__originalCorrectAnswers: list[str] = originalCorrectAnswers
        self.__answerAddendum: str | None = answerAddendum

    @property
    def answerAddendum(self) -> str | None:
        return self.__answerAddendum

    @property
    def cleanedCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__cleanedCorrectAnswers)

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
            'answerAddendum': self.answerAddendum,
            'category': self.category,
            'categoryId': self.categoryId,
            'cleanedCorrectAnswers': self.cleanedCorrectAnswers,
            'correctAnswers': self.correctAnswers,
            'originalCorrectAnswers': self.originalCorrectAnswers,
            'originalTriviaSource': self.originalTriviaSource,
            'question': self.question,
            'responses': self.responses,
            'triviaDifficulty': self.triviaDifficulty,
            'triviaId': self.triviaId,
            'triviaSource': self.triviaSource,
            'triviaType': self.triviaType
        }

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.QUESTION_ANSWER
