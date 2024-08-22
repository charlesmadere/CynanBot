from abc import ABC, abstractmethod

from .triviaDatabaseTriviaQuestion import TriviaDatabaseTriviaQuestion


class TriviaDatabaseQuestionStorageInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> TriviaDatabaseTriviaQuestion:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass
