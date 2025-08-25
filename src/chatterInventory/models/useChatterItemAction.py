from dataclasses import dataclass

from .chatterItemType import ChatterItemType
from .pointRedemptionItemRequestData import PointRedemptionItemRequestData
from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class UseChatterItemAction:
    ignoreInventory: bool
    itemType: ChatterItemType
    pointRedemption: PointRedemptionItemRequestData | None
    actionId: str
    chatMessage: str | None
    chatterUserId: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    user: UserInterface

    @property
    def twitchChannel(self) -> str:
        return self.user.handle
