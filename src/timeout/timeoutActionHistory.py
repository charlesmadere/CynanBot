from dataclasses import dataclass

from frozenlist import FrozenList

from .timeoutActionHistoryEntry import TimeoutActionHistoryEntry


@dataclass(frozen = True)
class TimeoutActionHistory:
    totalTimeouts: int
    entries: FrozenList[TimeoutActionHistoryEntry] | None
    chatterUserId: str
    twitchChannel: str
    twitchChannelId: str
