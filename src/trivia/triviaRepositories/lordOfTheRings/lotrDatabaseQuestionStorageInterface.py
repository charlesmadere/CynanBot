from abc import ABC, abstractmethod

from .lotrTriviaQuestion import LotrTriviaQuestion


class LotrDatabaseQuestionStorageInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> LotrTriviaQuestion:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass
