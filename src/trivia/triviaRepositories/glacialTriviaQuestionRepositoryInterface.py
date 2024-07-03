from abc import abstractmethod

from .triviaQuestionRepositoryInterface import TriviaQuestionRepositoryInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaSource import TriviaSource


class GlacialTriviaQuestionRepositoryInterface(TriviaQuestionRepositoryInterface):

    @abstractmethod
    async def remove(self, triviaId: str, originalTriviaSource: TriviaSource):
        pass

    @abstractmethod
    async def store(self, question: AbsTriviaQuestion) -> bool:
        pass
