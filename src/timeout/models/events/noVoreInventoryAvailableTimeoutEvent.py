from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..timeoutTarget import TimeoutTarget


@dataclass(frozen = True, slots = True)
class NoVoreInventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    thumbsDownEmote: str
    timeoutTarget: TimeoutTarget
    originatingAction: VoreTimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
