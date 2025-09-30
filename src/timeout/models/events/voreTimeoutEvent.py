from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..chatterTimeoutHistory import ChatterTimeoutHistory
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class VoreTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    timeoutTarget: BasicTimeoutTarget
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    chatterTimeoutHistory: ChatterTimeoutHistory
    eventId: str
    instigatorUserName: str
    ripBozoEmote: str
    timeoutResult: TwitchTimeoutResult
    originatingAction: VoreTimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
