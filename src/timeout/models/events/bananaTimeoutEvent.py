from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..bananaTimeoutTarget import BananaTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class BananaTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    originatingAction: BananaTimeoutAction
    target: BananaTimeoutTarget
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    eventId: str
    instigatorUserName: str
    ripBozoEmote: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
