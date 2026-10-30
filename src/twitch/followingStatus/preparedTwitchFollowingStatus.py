from dataclasses import dataclass

from .twitchFollowingStatus import TwitchFollowingStatus
from ..localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedTwitchFollowingStatus(TwitchUserInterface):
    followingDurationSeconds: int
    followingStatus: TwitchFollowingStatus
    durationMessage: str
    shorthandDurationMessage: str
    userLogin: str
    userName: str

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName

    @property
    def twitchChannelId(self) -> str:
        return self.followingStatus.twitchChannelId

    @property
    def userId(self) -> str:
        return self.followingStatus.userId
