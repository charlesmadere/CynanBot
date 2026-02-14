from abc import ABC, abstractmethod

from .toxicTriviaResult import ToxicTriviaResult


class ToxicTriviaOccurencesRepositoryInterface(ABC):

    @abstractmethod
    async def fetchDetails(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> ToxicTriviaResult:
        pass

    @abstractmethod
    async def incrementToxicCount(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> ToxicTriviaResult:
        pass
