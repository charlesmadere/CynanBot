from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..itemDetails.crowdMicItemDetails import CrowdMicItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class CrowdMicStartedItemEvent(AbsChatterItemEvent):
    itemDetails: CrowdMicItemDetails
    updatedInventory: ChatterInventoryData | None
    emoji: str
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
