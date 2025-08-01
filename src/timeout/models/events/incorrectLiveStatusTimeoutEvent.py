from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent


@dataclass(frozen = True)
class IncorrectLiveStatusTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AbsTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
