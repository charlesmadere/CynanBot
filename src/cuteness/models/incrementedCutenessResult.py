import locale
from dataclasses import dataclass
from datetime import datetime

from .cutenessEntry import CutenessEntry


@dataclass(frozen = True, slots = True)
class IncrementedCutenessResult(CutenessEntry):
    cutenessDate: datetime
    newCuteness: int
    previousCuteness: int
    chatterUserId: str
    twitchChannelId: str

    def getChatterUserId(self) -> str:
        return self.chatterUserId

    def getCuteness(self) -> int:
        return self.newCuteness

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    @property
    def newCutenessStr(self) -> str:
        return locale.format_string("%d", self.newCuteness, grouping = True)

    @property
    def previousCutenessStr(self) -> str:
        return locale.format_string("%d", self.previousCuteness, grouping = True)
