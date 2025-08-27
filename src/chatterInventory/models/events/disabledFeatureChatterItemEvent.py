from dataclasses import dataclass

from .useChatterItemEvent import UseChatterItemEvent
from ..chatterItemType import ChatterItemType
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class DisabledFeatureChatterItemEvent(UseChatterItemEvent):
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction

    @property
    def itemType(self) -> ChatterItemType:
        return self.originatingAction.itemType
