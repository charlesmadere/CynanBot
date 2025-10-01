from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutTarget import TimeoutTarget


@dataclass(frozen = True)
class BananaTargetIsImmuneTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    eventId: str
    timeoutTarget: TimeoutTarget

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
