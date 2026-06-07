from dataclasses import dataclass

from frozendict import frozendict

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..chatterItemType import ChatterItemType
from ..gashaponTier import GashaponTier
from ..useChatterItemAction import UseChatterItemAction


@dataclass(frozen = True, slots = True)
class GashaponResultsChatterItemEvent(AbsChatterItemEvent):
    updatedInventory: ChatterInventoryData
    awardedItems: frozendict[ChatterItemType, int]
    gashaponTier: GashaponTier
    eventId: str
    hypeEmote: str
    originatingAction: UseChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> UseChatterItemAction:
        return self.originatingAction
