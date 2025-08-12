from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..bananaTimeoutTarget import BananaTimeoutTarget
from ..timeoutDiceRoll import TimeoutDiceRoll


@dataclass(frozen = True)
class BananaTimeoutDiceRollFailedEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    target: BananaTimeoutTarget
    eventId: str
    instigatorUserName: str
    diceRoll: TimeoutDiceRoll

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
