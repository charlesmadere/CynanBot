import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (
    BadTriviaOriginalCorrectAnswersException, NoTriviaCorrectAnswersException)


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: list[str],
        cleanedCorrectAnswers: list[str],
        category: str | None,
        categoryId: str | None,
        question: str,
        originalCorrectAnswers: list[str],
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
            originalTriviaSource = originalTriviaSource
        )

        if not isinstance(correctAnswers, list) or len(correctAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not isinstance(cleanedCorrectAnswers, list) or len(cleanedCorrectAnswers) == 0:
            raise NoTriviaCorrectAnswersException(f'cleanedCorrectAnswers argument is malformed: \"{cleanedCorrectAnswers}\"')
        elif not isinstance(originalCorrectAnswers, list) or len(originalCorrectAnswers) == 0:
            raise BadTriviaOriginalCorrectAnswersException(f'originalCorrectAnswers argument is malformed: \"{originalCorrectAnswers}\"')

        self.__correctAnswers: list[str] = correctAnswers
        self.__cleanedCorrectAnswers: list[str] = cleanedCorrectAnswers
        self.__originalCorrectAnswers: list[str] = originalCorrectAnswers

    @property
    def cleanedCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__cleanedCorrectAnswers)

    @property
    def correctAnswers(self) -> list[str]:
        return utils.copyList(self.__correctAnswers)

    @property
    def originalCorrectAnswers(self) -> list[str]:
        return utils.copyList(self.__originalCorrectAnswers)

    @property
    def responses(self) -> list[str]:
        return list()

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.QUESTION_ANSWER
