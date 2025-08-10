from abc import ABC, abstractmethod

from ..models.events.absTimeoutEvent import AbsTimeoutEvent


class TimeoutEventListener(ABC):

    @abstractmethod
    async def onNewTimeoutEvent(self, event: AbsTimeoutEvent):
        pass
