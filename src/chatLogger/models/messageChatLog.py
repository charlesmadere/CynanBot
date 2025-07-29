from dataclasses import dataclass

from .absChatLog import AbsChatLog
from ...misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class MessageChatLog(AbsChatLog):
    bits: int | None
    dateTime: SimpleDateTime
    chatterUserId: str
    chatterUserLogin: str
    message: str
    twitchChannel: str
    twitchChannelId: str

    def getDateTime(self) -> SimpleDateTime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
