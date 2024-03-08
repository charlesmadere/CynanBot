from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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
        elif not utils.isValidStr(triviaId):
            raise BadTriviaIdException(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaDifficulty, TriviaDifficulty):
            raise BadTriviaDifficultyException(f'triviaDifficulty argument is malformed: \"{triviaDifficulty}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise BadTriviaSourceException(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise BadTriviaTypeException(f'triviaType argument is malformed: \"{triviaType}\"')

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

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'category': self.__category,
            'categoryId': self.__categoryId,
            'question': self.__question,
            'triviaDifficulty': self.__triviaDifficulty,
            'triviaId': self.__triviaId,
            'triviaSource': self.__triviaSource,
            'triviaType': self.__triviaType
        }
