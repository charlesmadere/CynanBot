from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
from ...questions.triviaQuestionType import TriviaQuestionType
from ....misc import utils as utils


class BooleanPokepediaTriviaQuestion(PokepediaTriviaQuestion):

    def __init__(
        self,
        correctAnswer: bool,
        pokepediaTriviaType: PokepediaTriviaQuestionType,
        question: str
    ):
        super().__init__(
            pokepediaTriviaType = pokepediaTriviaType,
            question = question
        )

        if not utils.isValidBool(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__correctAnswer: bool = correctAnswer

    def correctAnswer(self) -> bool:
        return self.__correctAnswer

    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.TRUE_FALSE
