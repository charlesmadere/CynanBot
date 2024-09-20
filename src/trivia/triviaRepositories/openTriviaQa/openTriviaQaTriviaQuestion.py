from abc import ABC, abstractmethod

from .openTriviaQaQuestionType import OpenTriviaQaQuestionType
from ....misc import utils as utils


class OpenTriviaQaTriviaQuestion(ABC):

    def __init__(
        self,
        category: str | None,
        question: str,
        questionId: str
    ):
        if category is not None and not isinstance(category, str):
            raise TypeError(f'category argument is malformed: \"{category}\"')
        elif not utils.isValidStr(question):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(questionId):
            raise TypeError(f'questionId argument is malformed: \"{questionId}\"')

        self.__category: str | None = category
        self.__question: str = question
        self.__questionId: str = questionId

    @property
    def category(self) -> str | None:
        return self.__category

    @property
    def question(self) -> str:
        return self.__question

    @property
    def questionId(self) -> str:
        return self.__questionId

    @property
    @abstractmethod
    def questionType(self) -> OpenTriviaQaQuestionType:
        pass
