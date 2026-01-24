from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class TrollmojiHelperInterface(Clearable, ABC):

    @abstractmethod
    async def getBombEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getBombEmoteOrBackup(self) -> str:
        pass

    @abstractmethod
    async def getDinkDonkEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getEmote(
        self,
        emoteText: str | None,
        twitchEmoteChannelId: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def getExplodedEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getExplodedEmoteOrBackup(self) -> str:
        pass

    @abstractmethod
    async def getGottemEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getGottemEmoteOrBackup(self) -> str:
        pass

    @abstractmethod
    async def getHypeEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getHypeEmoteOrBackup(self) -> str:
        pass

    @abstractmethod
    async def getShrugEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getThumbsDownEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getThumbsDownEmoteOrBackup(self) -> str:
        pass

    @abstractmethod
    async def getThumbsUpEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getThumbsUpEmoteOrBackup(self) -> str:
        pass
