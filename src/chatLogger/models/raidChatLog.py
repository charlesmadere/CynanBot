import locale
from dataclasses import dataclass
from datetime import datetime

from .absChatLog import AbsChatLog


@dataclass(frozen = True, slots = True)
class RaidChatLog(AbsChatLog):
    dateTime: datetime
    viewers: int
    raidUserId: str
    raidUserLogin: str
    twitchChannel: str
    twitchChannelId: str

    def getDateTime(self) -> datetime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    @property
    def viewersStr(self) -> str:
        return locale.format_string("%d", self.viewers, grouping = True)
