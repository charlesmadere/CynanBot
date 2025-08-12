from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.airStrikeTimeoutAction import AirStrikeTimeoutAction


@dataclass(frozen = True)
class NoAirStrikeInventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    eventId: str
    instigatorUserName: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
