from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseGrenadeChatterItemEvent(AbsChatterItemEvent):
    itemDetails: GrenadeItemDetails
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
