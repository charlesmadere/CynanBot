import locale

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class AnivCopyMessageTimeoutScore:
    mostRecentDodge: datetime | None
    mostRecentTimeout: datetime | None
    dodgeScore: int
    timeoutScore: int
    chatterUserId: str
    twitchChannelId: str

    @property
    def dodgeScoreStr(self) -> str:
        return locale.format_string("%d", self.dodgeScore, grouping = True)

    @property
    def timeoutScoreStr(self) -> str:
        return locale.format_string("%d", self.timeoutScore, grouping = True)
