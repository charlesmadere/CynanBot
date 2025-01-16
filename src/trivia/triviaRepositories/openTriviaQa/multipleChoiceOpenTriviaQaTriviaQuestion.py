from frozenlist import FrozenList

from .openTriviaQaQuestionType import OpenTriviaQaQuestionType
from .openTriviaQaTriviaQuestion import OpenTriviaQaTriviaQuestion
from ....misc import utils as utils


class MultipleChoiceOpenTriviaQaTriviaQuestion(OpenTriviaQaTriviaQuestion):

    def __init__(
        self,
        incorrectAnswers: FrozenList[str],
        category: str | None,
        correctAnswer: str,
        question: str,
        questionId: str
    ):
        super().__init__(
            category = category,
            question = question,
            questionId = questionId
        )

        if not isinstance(incorrectAnswers, FrozenList) or len(incorrectAnswers) == 0:
            raise TypeError(f'incorrectAnswers argument is malformed: \"{incorrectAnswers}\"')
        elif not utils.isValidStr(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__incorrectAnswers: FrozenList[str] = incorrectAnswers
        self.__correctAnswer: str = correctAnswer

    @property
    def correctAnswer(self) -> str:
        return self.__correctAnswer

    @property
    def incorrectAnswers(self) -> FrozenList[str]:
        return self.__incorrectAnswers

    @property
    def questionType(self) -> OpenTriviaQaQuestionType:
        return OpenTriviaQaQuestionType.MULTIPLE_CHOICE
