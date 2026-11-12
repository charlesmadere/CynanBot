from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..chatterInventoryData import ChatterInventoryData
from ..requestWatchStreakRewardAction import RequestWatchStreakRewardAction


@dataclass(frozen = True, slots = True)
class WatchStreakRewardedChatterItemEvent(AbsChatterItemEvent):
    updatedInventory: ChatterInventoryData
    gashaponsRewarded: int
    originatingAction: RequestWatchStreakRewardAction
    eventId: str
    hypeEmote: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> RequestWatchStreakRewardAction:
        return self.originatingAction

    @property
    def watchStreak(self) -> int:
        return self.originatingAction.watchStreak
