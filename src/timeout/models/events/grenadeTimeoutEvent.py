from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..grenadeTimeoutTarget import GrenadeTimeoutTarget
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class GrenadeTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    originatingAction: GrenadeTimeoutAction
    target: GrenadeTimeoutTarget
    bombEmote: str
    eventId: str
    explodedEmote: str
    instigatorUserName: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
