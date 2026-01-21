import locale
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class ShinyTriviaResult:
    mostRecent: datetime | None
    newShinyCount: int
    oldShinyCount: int
    twitchChannel: str
    twitchChannelId: str
    userId: str

    @property
    def newShinyCountStr(self) -> str:
        return locale.format_string("%d", self.newShinyCount, grouping = True)

    @property
    def oldShinyCountStr(self) -> str:
        return locale.format_string("%d", self.oldShinyCount, grouping = True)
