import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import NoTriviaCorrectAnswersException


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[str],
        cleanedCorrectAnswers: list[str],
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
            triviaSource = triviaSource,
            originalTriviaSource = originalTriviaSource,
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        )

        if not utils.areValidStrs(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not utils.areValidStrs(cleanedCorrectAnswers):
            raise NoTriviaCorrectAnswersException(f'cleanedCorrectAnswers argument is malformed: \"{cleanedCorrectAnswers}\"')

        self.__correctAnswers: list[str] = correctAnswers
        self.__cleanedCorrectAnswers: list[str] = cleanedCorrectAnswers

    def getCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)

    def getCleanedCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__cleanedCorrectAnswers)

    def getPrompt(self, delimiter: str = ' ') -> str:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if self.hasCategory():
            return f'(category is \"{self.getCategory()}\") {self.getQuestion()}'
        else:
            return self.getQuestion()

    def getResponses(self) -> list[str]:
        return list()
