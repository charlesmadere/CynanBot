from abc import ABC, abstractmethod


class TwitchChannelInformationHelperInterface(ABC):

    @abstractmethod
    async def getGame(
        self,
        twitchChannelId: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def getTitle(
        self,
        twitchChannelId: str,
    ) -> str | None:
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
