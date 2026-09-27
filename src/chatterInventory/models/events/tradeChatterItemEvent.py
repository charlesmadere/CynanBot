from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..tradeChatterItemAction import TradeChatterItemAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TradeChatterItemEvent(AbsChatterItemEvent):
    fromChatterInventory: ChatterInventoryData
    toChatterInventory: ChatterInventoryData
    tradeAmount: int
    eventId: str
    originatingAction: TradeChatterItemAction
    fromChatterUserData: TwitchUserInterface
    toChatterUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> TradeChatterItemAction:
        return self.originatingAction
