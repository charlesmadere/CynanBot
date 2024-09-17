from abc import ABC, abstractmethod


class OfficialTwitchAccountUserIdProviderInterface(ABC):

    @abstractmethod
    async def getTwitchAccountUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getTwitchAnonymousGifterUserId(self) -> str | None:
        pass
