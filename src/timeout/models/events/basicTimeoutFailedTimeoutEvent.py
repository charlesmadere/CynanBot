from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..basicTimeoutAction import BasicTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget


@dataclass(frozen = True)
class BasicTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    target: BasicTimeoutTarget
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
