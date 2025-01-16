from frozenlist import FrozenList

from .pokepediaTriviaQuestion import PokepediaTriviaQuestion
from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
from ...questions.triviaQuestionType import TriviaQuestionType
from ....misc import utils as utils


class MultipleChoicePokepediaTriviaQuestion(PokepediaTriviaQuestion):

    def __init__(
        self,
        incorrectAnswers: FrozenList[str],
        pokepediaTriviaType: PokepediaTriviaQuestionType,
        correctAnswer: str,
        question: str
    ):
        super().__init__(
            pokepediaTriviaType = pokepediaTriviaType,
            question = question
        )

        if not isinstance(incorrectAnswers, FrozenList):
            raise TypeError(f'incorrectAnswers argument is malformed: \"{incorrectAnswers}\"')
        elif len(incorrectAnswers) == 0:
            raise ValueError(f'incorrectAnswers argument can\'t be empty: \"{incorrectAnswers}\"')
        elif not utils.isValidStr(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__incorrectAnswers: FrozenList[str] = incorrectAnswers
        self.__correctAnswer: str = correctAnswer

    def correctAnswer(self) -> str:
        return self.__correctAnswer

    def incorrectAnswers(self) -> FrozenList[str]:
        return self.__incorrectAnswers

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.MULTIPLE_CHOICE
