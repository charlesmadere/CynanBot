from abc import ABC, abstractmethod
from dataclasses import dataclass


class TwitchChannelInformationHelperInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class GameDetails:
        gameId: str | None
        gameName: str | None

    @abstractmethod
    async def getGameDetails(
        self,
        twitchChannelId: str,
    ) -> GameDetails:
        pass

    @abstractmethod
    async def getTitle(
        self,
        twitchChannelId: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def requireTitle(
        self,
        twitchChannelId: str,
    ) -> str:
        pass

    @abstractmethod
    async def setGame(
        self,
        gameName: str,
        twitchChannelId: str,
    ) -> str:
        pass

    @abstractmethod
    async def setTitle(
        self,
        title: str,
        twitchChannelId: str,
    ) -> str:
        pass
