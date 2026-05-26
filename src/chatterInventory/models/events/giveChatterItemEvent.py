import locale
from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..giveChatterItemAction import GiveChatterItemAction


@dataclass(frozen = True, slots = True)
class GiveChatterItemEvent(AbsChatterItemEvent):
    updatedInventory: ChatterInventoryData
    changeAmount: int
    chatterUserName: str
    eventId: str
    originatingAction: GiveChatterItemAction

    @property
    def changeAmountString(self) -> str:
        return locale.format_string("%d", self.changeAmount, grouping = True)

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> GiveChatterItemAction:
        return self.originatingAction
