from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget


@dataclass(frozen = True)
class BananaTimeoutDiceRollQueuedEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    timeoutTarget: BasicTimeoutTarget
    requestQueueSize: int
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
