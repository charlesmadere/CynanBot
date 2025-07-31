from dataclasses import dataclass

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..airStrikeTimeoutAction import AirStrikeTimeoutAction


@dataclass(frozen = True)
class AirStrikeTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
