from abc import ABC, abstractmethod

from .chatterItemType import ChatterItemType
from ...users.userInterface import UserInterface


class AbsChatterItemAction(ABC):

    @abstractmethod
    def getActionId(self) -> str:
        pass

    @abstractmethod
    def getItemType(self) -> ChatterItemType:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChatMessageId(self) -> str | None:
        pass

    @abstractmethod
    def getUser(self) -> UserInterface:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.getUser().handle
