from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutDiceRoll import TimeoutDiceRoll
from ..timeoutDiceRollFailureData import TimeoutDiceRollFailureData
from ..timeoutTarget import TimeoutTarget


@dataclass(frozen = True)
class BananaTimeoutDiceRollFailedEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    eventId: str
    instigatorUserName: str
    ripBozoEmote: str
    diceRoll: TimeoutDiceRoll
    diceRollFailureData: TimeoutDiceRollFailureData
    timeoutTarget: TimeoutTarget

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
