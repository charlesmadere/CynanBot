import locale
from dataclasses import dataclass

from frozenlist import FrozenList

from .chatterTimeoutHistoryEntry import ChatterTimeoutHistoryEntry


@dataclass(frozen = True, slots = True)
class ChatterTimeoutHistory:
    entries: FrozenList[ChatterTimeoutHistoryEntry]
    totalDurationSeconds: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def totalDurationSecondsStr(self) -> str:
        return locale.format_string("%d", self.totalDurationSeconds, grouping = True)
