from abc import ABC, abstractmethod

from ..models.chatterItemGiveResult import ChatterItemGiveResult
from ..models.chatterItemType import ChatterItemType
from ..models.preparedChatterInventoryData import PreparedChatterInventoryData


class ChatterInventoryHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> PreparedChatterInventoryData:
        pass

    @abstractmethod
    async def give(
        self,
        itemType: ChatterItemType,
        giveAmount: int,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterItemGiveResult:
        pass
