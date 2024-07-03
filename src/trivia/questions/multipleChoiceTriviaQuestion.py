from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (NoTriviaCorrectAnswersException,
                                     NoTriviaMultipleChoiceResponsesException)
from ...misc import utils as utils


class MultipleChoiceTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[str],
        multipleChoiceResponses: list[str],
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
            originalTriviaSource = originalTriviaSource,
            triviaSource = triviaSource
        )

        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(multipleChoiceResponses, list) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        self.__correctAnswers: list[str] = correctAnswers
        self.__multipleChoiceResponses: list[str] = multipleChoiceResponses

    @property
    def correctAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)

    @property
    def indexesWithCorrectAnswers(self) -> dict[int, str]:
        indexesWithCorrectAnswers: dict[int, str] = dict()

        for index, response in enumerate(self.__multipleChoiceResponses):
            for correctAnswer in self.__correctAnswers:
                if response.casefold() == correctAnswer.casefold():
                    indexesWithCorrectAnswers[index] = response

        return indexesWithCorrectAnswers

    @property
    def responses(self) -> list[str]:
        return utils.copyList(self.__multipleChoiceResponses)

    @property
    def responseCount(self) -> int:
        return len(self.__multipleChoiceResponses)

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.MULTIPLE_CHOICE
