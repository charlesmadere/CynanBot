from abc import ABC, abstractmethod
from typing import Final

from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty
from ....misc import utils as utils


class OpenTriviaDatabaseQuestion(ABC):

    def __init__(
        self,
        category: str | None,
        question: str,
        difficulty: TriviaDifficulty,
    ):
        if category is not None and not isinstance(category, str):
            raise TypeError(f'category argument is malformed: \"{category}\"')
        elif not utils.isValidStr(question):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(difficulty, TriviaDifficulty):
            raise TypeError(f'difficulty argument is malformed: \"{difficulty}\"')

        self.__category: Final[str | None] = category
        self.__question: Final[str] = question
        self.__difficulty: Final[TriviaDifficulty] = difficulty

    @property
    def category(self) -> str | None:
        return self.__category

    @property
    def difficulty(self) -> TriviaDifficulty:
        return self.__difficulty

    @property
    def question(self) -> str:
        return self.__question

    @property
    @abstractmethod
    def triviaType(self) -> TriviaQuestionType:
        pass
