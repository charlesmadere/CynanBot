from abc import ABC, abstractmethod

from .chatterPrefferedTts import ChatterPreferredTts
from ...misc.clearable import Clearable


class ChattersPreferredTtsRepositoryInterface(ABC, Clearable):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts:
        pass
