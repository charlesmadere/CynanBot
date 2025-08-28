from dataclasses import dataclass

from .useChatterItemEvent import UseChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..chatterItemType import ChatterItemType
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class NotEnoughInventoryChatterItemEvent(UseChatterItemEvent):
    chatterInventory: ChatterInventoryData
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction

    @property
    def itemType(self) -> ChatterItemType:
        return self.originatingAction.itemType
