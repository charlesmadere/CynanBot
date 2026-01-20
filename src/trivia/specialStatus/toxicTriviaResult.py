import locale
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class ToxicTriviaResult:
    mostRecent: datetime | None
    newToxicCount: int
    oldToxicCount: int
    twitchChannel: str
    twitchChannelId: str
    userId: str

    @property
    def newToxicCountStr(self) -> str:
        return locale.format_string("%d", self.newToxicCount, grouping = True)

    @property
    def oldToxicCountStr(self) -> str:
        return locale.format_string("%d", self.oldToxicCount, grouping = True)
