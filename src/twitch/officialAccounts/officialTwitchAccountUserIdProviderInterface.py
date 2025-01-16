from abc import ABC, abstractmethod


class OfficialTwitchAccountUserIdProviderInterface(ABC):

    @abstractmethod
    async def getTwitchAccountUserId(self) -> str:
        pass

    @abstractmethod
    async def getTwitchAnonymousGifterUserId(self) -> str:
        pass

    @abstractmethod
    async def getValorantUserId(self) -> str:
        pass
