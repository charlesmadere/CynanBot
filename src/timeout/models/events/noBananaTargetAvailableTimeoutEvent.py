from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult


@dataclass(frozen = True, slots = True)
class NoBananaTargetAvailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    updatedInventory: ChatterItemGiveResult | None
    eventId: str
    instigatorUserName: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
