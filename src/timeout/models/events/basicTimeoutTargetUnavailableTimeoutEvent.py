from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..basicTimeoutAction import BasicTimeoutAction


@dataclass(frozen = True)
class BasicTimeoutTargetUnavailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction

    @property
    def targetUserId(self) -> str:
        return self.originatingAction.targetUserId
