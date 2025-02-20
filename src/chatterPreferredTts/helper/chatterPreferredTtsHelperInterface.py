from abc import ABC, abstractmethod

from ..models.chatterPrefferedTts import ChatterPreferredTts


class ChatterPreferredTtsHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterPreferredTts | None:
        pass
