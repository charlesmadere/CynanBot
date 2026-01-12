from dataclasses import dataclass

from .twitchSendChatDropReason import TwitchSendChatDropReason


@dataclass(frozen = True)
class TwitchSendChatMessageResponseEntry:
    isSent: bool
    messageId: str
    dropReason: TwitchSendChatDropReason | None
