from abc import ABC, abstractmethod

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
        triviaSource: TriviaSource
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

        self.__category: str | None = category
        self.__categoryId: str | None = categoryId
        self.__question: str = question
        self.__triviaId: str = triviaId
        self.__triviaDifficulty: TriviaDifficulty = triviaDifficulty
        self.__originalTriviaSource: TriviaSource | None = originalTriviaSource
        self.__triviaSource: TriviaSource = triviaSource

    @property
    def category(self) -> str | None:
        return self.__category

    @property
    def categoryId(self) -> str | None:
        return self.__categoryId

    @property
    @abstractmethod
    def correctAnswers(self) -> list[str]:
        pass

    @property
    def originalTriviaSource(self) -> TriviaSource | None:
        return self.__originalTriviaSource

    @property
    def question(self) -> str:
        return self.__question

    @property
    @abstractmethod
    def responses(self) -> list[str]:
        pass

    @property
    def triviaDifficulty(self) -> TriviaDifficulty:
        return self.__triviaDifficulty

    @property
    def triviaId(self) -> str:
        return self.__triviaId

    @property
    def triviaSource(self) -> TriviaSource:
        return self.__triviaSource

    @property
    @abstractmethod
    def triviaType(self) -> TriviaQuestionType:
        pass
