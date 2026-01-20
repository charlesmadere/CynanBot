from dataclasses import dataclass

from .twitchChatAnnouncementColor import TwitchChatAnnouncementColor


@dataclass(frozen = True, slots = True)
class TwitchSendChatAnnouncementRequest:
    broadcasterId: str
    message: str
    moderatorId: str
    color: TwitchChatAnnouncementColor | None
