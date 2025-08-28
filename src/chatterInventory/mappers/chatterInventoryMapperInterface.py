from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.bananaItemDetails import BananaItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails


class ChatterInventoryMapperInterface(ABC):

    @abstractmethod
    async def parseAirStrikeItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> AirStrikeItemDetails | None:
        pass

    @abstractmethod
    async def parseBananaItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> BananaItemDetails | None:
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
        inventoryJson: dict[str, int | Any | None] | frozendict[str, int | Any | None] | Any | None
    ) -> frozendict[ChatterItemType, int]:
        pass

    @abstractmethod
    async def parseItemType(
        self,
        itemType: str | Any | None
    ) -> ChatterItemType | None:
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
