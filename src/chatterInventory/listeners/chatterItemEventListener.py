from abc import ABC, abstractmethod

from ..models.events.absChatterItemEvent import AbsChatterItemEvent


class ChatterItemEventListener(ABC):

    @abstractmethod
    async def onNewChatterItemEvent(self, event: AbsChatterItemEvent):
        pass
