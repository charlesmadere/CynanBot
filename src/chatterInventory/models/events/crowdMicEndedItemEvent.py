from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..crowdMicrophoneStatus import CrowdMicrophoneStatus
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class CrowdMicEndedItemEvent(AbsChatterItemEvent):
    deadMicrophone: CrowdMicrophoneStatus
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
