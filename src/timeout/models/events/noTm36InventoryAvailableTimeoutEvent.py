from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.tm36TimeoutAction import Tm36TimeoutAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class NoTm36InventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    eventId: str
    thumbsDownEmote: str
    originatingAction: Tm36TimeoutAction
    targetUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
