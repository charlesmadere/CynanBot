from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.basicTimeoutAction import BasicTimeoutAction
from ..basicTimeoutTarget import BasicTimeoutTarget
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class BasicTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BasicTimeoutAction
    target: BasicTimeoutTarget
    timeoutDuration: CalculatedTimeoutDuration
    eventId: str
    ripBozoEmote: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
