from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.grenadeTimeoutAction import GrenadeTimeoutAction


@dataclass(frozen = True)
class NoGrenadeTargetAvailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: GrenadeTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
