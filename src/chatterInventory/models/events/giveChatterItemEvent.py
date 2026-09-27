import locale
from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..giveChatterItemAction import GiveChatterItemAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class GiveChatterItemEvent(AbsChatterItemEvent):
    updatedInventory: ChatterInventoryData
    originatingAction: GiveChatterItemAction
    changeAmount: int
    eventId: str
    chatterUserData: TwitchUserInterface

    @property
    def changeAmountString(self) -> str:
        return locale.format_string("%d", self.changeAmount, grouping = True)

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> GiveChatterItemAction:
        return self.originatingAction
