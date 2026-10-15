from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from ..models.chatterItemType import ChatterItemType


class ItemRequestMessageParserInterface(ABC):

    @dataclass(frozen = True, slots = True)
    class Result:
        itemType: ChatterItemType
        argument: str | None
        originalChatMessage: str

    @abstractmethod
    async def parse(
        self,
        chatMessage: str | Any | None,
    ) -> Result | None:
        pass
