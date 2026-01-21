from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..tradeChatterItemAction import TradeChatterItemAction


@dataclass(frozen = True, slots = True)
class TradeChatterItemEvent(AbsChatterItemEvent):
    fromChatterInventory: ChatterInventoryData
    toChatterInventory: ChatterInventoryData
    tradeAmount: int
    eventId: str
    fromChatterUserName: str
    toChatterUserName: str
    originatingAction: TradeChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> TradeChatterItemAction:
        return self.originatingAction
