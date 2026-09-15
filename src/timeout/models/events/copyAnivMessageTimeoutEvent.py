from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.copyAnivMessageTimeoutAction import CopyAnivMessageTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....aniv.models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ....aniv.models.whichAnivUser import WhichAnivUser
from ....twitch.localModels.twitchUserInterface import TwitchUserInterface
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True, slots = True)
class CopyAnivMessageTimeoutEvent(AbsTimeoutEvent):
    copyMessageTimeoutScore: AnivCopyMessageTimeoutScore
    originatingAction: CopyAnivMessageTimeoutAction
    timeoutDuration: CalculatedTimeoutDuration
    eventId: str
    ripBozoEmote: str
    timeoutResult: TwitchTimeoutResult
    anivUserData: TwitchUserInterface
    targetUserData: TwitchUserInterface

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction

    @property
    def whichAnivUser(self) -> WhichAnivUser:
        return self.originatingAction.whichAnivUser
