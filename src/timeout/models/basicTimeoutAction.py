from dataclasses import dataclass

from .absTimeoutAction import AbsTimeoutAction
from .absTimeoutDuration import AbsTimeoutDuration
from .pointRedemptionTimeoutData import PointRedemptionTimeoutData
from ..timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class BasicTimeoutAction(AbsTimeoutAction):
    timeoutDuration: AbsTimeoutDuration
    pointRedemption: PointRedemptionTimeoutData | None
    actionId: str
    instigatorUserId: str
    moderatorTwitchAccessToken: str
    moderatorUserId: str
    reason: str | None
    targetUserId: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    userTwitchAccessToken: str
    streamStatusRequirement: TimeoutStreamStatusRequirement | None
    user: UserInterface

    def getActionId(self) -> str:
        return self.actionId

    def getInstigatorUserId(self) -> str:
        return self.instigatorUserId

    def getModeratorTwitchAccessToken(self) -> str:
        return self.moderatorTwitchAccessToken

    def getModeratorUserId(self) -> str:
        return self.moderatorUserId

    def getPointRedemptionData(self) -> PointRedemptionTimeoutData | None:
        return self.pointRedemption

    def getStreamStatusRequirement(self) -> TimeoutStreamStatusRequirement | None:
        return self.streamStatusRequirement

    def getTimeoutDuration(self) -> AbsTimeoutDuration:
        return self.timeoutDuration

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchChatMessageId(self) -> str | None:
        return self.twitchChatMessageId

    def getUser(self) -> UserInterface:
        return self.user

    def getUserTwitchAccessToken(self) -> str:
        return self.userTwitchAccessToken
