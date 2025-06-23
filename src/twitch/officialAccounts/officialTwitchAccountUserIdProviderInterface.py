from abc import ABC, abstractmethod


class OfficialTwitchAccountUserIdProviderInterface(ABC):

    @abstractmethod
    async def getAllUserIds(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def getFrostyToolsDotComUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getMoobotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getNightbotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getPuptimeUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getSeryBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getSoundAlertsUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStreamElementsUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStreamLabsUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getStreamStickersUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTangiaBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTheRunBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTwitchAccountUserId(self) -> str:
        pass

    @abstractmethod
    async def getTwitchAnonymousGifterUserId(self) -> str:
        pass

    @abstractmethod
    async def getValorantUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getZeldoBotUserId(self) -> str | None:
        pass
