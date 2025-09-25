from abc import ABC, abstractmethod
from typing import Any

from ..models.states.absPixelsDiceState import AbsPixelsDiceState


class PixelsDiceStateMapperInterface(ABC):

    @abstractmethod
    async def map(
        self,
        rawData: bytearray | Any | None,
    ) -> AbsPixelsDiceState | None:
        pass
