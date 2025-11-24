from typing import Any, Final

from frozendict import frozendict
from frozenlist import FrozenList

from .absTriviaQuestion import AbsTriviaQuestion
from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException


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

        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(multipleChoiceResponses, list) or len(multipleChoiceResponses) == 0:
            raise NoTriviaMultipleChoiceResponsesException(f'multipleChoiceResponses argument is malformed: \"{multipleChoiceResponses}\"')

        self.__correctAnswers: Final[list[str]] = correctAnswers
        self.__multipleChoiceResponses: Final[list[str]] = multipleChoiceResponses

    @property
    def correctAnswers(self) -> FrozenList[str]:
        correctAnswers: FrozenList[str] = FrozenList(self.__correctAnswers)
        correctAnswers.freeze()
        return correctAnswers

    @property
    def indexesWithCorrectAnswers(self) -> frozendict[int, str]:
        indexesWithCorrectAnswers: dict[int, str] = dict()

        for index, response in enumerate(self.__multipleChoiceResponses):
            for correctAnswer in self.__correctAnswers:
                if response.casefold() == correctAnswer.casefold():
                    indexesWithCorrectAnswers[index] = response

        return frozendict(indexesWithCorrectAnswers)

    @property
    def responses(self) -> FrozenList[str]:
        responses: FrozenList[str] = FrozenList(self.__multipleChoiceResponses)
        responses.freeze()
        return responses

    @property
    def responseCount(self) -> int:
        return len(self.__multipleChoiceResponses)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'category': self.category,
            'categoryId': self.categoryId,
            'correctAnswers': self.__correctAnswers,
            'indexesWithCorrectAnswers': self.indexesWithCorrectAnswers,
            'originalTriviaSource': self.originalTriviaSource,
            'question': self.question,
            'responses': self.__multipleChoiceResponses,
            'responseCount': self.responseCount,
            'triviaDifficulty': self.triviaDifficulty,
            'triviaId': self.triviaId,
            'triviaSource': self.triviaSource,
            'triviaType': self.triviaType,
        }

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.MULTIPLE_CHOICE
