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

        if not utils.isValidBool(correctAnswer):
            raise NoTriviaCorrectAnswersException(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__correctAnswer: bool = correctAnswer

    @property
    def correctAnswer(self) -> bool:
        return self.__correctAnswer

    @property
    def correctAnswers(self) -> list[str]:
        return [ str(self.__correctAnswer).lower() ]

    @property
    def responses(self) -> list[str]:
        return [ str(True).lower(), str(False).lower() ]

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.TRUE_FALSE
