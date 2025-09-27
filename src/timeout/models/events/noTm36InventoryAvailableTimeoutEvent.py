from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.tm36TimeoutAction import Tm36TimeoutAction


@dataclass(frozen = True)
class NoTm36InventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    targetUserName: str
    thumbsDownEmote: str
    originatingAction: Tm36TimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
