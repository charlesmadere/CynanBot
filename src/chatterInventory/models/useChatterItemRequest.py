from dataclasses import dataclass

from .chatterItemType import ChatterItemType
from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class UseChatterItemRequest:
    ignoreInventory: bool
    itemType: ChatterItemType | None
    chatMessage: str | None
    chatterUserId: str
    requestId: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    user: UserInterface

    @property
    def twitchChannel(self) -> str:
        return self.user.handle
