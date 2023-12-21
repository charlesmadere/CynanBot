from abc import ABC, abstractmethod
from typing import List, Set

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
    async def clearQueuedSuperGames(self, twitchChannel: str) -> ClearQueuedGamesResult:
        pass

    @abstractmethod
    async def getQueuedSuperGamesSize(self, twitchChannel: str) -> int:
        pass

    @abstractmethod
    async def popQueuedSuperGames(self, activeChannels: Set[str]) -> List[StartNewSuperTriviaGameAction]:
        pass
