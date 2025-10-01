from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class BananaTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    eventId: str
    instigatorUserName: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
