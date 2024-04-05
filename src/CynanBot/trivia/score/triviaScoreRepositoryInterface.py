from abc import ABC, abstractmethod

from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult


class TriviaScoreRepositoryInterface(ABC):

    @abstractmethod
    async def fetchTriviaScore(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        pass

    @abstractmethod
    async def incrementSuperTriviaWins(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        pass

    @abstractmethod
    async def incrementTriviaLosses(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        pass

    @abstractmethod
    async def incrementTriviaWins(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ) -> TriviaScoreResult:
        pass
