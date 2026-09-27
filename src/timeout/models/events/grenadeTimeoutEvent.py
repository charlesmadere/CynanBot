from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..timeoutTarget import TimeoutTarget
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class GrenadeTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    originatingAction: GrenadeTimeoutAction
    bombEmote: str
    eventId: str
    explodedEmote: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult
    instigatorUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
