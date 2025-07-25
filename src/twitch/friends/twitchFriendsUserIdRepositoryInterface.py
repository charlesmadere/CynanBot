from abc import ABC, abstractmethod


class TwitchFriendsUserIdRepositoryInterface(ABC):

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
    async def getAyAerithUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getBastionBlueUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getCharlesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getDylanStewUserId(self) -> str | None:
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
    async def getKiawaBotUserId(self) -> str | None:
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
    async def getMiaGuwuUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getOathyBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getPatLanicusUserId(self) -> str | None:
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
