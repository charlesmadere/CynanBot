from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..absTimeoutTarget import AbsTimeoutTarget
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction


@dataclass(frozen = True)
class BananaTargetIsImmuneTimeoutEvent(AbsTimeoutEvent):
    timeoutTarget: AbsTimeoutTarget
    originatingAction: BananaTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
