from dataclasses import dataclass
from datetime import datetime

from .cutenessEntry import CutenessEntry


@dataclass(frozen = True, slots = True)
class CutenessHistoryEntry(CutenessEntry):
    cutenessDate: datetime
    cuteness: int
    chatterUserId: str
    twitchChannelId: str

    def getChatterUserId(self) -> str:
        return self.chatterUserId

    def getCuteness(self) -> int:
        return self.cuteness

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
