from abc import ABC, abstractmethod

from .openTriviaQaTriviaQuestion import OpenTriviaQaTriviaQuestion


class OpenTriviaQaQuestionStorageInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> OpenTriviaQaTriviaQuestion:
        pass

    @abstractmethod
    async def hasQuestionSetAvailable(self) -> bool:
        pass
