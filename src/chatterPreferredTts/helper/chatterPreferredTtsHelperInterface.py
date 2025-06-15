from abc import ABC, abstractmethod

from ..models.chatterPrefferedTts import ChatterPreferredTts


class ChatterPreferredTtsHelperInterface(ABC):

    @abstractmethod
    async def applyRandomPreferredTts(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts:
        pass

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        pass
