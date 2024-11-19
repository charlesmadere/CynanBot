from dataclasses import dataclass


@dataclass(frozen = True)
class CrowdControlMessage:
    chatterUserId: str
    chatterUserName: str
    message: str
    twitchChannel: str
    twitchChannelId: str
    twitchChatMessageId: str | None
