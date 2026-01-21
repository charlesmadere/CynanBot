from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..useChatterItemAction import UseChatterItemAction
from ....voicemail.models.addVoicemailResult import AddVoicemailResult


@dataclass(frozen = True, slots = True)
class UseCassetteTapeChatterItemEvent(AbsChatterItemEvent):
    addVoicemailResult: AddVoicemailResult
    updatedInventory: ChatterInventoryData | None
    eventId: str
    targetUserId: str
    targetUserName: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
