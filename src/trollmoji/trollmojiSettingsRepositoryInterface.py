from abc import ABC, abstractmethod

from .trollmojiDetails import TrollmojiDetails
from ..misc.clearable import Clearable


class TrollmojiSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getBombEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getBombEmoteBackup(self) -> str:
        pass

    @abstractmethod
    async def getDinkDonkEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getGottemEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getGottemEmoteBackup(self) -> str:
        pass

    @abstractmethod
    async def getHypeEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getHypeEmoteBackup(self) -> str:
        pass

    @abstractmethod
    async def getShrugEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getThumbsDownEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getThumbsDownEmoteBackup(self) -> str:
        pass

    @abstractmethod
    async def getThumbsUpEmote(self) -> TrollmojiDetails | None:
        pass

    @abstractmethod
    async def getThumbsUpEmoteBackup(self) -> str:
        pass
