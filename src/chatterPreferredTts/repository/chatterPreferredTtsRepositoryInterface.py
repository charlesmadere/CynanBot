from abc import ABC, abstractmethod

from ..models.chatterPrefferedTts import ChatterPreferredTts
from ...misc.clearable import Clearable


class ChatterPreferredTtsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredTts | None:
        pass

    @abstractmethod
    async def remove(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredTts | None:
        pass

    @abstractmethod
    async def set(self, preferredTts: ChatterPreferredTts):
        pass
