from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction


@dataclass(frozen = True)
class IncorrectLiveStatusTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AbsTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
