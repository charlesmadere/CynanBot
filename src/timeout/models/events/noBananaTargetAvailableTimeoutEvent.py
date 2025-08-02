from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..bananaTimeoutAction import BananaTimeoutAction


@dataclass(frozen = True)
class NoBananaTargetAvailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
