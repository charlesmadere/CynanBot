from abc import ABC, abstractmethod

from .pokepediaTriviaQuestionType import PokepediaTriviaQuestionType
from ...questions.triviaQuestionType import TriviaQuestionType
from ....misc import utils as utils


class PokepediaTriviaQuestion(ABC):

    def __init__(
        self,
        pokepediaTriviaType: PokepediaTriviaQuestionType,
        question: str
    ):
        if not isinstance(pokepediaTriviaType, PokepediaTriviaQuestionType):
            raise TypeError(f'pokepediaTriviaType argument is malformed: \"{pokepediaTriviaType}\"')
        elif not utils.isValidStr(question):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        self.__pokepediaTriviaType: PokepediaTriviaQuestionType = pokepediaTriviaType
        self.__question: str = question

    @property
    def pokepediaTriviaType(self) -> PokepediaTriviaQuestionType:
        return self.__pokepediaTriviaType

    @property
    def question(self) -> str:
        return self.__question

    @property
    @abstractmethod
    def triviaType(self) -> TriviaQuestionType:
        pass
