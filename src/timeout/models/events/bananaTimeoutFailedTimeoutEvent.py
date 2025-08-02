from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..bananaTimeoutAction import BananaTimeoutAction
from ..bananaTimeoutTarget import BananaTimeoutTarget


@dataclass(frozen = True)
class BananaTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    target: BananaTimeoutTarget
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
