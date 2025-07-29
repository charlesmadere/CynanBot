import locale
from dataclasses import dataclass

from .absChatLog import AbsChatLog
from ...misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class CheerChatLog(AbsChatLog):
    bits: int | None
    dateTime: SimpleDateTime
    cheerUserId: str
    cheerUserLogin: str
    twitchChannel: str
    twitchChannelId: str

    @property
    def bitsStr(self) -> str:
        return locale.format_string("%d", self.bits, grouping = True)

    def getDateTime(self) -> SimpleDateTime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
