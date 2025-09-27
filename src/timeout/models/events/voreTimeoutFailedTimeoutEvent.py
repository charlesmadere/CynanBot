from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.voreTimeoutAction import VoreTimeoutAction
from ..voreTimeoutTarget import VoreTimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class VoreTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    instigatorUserName: str
    timeoutResult: TwitchTimeoutResult
    originatingAction: VoreTimeoutAction
    target: VoreTimeoutTarget

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
