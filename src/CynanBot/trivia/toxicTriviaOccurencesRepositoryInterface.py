from abc import ABC, abstractmethod

from CynanBot.trivia.toxicTriviaResult import ToxicTriviaResult


class ToxicTriviaOccurencesRepositoryInterface(ABC):

    @abstractmethod
    async def fetchDetails(
        self,
        twitchChannel: str,
        userId: str
    ) -> ToxicTriviaResult:
        pass

    @abstractmethod
    async def incrementToxicCount(
        self,
        twitchChannel: str,
        userId: str
    ) -> ToxicTriviaResult:
        pass
