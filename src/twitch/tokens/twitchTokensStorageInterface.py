from abc import ABC, abstractmethod
from datetime import datetime

from ..api.models.twitchTokensDetails import TwitchTokensDetails


class TwitchTokensStorageInterface(ABC):

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str,
    ) -> TwitchTokensDetails | None:
        pass

    @abstractmethod
    async def remove(
        self,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    async def set(
        self,
        twitchChannelId: str,
        tokensDetails: TwitchTokensDetails | None,
    ):
        pass

    @abstractmethod
    async def updateExpirationTime(
        self,
        expirationTime: datetime,
        twitchChannelId: str,
    ):
        pass
