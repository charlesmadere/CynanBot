from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..actions.startNewSuperTriviaGameAction import StartNewSuperTriviaGameAction
from ..addQueuedGamesResult import AddQueuedGamesResult
from ..clearQueuedGamesResult import ClearQueuedGamesResult


class QueuedTriviaGameStoreInterface(ABC):

    @abstractmethod
    async def addSuperGames(
        self,
        isSuperTriviaGameCurrentlyInProgress: bool,
        action: StartNewSuperTriviaGameAction,
    ) -> AddQueuedGamesResult:
        pass

    @abstractmethod
    async def clearQueuedSuperGames(
        self,
        twitchChannelId: str,
    ) -> ClearQueuedGamesResult:
        pass

    @abstractmethod
    async def getQueuedSuperGamesSize(
        self,
        twitchChannelId: str,
    ) -> int:
        pass

    @abstractmethod
    async def popQueuedSuperGames(
        self,
        activeChannelIds: set[str],
    ) -> FrozenList[StartNewSuperTriviaGameAction]:
        pass
