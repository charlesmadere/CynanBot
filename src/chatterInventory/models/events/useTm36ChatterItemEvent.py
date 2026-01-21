from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..itemDetails.tm36ItemDetails import Tm36ItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class UseTm36ChatterItemEvent(AbsChatterItemEvent):
    eventId: str
    itemDetails: Tm36ItemDetails
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
