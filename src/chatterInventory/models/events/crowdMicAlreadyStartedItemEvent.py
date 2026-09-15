from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..itemDetails.crowdMicItemDetails import CrowdMicItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class CrowdMicAlreadyStartedItemEvent(AbsChatterItemEvent):
    itemDetails: CrowdMicItemDetails
    microphoneStatus: CrowdMicrophoneStatus
    updatedInventory: ChatterInventoryData | None
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
