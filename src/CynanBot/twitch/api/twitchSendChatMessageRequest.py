from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchSendChatMessageRequest():
    broadcasterId: str
    message: str
    replyParentMessageId: str | None
    senderId: str
