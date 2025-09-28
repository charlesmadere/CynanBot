from abc import ABC, abstractmethod

from ..models.pixelsDiceRoll import PixelsDiceRoll


class PixelsDiceRollRequestCallback(ABC):

    @abstractmethod
    async def onPixelsDiceRolled(self, roll: PixelsDiceRoll):
        pass
