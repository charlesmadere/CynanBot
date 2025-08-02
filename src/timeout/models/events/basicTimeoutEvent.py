from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..basicTimeoutAction import BasicTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration


@dataclass(frozen = True)
class BasicTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    target: BasicTimeoutTarget
    timeoutDuration: CalculatedTimeoutDuration
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
