import locale
from dataclasses import dataclass

from .timeoutActionType import TimeoutActionType
from .timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..users.userInterface import UserInterface


@dataclass(frozen = True)
class TimeoutActionData:
    isRandomChanceEnabled: bool
    bits: int | None
    durationSeconds: int
    chatMessage: str | None
    instigatorUserId: str
    instigatorUserName: str
    moderatorTwitchAccessToken: str
    moderatorUserId: str
    pointRedemptionEventId: str | None
    pointRedemptionMessage: str | None
    pointRedemptionRewardId: str | None
    timeoutTargetUserId: str
    timeoutTargetUserName: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    userTwitchAccessToken: str
    actionType: TimeoutActionType
    streamStatusRequirement: TimeoutStreamStatusRequirement
    user: UserInterface

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)

    @property
    def isTimeoutCheerActionIncreasedBullyFailureEnabled(self) -> bool:
        return self.user.isTimeoutCheerActionIncreasedBullyFailureEnabled

    @property
    def twitchChannel(self) -> str:
        return self.user.handle
