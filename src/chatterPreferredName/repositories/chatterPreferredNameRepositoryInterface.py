from abc import ABC, abstractmethod

from ..models.chatterPreferredNameData import ChatterPreferredNameData
from ...misc.clearable import Clearable


class ChatterPreferredNameRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        preferredName: str | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        pass
