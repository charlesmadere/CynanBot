from abc import ABC, abstractmethod

from ..models.airStrikeItemDetails import AirStrikeItemDetails
from ..models.chatterItemType import ChatterItemType
from ...misc.clearable import Clearable


class ChatterInventorySettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getAirStrikeItemDetails(self) -> AirStrikeItemDetails | None:
        pass

    @abstractmethod
    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
