from dataclasses import dataclass


@dataclass(frozen = True)
class CrowdControlMessage:
    message: str
    twitchChannel: str
    twitchChannelId: str
    twitchChatMessageId: str | None
