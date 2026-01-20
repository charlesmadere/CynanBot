from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class ChatMessage:
    text: str
    twitchChannelId: str
    sendAfter: datetime | None = None
    replyMessageId: str | None = None
