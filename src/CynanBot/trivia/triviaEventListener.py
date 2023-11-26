from abc import ABC, abstractmethod

from trivia.absTriviaEvent import AbsTriviaEvent


class TriviaEventListener(ABC):

    @abstractmethod
    async def onNewTriviaEvent(self, event: AbsTriviaEvent):
        pass
