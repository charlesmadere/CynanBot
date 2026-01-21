from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..itemDetails.bananaItemDetails import BananaItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class UseBananaChatterItemEvent(AbsChatterItemEvent):
    itemDetails: BananaItemDetails
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
