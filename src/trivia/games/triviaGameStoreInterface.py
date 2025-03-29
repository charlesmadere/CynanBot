from abc import ABC, abstractmethod

from frozenlist import FrozenList

from .absTriviaGameState import AbsTriviaGameState
from .superTriviaGameState import SuperTriviaGameState
from .triviaGameState import TriviaGameState


class TriviaGameStoreInterface(ABC):

    @abstractmethod
    async def add(
        self,
        state: AbsTriviaGameState
    ):
        pass

    @abstractmethod
    async def getAll(self) -> FrozenList[AbsTriviaGameState]:
        pass

    @abstractmethod
    async def getNormalGame(
        self,
        twitchChannelId: str,
        userId: str
    ) -> TriviaGameState | None:
        pass

    @abstractmethod
    async def getNormalGames(self) -> list[TriviaGameState]:
        pass

    @abstractmethod
    async def getSuperGame(
        self,
        twitchChannelId: str
    ) -> SuperTriviaGameState | None:
        pass

    @abstractmethod
    async def getSuperGames(self) -> list[SuperTriviaGameState]:
        pass

    @abstractmethod
    async def getTwitchChannelIdsWithActiveSuperGames(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def removeNormalGame(
        self,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        pass

    @abstractmethod
    async def removeSuperGame(
        self,
        twitchChannelId: str
    ) -> bool:
        pass
