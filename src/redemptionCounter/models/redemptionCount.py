import locale
from dataclasses import dataclass


@dataclass(frozen = True)
class RedemptionCount:
    count: int
    chatterUserId: str
    counterName: str
    twitchChannelId: str

    @property
    def countStr(self) -> str:
        return locale.format_string("%d", self.count, grouping = True)
