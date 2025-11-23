from typing import Any, Final

from frozenlist import FrozenList

from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import BadTriviaOriginalCorrectAnswersException, NoTriviaCorrectAnswersException
from ...misc import utils as utils


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        allWords: frozenset[str] | None,
        compiledCorrectAnswers: list[str],
        correctAnswers: list[str],
        originalCorrectAnswers: list[str],
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
            triviaSource = triviaSource,
            originalTriviaSource = originalTriviaSource,
        )

        if allWords is not None and not isinstance(allWords, frozenset):
            raise TypeError(f'allWords argument is malformed: \"{allWords}\"')
        elif not isinstance(compiledCorrectAnswers, list) or len(compiledCorrectAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'compiledCorrectAnswers argument is malformed: \"{compiledCorrectAnswers}\"')
        elif not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(originalCorrectAnswers, list) or len(originalCorrectAnswers) == 0:
            raise BadTriviaOriginalCorrectAnswersException(f'originalCorrectAnswers argument is malformed: \"{originalCorrectAnswers}\"')

        self.__allWords: Final[frozenset[str] | None] = allWords
        self.__compiledCorrectAnswers: Final[list[str]] = compiledCorrectAnswers
        self.__correctAnswers: Final[list[str]] = correctAnswers
        self.__originalCorrectAnswers: Final[list[str]] = originalCorrectAnswers

    @property
    def allWords(self) -> frozenset[str] | None:
        return self.__allWords

    @property
    def compiledCorrectAnswers(self) -> FrozenList[str]:
        frozenCompiledCorrectAnswers: FrozenList[str] = FrozenList(self.__compiledCorrectAnswers)
        frozenCompiledCorrectAnswers.freeze()
        return frozenCompiledCorrectAnswers

    @property
    def correctAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)

    @property
    def originalCorrectAnswers(self) -> FrozenList[str]:
        frozenOriginalCorrectAnswers: FrozenList[str] = FrozenList(self.__originalCorrectAnswers)
        frozenOriginalCorrectAnswers.freeze()
        return frozenOriginalCorrectAnswers

    @property
    def responses(self) -> list[str]:
        return list()

    def toDictionary(self) -> dict[str, Any]:
        return {
            'allWords': self.allWords,
            'category': self.category,
            'categoryId': self.categoryId,
            'compiledCorrectAnswers': self.__compiledCorrectAnswers,
            'correctAnswers': self.__correctAnswers,
            'originalCorrectAnswers': self.__originalCorrectAnswers,
            'originalTriviaSource': self.originalTriviaSource,
            'question': self.question,
            'triviaDifficulty': self.triviaDifficulty,
            'triviaId': self.triviaId,
            'triviaSource': self.triviaSource,
            'triviaType': self.triviaType,
        }

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.QUESTION_ANSWER
