import locale
from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutTarget import TimeoutTarget


@dataclass(frozen = True)
class BananaTimeoutDiceRollQueuedEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    requestQueueSize: int
    eventId: str
    instigatorUserName: str
    timeoutTarget: TimeoutTarget

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction

    @property
    def requestQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.requestQueueSize, grouping = True)
