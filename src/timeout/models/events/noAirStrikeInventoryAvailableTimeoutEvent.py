from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.airStrikeTimeoutAction import AirStrikeTimeoutAction
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class NoAirStrikeInventoryAvailableTimeoutEvent(AbsTimeoutEvent):
    originatingAction: AirStrikeTimeoutAction
    eventId: str
    instigatorUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
