from dataclasses import dataclass

from frozenlist import FrozenList

from .chatterTimeoutHistory import ChatterTimeoutHistory
from .chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry


@dataclass(frozen = True)
class PreparedChatterTimeoutHistory:
    chatterTimeoutHistory: ChatterTimeoutHistory
    chatterUserName: str
    twitchChannel: str

    @property
    def chatterUserId(self) -> str:
        return self.chatterTimeoutHistory.chatterUserId

    @property
    def entries(self) -> FrozenList[ChatterTimeoutHistoryEntry]:
        return self.chatterTimeoutHistory.entries

    @property
    def totalDurationSeconds(self) -> int:
        return self.chatterTimeoutHistory.totalDurationSeconds

    @property
    def totalDurationSecondsStr(self) -> str:
        return self.chatterTimeoutHistory.totalDurationSecondsStr

    @property
    def twitchChannelId(self) -> str:
        return self.chatterTimeoutHistory.twitchChannelId
