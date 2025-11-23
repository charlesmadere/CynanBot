from abc import ABC, abstractmethod
from typing import Any, Final

from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import (BadTriviaCategoryException,
                                BadTriviaCategoryIdException,
                                BadTriviaDifficultyException,
                                BadTriviaIdException,
                                BadTriviaSourceException,
                                NoTriviaQuestionException)
from ...misc import utils as utils


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
    ):
        if category is not None and not isinstance(category, str):
            raise BadTriviaCategoryException(f'category argument is malformed: \"{category}\"')
        elif categoryId is not None and not isinstance(categoryId, str):
            raise BadTriviaCategoryIdException(f'categoryId argument is malformed: \"{categoryId}\"')
        elif not utils.isValidStr(question):
            raise NoTriviaQuestionException(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(triviaId):
            raise BadTriviaIdException(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(triviaDifficulty, TriviaDifficulty):
            raise BadTriviaDifficultyException(f'triviaDifficulty argument is malformed: \"{triviaDifficulty}\"')
        elif originalTriviaSource is not None and not isinstance(originalTriviaSource, TriviaSource):
            raise BadTriviaSourceException(f'originalTriviaSource argument is malformed: \"{triviaSource}\"')
        elif not isinstance(triviaSource, TriviaSource):
            raise BadTriviaSourceException(f'triviaSource argument is malformed: \"{triviaSource}\"')

        self.__category: Final[str | None] = category
        self.__categoryId: Final[str | None] = categoryId
        self.__question: Final[str] = question
        self.__triviaId: Final[str] = triviaId
        self.__triviaDifficulty: Final[TriviaDifficulty] = triviaDifficulty
        self.__originalTriviaSource: Final[TriviaSource | None] = originalTriviaSource
        self.__triviaSource: Final[TriviaSource] = triviaSource

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

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    @property
    @abstractmethod
    def responses(self) -> list[str]:
        pass

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
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
