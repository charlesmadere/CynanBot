from abc import ABC, abstractmethod

from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from ...misc.clearable import Clearable


class ChatterInventorySettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getAirStrikeItemDetails(self) -> AirStrikeItemDetails:
        pass

    @abstractmethod
    async def getBananaItemDetails(self) -> BananaItemDetails:
        pass

    @abstractmethod
    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        pass

    @abstractmethod
    async def getGrenadeItemDetails(self) -> GrenadeItemDetails:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
