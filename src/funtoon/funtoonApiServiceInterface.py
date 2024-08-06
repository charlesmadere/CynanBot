from abc import ABC, abstractmethod

from .funtoonTriviaQuestion import FuntoonTriviaQuestion


class FuntoonApiServiceInterface(ABC):

    @abstractmethod
    async def banTriviaQuestion(self, triviaId: str) -> bool:
        pass

    @abstractmethod
    async def fetchTriviaQuestion(self) -> FuntoonTriviaQuestion:
        pass
