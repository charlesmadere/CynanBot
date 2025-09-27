from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..voreTimeoutTarget import VoreTimeoutTarget


@dataclass(frozen = True)
class NoVoreInventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    thumbsDownEmote: str
    originatingAction: VoreTimeoutAction
    timeoutTarget: VoreTimeoutTarget

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
