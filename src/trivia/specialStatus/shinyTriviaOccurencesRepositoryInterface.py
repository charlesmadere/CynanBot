from abc import ABC, abstractmethod

from .shinyTriviaResult import ShinyTriviaResult


class ShinyTriviaOccurencesRepositoryInterface(ABC):

    @abstractmethod
    async def fetchDetails(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> ShinyTriviaResult:
        pass

    @abstractmethod
    async def incrementShinyCount(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> ShinyTriviaResult:
        pass
