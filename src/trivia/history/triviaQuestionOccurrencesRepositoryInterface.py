from abc import ABC, abstractmethod

from .triviaQuestionOccurrences import TriviaQuestionOccurrences
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.triviaSource import TriviaSource


class TriviaQuestionOccurrencesRepositoryInterface(ABC):

    @abstractmethod
    async def getOccurrences(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> TriviaQuestionOccurrences:
        pass

    @abstractmethod
    async def getOccurrencesFromQuestion(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> TriviaQuestionOccurrences:
        pass

    @abstractmethod
    async def incrementOccurrences(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> TriviaQuestionOccurrences:
        pass

    @abstractmethod
    async def incrementOccurrencesFromQuestion(
        self,
        triviaQuestion: AbsTriviaQuestion
    ) -> TriviaQuestionOccurrences:
        pass
