from dataclasses import dataclass

from .absChatterItemEvent import AbsChatterItemEvent
from ..requestGashaponRewardAction import RequestGashaponRewardAction


@dataclass(frozen = True, slots = True)
class GashaponNotRewardedNotFollowingChatterItemEvent(AbsChatterItemEvent):
    originatingAction: RequestGashaponRewardAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> RequestGashaponRewardAction:
        return self.originatingAction
