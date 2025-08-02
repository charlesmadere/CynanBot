from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..grenadeTimeoutAction import GrenadeTimeoutAction
from ..grenadeTimeoutTarget import GrenadeTimeoutTarget


@dataclass(frozen = True)
class GrenadeTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: GrenadeTimeoutAction
    target: GrenadeTimeoutTarget
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
