import locale
from dataclasses import dataclass
from datetime import datetime

from .absChatLog import AbsChatLog


@dataclass(frozen = True)
class CheerChatLog(AbsChatLog):
    dateTime: datetime
    bits: int | None
    cheerUserId: str
    cheerUserLogin: str
    twitchChannel: str
    twitchChannelId: str

    @property
    def bitsStr(self) -> str:
        return locale.format_string("%d", self.bits, grouping = True)

    def getDateTime(self) -> datetime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
