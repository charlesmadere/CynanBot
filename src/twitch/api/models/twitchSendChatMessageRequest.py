from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchSendChatMessageRequest:
    broadcasterId: str
    message: str
    replyParentMessageId: str | None
    senderId: str
