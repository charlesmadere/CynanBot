from abc import ABC, abstractmethod

from ..models.chatterInventoryData import ChatterInventoryData
from ..models.chatterItemType import ChatterItemType
from ...misc.clearable import Clearable


class ChatterInventoryRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        pass

    @abstractmethod
    async def update(
        self,
        itemType: ChatterItemType,
        changeAmount: int,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        pass
