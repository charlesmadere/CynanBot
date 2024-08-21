from abc import ABC, abstractmethod

from .willFryTriviaQuestion import WillFryTriviaQuestion


class WillFryTriviaApiServiceInterface(ABC):

    @abstractmethod
    async def fetchTriviaQuestion(self) -> WillFryTriviaQuestion:
        pass
