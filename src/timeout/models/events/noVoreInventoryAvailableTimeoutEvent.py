from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget


@dataclass(frozen = True)
class NoVoreInventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    timeoutTarget: BasicTimeoutTarget
    eventId: str
    thumbsDownEmote: str
    originatingAction: VoreTimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
