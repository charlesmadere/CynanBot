from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..absChatterItemAction import AbsChatterItemAction
from ..tradeChatterItemAction import TradeChatterItemAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TradeChatterNotEnoughInventoryItemEvent(AbsChatterItemEvent):
    tradeAmount: int
    eventId: str
    originatingAction: TradeChatterItemAction
    fromChatterUserData: TwitchUserInterface
    toChatterUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsChatterItemAction:
        return self.originatingAction
