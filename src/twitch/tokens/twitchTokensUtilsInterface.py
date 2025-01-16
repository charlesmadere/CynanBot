from abc import ABC, abstractmethod


class TwitchTokensUtilsInterface(ABC):

    @abstractmethod
    async def getAccessTokenOrFallback(self, twitchChannel: str) -> str | None:
        pass

    @abstractmethod
    async def getAccessTokenByIdOrFallback(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def requireAccessTokenOrFallback(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def requireAccessTokenByIdOrFallback(self, twitchChannelId: str) -> str:
        pass
