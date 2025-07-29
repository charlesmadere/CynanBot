import locale
from dataclasses import dataclass

from .absChatLog import AbsChatLog
from ...misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class RaidChatLog(AbsChatLog):
    viewers: int
    dateTime: SimpleDateTime
    raidUserId: str
    raidUserLogin: str
    twitchChannel: str
    twitchChannelId: str

    def getDateTime(self) -> SimpleDateTime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    @property
    def viewersStr(self) -> str:
        return locale.format_string("%d", self.viewers, grouping = True)
