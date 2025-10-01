from dataclasses import dataclass

from .absTimeoutAction import AbsTimeoutAction
from ..absTimeoutDuration import AbsTimeoutDuration
from ..timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ....aniv.models.whichAnivUser import WhichAnivUser
from ....users.userInterface import UserInterface


@dataclass(frozen = True)
class CopyAnivMessageTimeoutAction(AbsTimeoutAction):
    timeoutDuration: AbsTimeoutDuration
    actionId: str
    anivUserId: str
    moderatorTwitchAccessToken: str
    moderatorUserId: str
    targetUserId: str
    twitchChannelId: str
    userTwitchAccessToken: str
    streamStatusRequirement: TimeoutStreamStatusRequirement | None
    user: UserInterface
    whichAnivUser: WhichAnivUser

    def getActionId(self) -> str:
        return self.actionId

    def getChatMessage(self) -> str | None:
        return None

    def getInstigatorUserId(self) -> str:
        return self.anivUserId

    def getModeratorTwitchAccessToken(self) -> str:
        return self.moderatorTwitchAccessToken

    def getModeratorUserId(self) -> str:
        return self.moderatorUserId

    def getStreamStatusRequirement(self) -> TimeoutStreamStatusRequirement | None:
        return self.streamStatusRequirement

    def getTimeoutDuration(self) -> AbsTimeoutDuration:
        return self.timeoutDuration

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchChatMessageId(self) -> str | None:
        return None

    def getUser(self) -> UserInterface:
        return self.user

    def getUserTwitchAccessToken(self) -> str:
        return self.userTwitchAccessToken
