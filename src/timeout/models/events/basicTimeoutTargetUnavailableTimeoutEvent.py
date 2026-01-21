from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.basicTimeoutAction import BasicTimeoutAction


@dataclass(frozen = True, slots = True)
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
