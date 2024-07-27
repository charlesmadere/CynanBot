import locale
from dataclasses import dataclass

from .twitchStreamType import TwitchStreamType


@dataclass(frozen = True)
class TwitchLiveUserDetails:
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

    def getViewerCountStr(self) -> str:
        return locale.format_string("%d", self.viewerCount, grouping = True)
