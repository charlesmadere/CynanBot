from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.tm36TimeoutAction import Tm36TimeoutAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class Tm36TimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    originatingAction: Tm36TimeoutAction
    timeoutResult: TwitchTimeoutResult
    targetUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
