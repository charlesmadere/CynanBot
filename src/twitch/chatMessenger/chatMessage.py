from dataclasses import dataclass


@dataclass(frozen = True)
class ChatMessage:
    text: str
    twitchChannelId: str
    delaySeconds: int | None = None
    replyMessageId: str | None = None
