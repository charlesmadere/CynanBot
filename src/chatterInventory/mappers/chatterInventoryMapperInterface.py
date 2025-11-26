from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.animalPetItemDetails import AnimalPetItemDetails
from ..models.itemDetails.bananaItemDetails import BananaItemDetails
from ..models.itemDetails.gashaponItemDetails import GashaponItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..models.itemDetails.tm36ItemDetails import Tm36ItemDetails
from ..models.itemDetails.voreItemDetails import VoreItemDetails


class ChatterInventoryMapperInterface(ABC):

    @abstractmethod
    async def parseAirStrikeItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> AirStrikeItemDetails | None:
        pass

    @abstractmethod
    async def parseAnimalPetItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> AnimalPetItemDetails | None:
        pass

    @abstractmethod
    async def parseBananaItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> BananaItemDetails | None:
        pass

    @abstractmethod
    async def parseGashaponItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> GashaponItemDetails | None:
        pass

    @abstractmethod
    async def parseGrenadeItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> GrenadeItemDetails | None:
        pass

    @abstractmethod
    async def parseInventory(
        self,
        inventoryJson: dict[str, int | Any | None] | frozendict[str, int | Any | None] | Any | None,
    ) -> frozendict[ChatterItemType, int]:
        pass

    @abstractmethod
    async def parseItemType(
        self,
        itemType: str | Any | None,
    ) -> ChatterItemType | None:
        pass

    @abstractmethod
    async def parseTm36ItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> Tm36ItemDetails | None:
        pass

    @abstractmethod
    async def parseVoreItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> VoreItemDetails | None:
        pass

    @abstractmethod
    async def requireItemType(
        self,
        itemType: str | Any | None
    ) -> ChatterItemType:
        pass

    @abstractmethod
    async def serializeInventory(
        self,
        inventory: dict[ChatterItemType, int] | frozendict[ChatterItemType, int]
    ) -> dict[str, int]:
        pass

    @abstractmethod
    async def serializeItemType(
        self,
        itemType: ChatterItemType
    ) -> str:
        pass
