from abc import ABC, abstractmethod
from typing import Any

from ..models.chatterPreferredNameData import ChatterPreferredNameData


class ChatterPreferredNameHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        preferredName: str | Any | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData:
        pass
