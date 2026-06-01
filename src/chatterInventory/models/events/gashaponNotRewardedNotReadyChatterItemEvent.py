from dataclasses import dataclass
from datetime import datetime

from .absChatterItemEvent import AbsChatterItemEvent
from ..requestGashaponRewardAction import RequestGashaponRewardAction


@dataclass(frozen = True, slots = True)
class GashaponNotRewardedNotReadyChatterItemEvent(AbsChatterItemEvent):
    nextGashaponAvailability: datetime
    originatingAction: RequestGashaponRewardAction
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> RequestGashaponRewardAction:
        return self.originatingAction
