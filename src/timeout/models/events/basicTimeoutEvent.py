from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.basicTimeoutAction import BasicTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ..timeoutTarget import TimeoutTarget
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class BasicTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    timeoutDuration: CalculatedTimeoutDuration
    eventId: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult

    @property
    def chatMessage(self) -> str | None:
        return self.originatingAction.chatMessage

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
