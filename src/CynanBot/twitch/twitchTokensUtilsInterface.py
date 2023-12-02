from abc import ABC, abstractmethod
from typing import Optional


class TwitchTokensUtilsInterface(ABC):

    @abstractmethod
    async def getAccessTokenOrFallback(self, twitchChannel: str) -> Optional[str]:
        pass

    @abstractmethod
    async def requireAccessTokenOrFallback(self, twitchChannel: str) -> str:
        pass
