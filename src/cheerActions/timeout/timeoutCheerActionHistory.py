from dataclasses import dataclass

from frozenlist import FrozenList

from .timeoutCheerActionEntry import TimeoutCheerActionEntry


@dataclass(frozen = True)
class TimeoutCheerActionHistory:
    totalTimeouts: int
    entries: FrozenList[TimeoutCheerActionEntry] | None
    chatterUserId: str
    twitchChannel: str
    twitchChannelId: str
