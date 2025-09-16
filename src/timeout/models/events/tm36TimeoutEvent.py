from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.tm36TimeoutAction import Tm36TimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....chatterInventory.models.chatterItemGiveResult import ChatterItemGiveResult
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class Tm36TimeoutEvent(AbsTimeoutEvent):
    timeoutDuration: CalculatedTimeoutDuration
    updatedInventory: ChatterItemGiveResult | None
    bombEmote: str
    eventId: str
    explodedEmote: str
    targetUserName: str
    originatingAction: Tm36TimeoutAction
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction
