from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..itemDetails.voreItemDetails import VoreItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseVoreChatterItemEvent(AbsChatterItemEvent):
    eventId: str
    originatingAction: UseChatterItemAction
    itemDetails: VoreItemDetails

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
