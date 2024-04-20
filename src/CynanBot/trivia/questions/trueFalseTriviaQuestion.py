import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import NoTriviaCorrectAnswersException


class TrueFalseTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[bool],
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
            triviaSource = triviaSource,
            triviaType = TriviaQuestionType.TRUE_FALSE
        )

        if not utils.areValidBools(correctAnswers) or not isinstance(correctAnswers, list):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')

        self.__correctAnswers: list[bool] = correctAnswers

    def getCorrectAnswers(self) -> list[str]:
        correctAnswers: list[str] = list()

        for correctAnswer in self.__correctAnswers:
            correctAnswers.append(str(correctAnswer).lower())

        return correctAnswers

    def getCorrectAnswerBools(self) -> list[bool]:
        return utils.copyList(self.__correctAnswers)

    def getPrompt(self, delimiter: str = ' ') -> str:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        return f'True or false! {self.getQuestion()}'

    def getResponses(self) -> list[str]:
        return [ str(True).lower(), str(False).lower() ]
