from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..grenadeTimeoutAction import GrenadeTimeoutAction


@dataclass(frozen = True)
class GrenadeTimeoutEvent(AbsTimeoutEvent):
    originatingAction: GrenadeTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
