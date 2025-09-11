from dataclasses import dataclass

from .absChatterItemAction import AbsChatterItemAction
from .chatterItemType import ChatterItemType
from ...users.userInterface import UserInterface


@dataclass(frozen = True)
class TradeChatterItemAction(AbsChatterItemAction):
    itemType: ChatterItemType
    tradeAmount: int
    actionId: str
    fromChatterUserId: str
    toChatterUserId: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    user: UserInterface

    def getActionId(self) -> str:
        return self.actionId

    def getItemType(self) -> ChatterItemType:
        return self.itemType

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchChatMessageId(self) -> str | None:
        return self.twitchChatMessageId

    def getUser(self) -> UserInterface:
        return self.user
