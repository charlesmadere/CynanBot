from dataclasses import dataclass

from .absTimeoutEvent import AbsTimeoutEvent
from ..actions.absTimeoutAction import AbsTimeoutAction
from ..actions.copyAnivMessageTimeoutAction import CopyAnivMessageTimeoutAction
from ..calculatedTimeoutDuration import CalculatedTimeoutDuration
from ....aniv.models.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ....aniv.models.whichAnivUser import WhichAnivUser
from ....twitch.timeout.twitchTimeoutResult import TwitchTimeoutResult


@dataclass(frozen = True)
class CopyAnivMessageTimeoutEvent(AbsTimeoutEvent):
    copyMessageTimeoutScore: AnivCopyMessageTimeoutScore
    originatingAction: CopyAnivMessageTimeoutAction
    timeoutDuration: CalculatedTimeoutDuration
    eventId: str
    anivUserName: str
    ripBozoEmote: str
    targetUserName: str
    timeoutResult: TwitchTimeoutResult

    def getEventId(self) -> str:
        return self.eventId

    def getOriginatingAction(self) -> AbsTimeoutAction:
        return self.originatingAction

    @property
    def whichAnivUser(self) -> WhichAnivUser:
        return self.originatingAction.whichAnivUser
