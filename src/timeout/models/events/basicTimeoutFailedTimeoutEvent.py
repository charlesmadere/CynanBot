from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.basicTimeoutAction import BasicTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class BasicTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    eventId: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
