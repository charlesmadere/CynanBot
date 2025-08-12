from dataclasses import dataclass

from frozendict import frozendict
from frozenlist import FrozenList

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ..airStrikeTimeoutTarget import AirStrikeTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class AirStrikeTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    asplodieStats: frozendict[AirStrikeTimeoutTarget, AsplodieStats]
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    timeoutResults: frozendict[AirStrikeTimeoutTarget, TwitchTimeoutResult]
    targets: FrozenList[AirStrikeTimeoutTarget]
    bombEmote: str
    eventId: str
    explodedEmote: str
    instigatorUserName: str

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
