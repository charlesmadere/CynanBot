from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class UseAirStrikeChatterItemEvent(AbsChatterItemEvent):
    itemDetails: AirStrikeItemDetails
    eventId: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
