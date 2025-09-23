from abc import ABC, abstractmethod
from typing import Any

from ..models.states.absPixelsDiceState import AbsPixelsDiceState


class PixelsDiceStateMapperInterface(ABC):

    @abstractmethod
    async def map(
        self,
        data: bytearray | Any | None,
    ) -> AbsPixelsDiceState | None:
        pass
