from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class NotEnoughInventoryChatterItemEvent(AbsChatterItemEvent):
    chatterInventory: ChatterInventoryData
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
