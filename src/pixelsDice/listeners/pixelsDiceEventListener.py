from abc import ABC, abstractmethod

from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent


class PixelsDiceEventListener(ABC):

    @abstractmethod
    async def onNewPixelsDiceEvent(self, event: AbsPixelsDiceEvent):
        pass
