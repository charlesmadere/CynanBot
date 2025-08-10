from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.grenadeTimeoutAction import GrenadeTimeoutAction
from ..grenadeTimeoutTarget import GrenadeTimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class GrenadeTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: GrenadeTimeoutAction
    target: GrenadeTimeoutTarget
    eventId: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
