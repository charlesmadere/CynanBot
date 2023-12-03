from abc import ABC, abstractmethod

from CynanBot.trivia.shinyTriviaResult import ShinyTriviaResult


class ShinyTriviaOccurencesRepositoryInterface(ABC):

    @abstractmethod
    async def fetchDetails(
        self,
        twitchChannel: str,
        userId: str
    ) -> ShinyTriviaResult:
        pass

    @abstractmethod
    async def incrementShinyCount(
        self,
        twitchChannel: str,
        userId: str
    ) -> ShinyTriviaResult:
        pass
