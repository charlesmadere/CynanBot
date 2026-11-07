from abc import ABC, abstractmethod


class TwitchFriendsUserIdRepositoryInterface(ABC):

    @abstractmethod
    async def getAlbeeesUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAmySumisuUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAngieYunaUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAoyamabukiUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getAyAerithUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getBastionBlueUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getCharlyUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getConcisionUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getDeltaRayneUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getDylanStewUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getEddieUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getEtucaUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getGarUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getHarleyHardtUserId(self) -> str | None:
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
    async def getKazekiiUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getKiaraUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getLndegenUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getLucyUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMerttUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMiaGuwuUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getNintendesiUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getOatsngoatsUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getPatLanicusUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getSakuraMilkTeaUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStashiocatUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTawUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTsteineUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTwinmoUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getVolwrathUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getZanianUserId(self) -> str | None:
        pass
