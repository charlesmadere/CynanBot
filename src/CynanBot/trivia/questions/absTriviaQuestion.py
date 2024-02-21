from abc import ABC, abstractmethod
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import (BadTriviaDifficultyException,
                                              BadTriviaIdException,
                                              BadTriviaSourceException,
                                              BadTriviaTypeException,
                                              NoTriviaQuestionException)


class AbsTriviaQuestion(ABC):

    def __init__(
        self,
        category: Optional[str],
        categoryId: Optional[str],
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ):
        if not utils.isValidStr(question):
            raise NoTriviaQuestionException(f'question argument is malformed: \"{question}\"')
        if not utils.isValidStr(triviaId):
            raise BadTriviaIdException(f'triviaId argument is malformed: \"{triviaId}\"')
        assert isinstance(triviaDifficulty, TriviaDifficulty), f"malformed {triviaDifficulty=}"
        assert isinstance(triviaSource, TriviaSource), f"malformed {triviaSource=}"
        assert isinstance(triviaType, TriviaQuestionType), f"malformed {triviaType=}"

        self.__category: Optional[str] = category
        self.__categoryId: Optional[str] = categoryId
        self.__question: str = question
        self.__triviaId: str = triviaId
        self.__triviaDifficulty: TriviaDifficulty = triviaDifficulty
        self.__triviaSource: TriviaSource = triviaSource
        self.__triviaType: TriviaQuestionType = triviaType

    def getCategory(self) -> Optional[str]:
        return self.__category

    def getCategoryId(self) -> Optional[str]:
        return self.__categoryId

    @abstractmethod
    def getCorrectAnswers(self) -> List[str]:
        pass

    @abstractmethod
    def getPrompt(self, delimiter: str = ' ') -> str:
        pass

    def getQuestion(self) -> str:
        return self.__question

    @abstractmethod
    def getResponses(self) -> List[str]:
        pass

    def getTriviaDifficulty(self) -> TriviaDifficulty:
        return self.__triviaDifficulty

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getTriviaType(self) -> TriviaQuestionType:
        return self.__triviaType

    def hasCategory(self) -> bool:
        return utils.isValidStr(self.__category)

    def hasCategoryId(self) -> bool:
        return utils.isValidStr(self.__categoryId)
