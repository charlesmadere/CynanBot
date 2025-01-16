from abc import ABC, abstractmethod

from .millionaireTriviaQuestion import MillionaireTriviaQuestion


class MillionaireTriviaQuestionStorageInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> MillionaireTriviaQuestion:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass
