from abc import ABC, abstractmethod

from ..models.preparedChatterInventoryData import PreparedChatterInventoryData


class ChatterInventoryHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> PreparedChatterInventoryData:
        pass
