from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class GrenadeTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: GrenadeTimeoutAction
    eventId: str
    instigatorUserName: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
