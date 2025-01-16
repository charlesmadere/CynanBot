from .openTriviaQaQuestionType import OpenTriviaQaQuestionType
from .openTriviaQaTriviaQuestion import OpenTriviaQaTriviaQuestion
from ....misc import utils as utils


class BooleanOpenTriviaQaTriviaQuestion(OpenTriviaQaTriviaQuestion):

    def __init__(
        self,
        correctAnswer: bool,
        category: str | None,
        question: str,
        questionId: str
    ):
        super().__init__(
            category = category,
            question = question,
            questionId = questionId
        )

        if not utils.isValidBool(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__correctAnswer: bool = correctAnswer

    @property
    def correctAnswer(self) -> bool:
        return self.__correctAnswer

    @property
    def questionType(self) -> OpenTriviaQaQuestionType:
        return OpenTriviaQaQuestionType.BOOLEAN
