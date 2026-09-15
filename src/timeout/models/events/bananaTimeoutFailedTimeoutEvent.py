from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class BananaTimeoutFailedTimeoutEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    eventId: str
    timeoutTarget: TimeoutTarget
    timeoutResult: TwitchTimeoutResult
    instigatorUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
