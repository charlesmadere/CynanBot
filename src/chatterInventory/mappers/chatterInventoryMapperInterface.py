from abc import ABC, abstractmethod
from typing import Any

from ..models.chatterItemType import ChatterItemType


class ChatterInventoryMapperInterface(ABC):

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
    async def serializeItemType(
        self,
        itemType: ChatterItemType
    ) -> str:
        pass
