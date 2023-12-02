from abc import ABC, abstractmethod
from typing import Optional


class TwitchTokensUtilsInterface(ABC):

    @abstractmethod
    async def getAccessTokenOrFallback(self, userName: str) -> Optional[str]:
        pass

    @abstractmethod
    async def requireAccessTokenOrFallback(self, userName: str) -> str:
        pass
