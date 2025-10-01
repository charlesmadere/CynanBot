from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..chatterTimeoutHistory import ChatterTimeoutHistory
from ..timeoutDiceRoll import TimeoutDiceRoll
from ..timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..timeoutTarget import TimeoutTarget
from ....asplodieStats.models.asplodieStats import AsplodieStats
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class BananaTimeoutEvent(AbsTimeoutEvent):
    asplodieStats: AsplodieStats
    originatingAction: BananaTimeoutAction
    isReverse: bool
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    chatterTimeoutHistory: ChatterTimeoutHistory
    eventId: str
    instigatorUserName: str
    ripBozoEmote: str
    diceRoll: TimeoutDiceRoll | None
    diceRollFailureData: TimeoutDiceRollFailureData | None
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
