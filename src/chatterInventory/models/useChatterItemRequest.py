from dataclasses import dataclass

from .pointRedemptionItemRequestData import PointRedemptionItemRequestData
from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class UseChatterItemRequest:
    pointRedemption: PointRedemptionItemRequestData | None
    chatMessage: str | None
    chatterUserId: str
    requestId: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    user: UserInterface

    @property
    def twitchChannel(self) -> str:
        return self.user.handle
