from abc import ABC, abstractmethod

from ..models.chatterPreferredNameData import ChatterPreferredNameData


class ChatterPreferredNameHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        pass
