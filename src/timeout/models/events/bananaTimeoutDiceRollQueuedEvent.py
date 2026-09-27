import locale
from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.bananaTimeoutAction import BananaTimeoutAction
from ..timeoutTarget import TimeoutTarget
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class BananaTimeoutDiceRollQueuedEvent(AbsTimeoutEvent):
    originatingAction: BananaTimeoutAction
    requestQueueSize: int
    eventId: str
    timeoutTarget: TimeoutTarget
    instigatorUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction

    @property
    def requestQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.requestQueueSize, grouping = True)
