from abc import ABC, abstractmethod

from ..chatterItemType import ChatterItemType
from ..useChatterItemAction import UseChatterItemAction


class UseChatterItemEvent(ABC):

    @abstractmethod
    def getEventId(self) -> str:
        pass

    @abstractmethod
    def getOriginatingAction(self) -> UseChatterItemAction:
        pass

    @property
    @abstractmethod
    def itemType(self) -> ChatterItemType:
        pass

    @property
    def twitchChannel(self) -> str:
        return self.getOriginatingAction().twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.getOriginatingAction().twitchChannelId

    @property
    def twitchChatMessageId(self) -> str | None:
        return self.getOriginatingAction().twitchChatMessageId
