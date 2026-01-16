import locale
from dataclasses import dataclass

from .twitchStreamType import TwitchStreamType
from ...localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True)
class TwitchLiveUserDetails(TwitchUserInterface):
    isMature: bool
    viewerCount: int
    streamId: str
    userId: str
    userLogin: str
    userName: str
    gameId: str | None = None
    gameName: str | None = None
    language: str | None = None
    thumbnailUrl: str |  None = None
    title: str | None = None
    streamType: TwitchStreamType = TwitchStreamType.UNKNOWN

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName

    @property
    def viewerCountStr(self) -> str:
        return locale.format_string("%d", self.viewerCount, grouping = True)
