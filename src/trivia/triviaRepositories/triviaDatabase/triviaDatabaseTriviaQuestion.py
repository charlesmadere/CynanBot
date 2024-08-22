from abc import ABC, abstractmethod

from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty
from ....misc import utils as utils


class TriviaDatabaseTriviaQuestion(ABC):

    def __init__(
        self,
        category: str | None,
        question: str,
        triviaId: str,
        difficulty: TriviaDifficulty
    ):
        if category is not None and not isinstance(category, str):
            raise TypeError(f'category argument is malformed: \"{category}\"')
        elif not utils.isValidStr(question):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(triviaId):
            raise TypeError(f'triviaId argument is malformed: \"{triviaId}\"')
        elif not isinstance(difficulty, TriviaDifficulty):
            raise TypeError(f'difficulty argument is malformed: \"{difficulty}\"')

        self.__category: str | None = category
        self.__question: str = question
        self.__triviaId: str = triviaId
        self.__difficulty: TriviaDifficulty = difficulty

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
    def triviaId(self) -> str:
        return self.__triviaId

    @property
    @abstractmethod
    def triviaType(self) -> TriviaQuestionType:
        pass
