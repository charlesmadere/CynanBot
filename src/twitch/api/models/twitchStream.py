from dataclasses import dataclass
from datetime import datetime

from .twitchStreamType import TwitchStreamType
from ...localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class TwitchStream(TwitchUserInterface):
    startedAt: datetime
    tags: frozenset[str]
    viewerCount: int
    gameId: str
    gameName: str
    language: str | None
    streamId: str
    thumbnailUrl: str | None
    title: str | None
    userId: str
    userLogin: str
    userName: str
    streamType: TwitchStreamType

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName
