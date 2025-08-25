from abc import ABC, abstractmethod

from ..models.events.useChatterItemEvent import UseChatterItemEvent


class UseChatterItemEventListener(ABC):

    @abstractmethod
    async def onNewUseChatterItemEvent(self, event: UseChatterItemEvent):
        pass
