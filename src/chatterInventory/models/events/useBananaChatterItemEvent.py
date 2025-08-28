from dataclasses import dataclass

from .useChatterItemEvent import UseChatterItemEvent
from ..chatterItemType import ChatterItemType
from ..itemDetails.bananaItemDetails import BananaItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseBananaChatterItemEvent(UseChatterItemEvent):
    itemDetails: BananaItemDetails
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction

    @property
    def itemType(self) -> ChatterItemType:
        return ChatterItemType.BANANA
