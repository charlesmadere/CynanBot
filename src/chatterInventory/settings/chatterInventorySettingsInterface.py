from abc import ABC, abstractmethod

from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.animalPetItemDetails import AnimalPetItemDetails
from ..models.itemDetails.bananaItemDetails import BananaItemDetails
from ..models.itemDetails.gashaponItemDetails import GashaponItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..models.itemDetails.tm36ItemDetails import Tm36ItemDetails
from ...misc.clearable import Clearable


class ChatterInventorySettingsInterface(Clearable, ABC):

    @abstractmethod
    async def getAirStrikeItemDetails(self) -> AirStrikeItemDetails:
        pass

    @abstractmethod
    async def getAnimalPetItemDetails(self) -> AnimalPetItemDetails:
        pass

    @abstractmethod
    async def getBananaItemDetails(self) -> BananaItemDetails:
        pass

    @abstractmethod
    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        pass

    @abstractmethod
    async def getGashaponItemDetails(self) -> GashaponItemDetails:
        pass

    @abstractmethod
    async def getGrenadeItemDetails(self) -> GrenadeItemDetails:
        pass

    @abstractmethod
    async def getTm36ItemDetails(self) -> Tm36ItemDetails:
        pass

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
