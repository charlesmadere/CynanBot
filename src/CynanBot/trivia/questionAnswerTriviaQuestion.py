from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import NoTriviaCorrectAnswersException
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class QuestionAnswerTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: List[str],
        cleanedCorrectAnswers: List[str],
        category: Optional[str],
        categoryId: Optional[str],
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        triviaSource: TriviaSource
    ):
        super().__init__(
            category = category,
            categoryId = categoryId,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = triviaDifficulty,
            triviaSource = triviaSource,
            triviaType = TriviaType.QUESTION_ANSWER
        )

        if not utils.areValidStrs(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')
        elif not utils.areValidStrs(cleanedCorrectAnswers):
            raise NoTriviaCorrectAnswersException(f'cleanedCorrectAnswers argument is malformed: \"{cleanedCorrectAnswers}\"')

        self.__correctAnswers: List[str] = correctAnswers
        self.__cleanedCorrectAnswers: List[str] = cleanedCorrectAnswers

    def getCorrectAnswers(self) -> List[str]:
        return utils.copyList(self.__correctAnswers)

    def getCleanedCorrectAnswers(self) -> List[str]:
        return utils.copyList(self.__cleanedCorrectAnswers)

    def getPrompt(self, delimiter: str = ' ') -> str:
        if self.hasCategory():
            return f'(category is \"{self.getCategory()}\") {self.getQuestion()}'
        else:
            return self.getQuestion()

    def getResponses(self) -> List[str]:
        return list()
