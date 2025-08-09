from dataclasses import dataclass

from frozendict import frozendict
from frozenlist import FrozenList

from ..absTimeoutAction import AbsTimeoutAction
from ..absTimeoutEvent import AbsTimeoutEvent
from ..airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..airStrikeTimeoutTarget import AirStrikeTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class AirStrikeTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    timeoutResults: frozendict[AirStrikeTimeoutTarget, TwitchTimeoutResult]
    targets: FrozenList[AirStrikeTimeoutTarget]
    eventId: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
