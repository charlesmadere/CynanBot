from dataclasses import dataclass
from datetime import datetime

from .absChatLog import AbsChatLog


@dataclass(frozen = True, slots = True)
class MessageChatLog(AbsChatLog):
    dateTime: datetime
    bits: int | None
    chatterUserId: str
    chatterUserLogin: str
    message: str
    twitchChannel: str
    twitchChannelId: str

    def getDateTime(self) -> datetime:
        return self.dateTime

    def getTwitchChannel(self) -> str:
        return self.twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId
