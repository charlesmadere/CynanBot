from abc import ABC, abstractmethod
from typing import Any

from frozendict import frozendict

from ..models.chatterItemType import ChatterItemType


class ChatterInventoryMapperInterface(ABC):

    @abstractmethod
    async def parseInventory(
        self,
        inventoryJson: dict[str, int | None] | frozendict[str, int | None] | Any | None
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
