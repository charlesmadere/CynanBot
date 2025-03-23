from abc import ABC, abstractmethod

from ...aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface


class TwitchFriendsUserIdRepositoryInterface(AnivUserIdProviderInterface, ABC):

    @abstractmethod
    async def getAcacUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAlbeeesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAneevUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAnivUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getBastionBlueUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getCharlesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getEddieUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getHokkaidoubareUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getImytUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getJrpUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getLucentUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMandooBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMerttUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getOathyBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStashiocatUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getVolwrathUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getZanianUserId(self) -> str | None:
        pass
