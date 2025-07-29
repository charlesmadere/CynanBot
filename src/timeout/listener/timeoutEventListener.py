from abc import ABC, abstractmethod

from ..models.absTimeoutEvent import AbsTimeoutEvent


class TimeoutEventListener(ABC):

    @abstractmethod
    async def onNewTimeoutEvent(self, event: AbsTimeoutEvent):
        pass
