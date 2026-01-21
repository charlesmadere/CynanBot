from abc import ABC, abstractmethod

from ..absChatterItemAction import AbsChatterItemAction
from ..chatterItemType import ChatterItemType
from ....users.userInterface import UserInterface


class AbsChatterItemEvent(ABC):

    @abstractmethod
    def getEventId(self) -> str:
        pass

    def getItemType(self) -> ChatterItemType:
        return self.getOriginatingAction().getItemType()

    @abstractmethod
    def getOriginatingAction(self) -> AbsChatterItemAction:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.user.handle

    @property
    def twitchChannelId(self) -> str:
        return self.getOriginatingAction().getTwitchChannelId()

    @property
    def twitchChatMessageId(self) -> str | None:
        return self.getOriginatingAction().getTwitchChatMessageId()

    @property
    def user(self) -> UserInterface:
        return self.getOriginatingAction().getUser()
