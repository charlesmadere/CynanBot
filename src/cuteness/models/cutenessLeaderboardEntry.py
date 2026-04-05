import locale
from dataclasses import dataclass

from .cutenessEntry import CutenessEntry


@dataclass(frozen = True, slots = True)
class CutenessLeaderboardEntry(CutenessEntry):
    cuteness: int
    rank: int
    chatterUserId: str
    twitchChannelId: str

    def getChatterUserId(self) -> str:
        return self.chatterUserId

    def getCuteness(self) -> int:
        return self.cuteness

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    @property
    def rankStr(self) -> str:
        return locale.format_string("%d", self.rank, grouping = True)
