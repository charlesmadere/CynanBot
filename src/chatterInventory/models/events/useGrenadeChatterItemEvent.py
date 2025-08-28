from dataclasses import dataclass

from .useChatterItemEvent import UseChatterItemEvent
from ..chatterItemType import ChatterItemType
from ..itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True)
class UseGrenadeChatterItemEvent(UseChatterItemEvent):
    itemDetails: GrenadeItemDetails
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction

    @property
    def itemType(self) -> ChatterItemType:
        return ChatterItemType.GRENADE
