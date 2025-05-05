from abc import ABC, abstractmethod

from ..models.chatterInventoryData import ChatterInventoryData
from ...misc.clearable import Clearable


class ChatterInventoryRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> ChatterInventoryData:
        pass
