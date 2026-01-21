from dataclasses import dataclass

from frozendict import frozendict
from frozenlist import FrozenList

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..timeoutTarget import TimeoutTarget
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class AirStrikeTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    asplodieStats: frozendict[TimeoutTarget, AsplodieStats]
    timeoutResults: frozendict[TimeoutTarget, TwitchTimeoutResult]
    targets: FrozenList[TimeoutTarget]
    bombEmote: str
    eventId: str
    explodedEmote: str
    instigatorUserName: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
