from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..itemDetails.crowdMicItemDetails import CrowdMicItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class CrowdMicEndingSoonItemEvent(AbsChatterItemEvent):
    itemDetails: CrowdMicItemDetails
    microphone: CrowdMicrophoneStatus
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
