from abc import abstractmethod

from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaSource import TriviaSource
from .triviaQuestionRepositoryInterface import TriviaQuestionRepositoryInterface


class GlacialTriviaQuestionRepositoryInterface(TriviaQuestionRepositoryInterface):

    @abstractmethod
    async def remove(self, triviaId: str, originalTriviaSource: TriviaSource):
        pass

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion) -> bool:
        pass
