import locale
from dataclasses import dataclass
from enum import Enum, auto

from ..users.userInterface import UserInterface


@dataclass(frozen = True)
class TimeoutActionData:

    class StreamStatusRequirement(Enum):
        ANY = auto()
        OFFLINE = auto()
        ONLINE = auto()

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
    streamStatusRequirement: StreamStatusRequirement
    user: UserInterface

    @property
    def durationSecondsStr(self) -> str:
        return locale.format_string("%d", self.durationSeconds, grouping = True)

    @property
    def twitchChannel(self) -> str:
        return self.user.getHandle()
