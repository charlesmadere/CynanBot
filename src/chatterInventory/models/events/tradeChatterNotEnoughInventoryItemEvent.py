from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..absChatterItemAction import AbsChatterItemAction
from ..tradeChatterItemAction import TradeChatterItemAction


@dataclass(frozen = True, slots = True)
class TradeChatterNotEnoughInventoryItemEvent(AbsChatterItemEvent):
    tradeAmount: int
    eventId: str
    fromChatterUserName: str
    toChatterUserName: str
    originatingAction: TradeChatterItemAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsChatterItemAction:
        return self.originatingAction
