from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class VoreTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    instigatorUserName: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult
    originatingAction: VoreTimeoutAction

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
