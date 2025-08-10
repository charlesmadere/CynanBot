from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.basicTimeoutAction import BasicTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class BasicTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    target: BasicTimeoutTarget
    eventId: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
