from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..timeoutTarget import TimeoutTarget
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class VoreTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    eventId: str
    ripBozoEmote: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult
    instigatorUserData: TwitchUserInterface
    originatingAction: VoreTimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
