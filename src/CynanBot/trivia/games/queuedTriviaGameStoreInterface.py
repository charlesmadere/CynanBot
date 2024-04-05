from abc import ABC, abstractmethod

from CynanBot.trivia.actions.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBot.trivia.addQueuedGamesResult import AddQueuedGamesResult
from CynanBot.trivia.clearQueuedGamesResult import ClearQueuedGamesResult


class QueuedTriviaGameStoreInterface(ABC):

    @abstractmethod
    async def addSuperGames(
        self,
        isSuperTriviaGameCurrentlyInProgress: bool,
        action: StartNewSuperTriviaGameAction
    ) -> AddQueuedGamesResult:
        pass

    @abstractmethod
    async def clearQueuedSuperGames(self, twitchChannelId: str) -> ClearQueuedGamesResult:
        pass

    @abstractmethod
    async def getQueuedSuperGamesSize(self, twitchChannelId: str) -> int:
        pass

    @abstractmethod
    async def popQueuedSuperGames(self, activeChannelIds: set[str]) -> list[StartNewSuperTriviaGameAction]:
        pass
