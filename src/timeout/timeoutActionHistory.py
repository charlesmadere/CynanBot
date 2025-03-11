from dataclasses import dataclass

from frozenlist import FrozenList

from .timeoutActionHistoryEntry import TimeoutActionHistoryEntry


@dataclass(frozen = True)
class TimeoutActionHistory:
    entries: FrozenList[TimeoutActionHistoryEntry] | None
    totalTimeouts: int
    chatterUserId: str
    twitchChannel: str
    twitchChannelId: str
