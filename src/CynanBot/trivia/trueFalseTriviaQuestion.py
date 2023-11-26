from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import NoTriviaCorrectAnswersException
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class TrueFalseTriviaQuestion(AbsTriviaQuestion):

    def __init__(
        self,
        correctAnswers: List[bool],
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
            triviaType = TriviaType.TRUE_FALSE
        )

        if not utils.areValidBools(correctAnswers):
            raise NoTriviaCorrectAnswersException(f'correctAnswers argument is malformed: \"{correctAnswers}\"')

        self.__correctAnswers: List[bool] = correctAnswers

    def getCorrectAnswers(self) -> List[str]:
        correctAnswers: List[str] = list()

        for correctAnswer in self.__correctAnswers:
            correctAnswers.append(str(correctAnswer).lower())

        return correctAnswers

    def getCorrectAnswerBools(self) -> List[bool]:
        return self.__correctAnswers

    def getPrompt(self, delimiter: str = ' ') -> str:
        return f'True or false! {self.getQuestion()}'

    def getResponses(self) -> List[str]:
        return [ str(True).lower(), str(False).lower() ]
