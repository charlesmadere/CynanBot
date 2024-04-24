from abc import ABC, abstractmethod
from typing import Any

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
        category: str | None,
        categoryId: str | None,
        question: str,
        triviaId: str,
        triviaDifficulty: TriviaDifficulty,
        originalTriviaSource: TriviaSource | None,
        triviaSource: TriviaSource,
        triviaType: TriviaQuestionType
    ):
        if not utils.isValidStr(question):
            raise NoTriviaQuestionException(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(triviaId):
            raise BadTriviaIdException(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaDifficulty, TriviaDifficulty):
            raise BadTriviaDifficultyException(f'triviaDifficulty argument is malformed: \"{triviaDifficulty}\"')
        elif originalTriviaSource is not None and not isinstance(originalTriviaSource, TriviaSource):
            raise BadTriviaSourceException(f'originalTriviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise BadTriviaSourceException(f'triviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaType, TriviaQuestionType):
            raise BadTriviaTypeException(f'triviaType argument is malformed: \"{triviaType}\"')

        self.__category: str | None = category
        self.__categoryId: str | None = categoryId
        self.__question: str = question
        self.__triviaId: str = triviaId
        self.__triviaDifficulty: TriviaDifficulty = triviaDifficulty
        self.__originalTriviaSource: TriviaSource | None = originalTriviaSource
        self.__triviaSource: TriviaSource = triviaSource
        self.__triviaType: TriviaQuestionType = triviaType

    def getCategory(self) -> str | None:
        return self.__category

    def getCategoryId(self) -> str | None:
        return self.__categoryId

    @abstractmethod
    def getCorrectAnswers(self) -> list[str]:
        pass

    def getOriginalTriviaSource(self) -> TriviaSource | None:
        return self.__originalTriviaSource

    @abstractmethod
    def getPrompt(self, delimiter: str = ' ') -> str:
        pass

    def getQuestion(self) -> str:
        return self.__question

    @abstractmethod
    def getResponses(self) -> list[str]:
        pass

    def getTriviaDifficulty(self) -> TriviaDifficulty:
        return self.__triviaDifficulty

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getTriviaType(self) -> TriviaQuestionType:
        return self.__triviaType

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'category': self.__category,
            'categoryId': self.__categoryId,
            'question': self.__question,
            'triviaDifficulty': self.__triviaDifficulty,
            'triviaId': self.__triviaId,
            'triviaSource': self.__triviaSource,
            'triviaType': self.__triviaType
        }
