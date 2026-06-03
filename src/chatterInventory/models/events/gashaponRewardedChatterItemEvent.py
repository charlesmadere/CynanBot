from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..requestGashaponRewardAction import RequestGashaponRewardAction


@dataclass(frozen = True, slots = True)
class GashaponRewardedChatterItemEvent(AbsChatterItemEvent):
    chatterInventory: ChatterInventoryData
    originatingAction: RequestGashaponRewardAction
    eventId: str
    hypeEmote: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> RequestGashaponRewardAction:
        return self.originatingAction
