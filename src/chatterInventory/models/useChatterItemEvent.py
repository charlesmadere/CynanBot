from abc import ABC, abstractmethod

from .chatterItemType import ChatterItemType


class UseChatterItemEvent(ABC):

    @abstractmethod
    def getActionId(self) -> str:
        pass

    @abstractmethod
    def getEventId(self) -> str:
        pass

    @abstractmethod
    def getItemType(self) -> ChatterItemType:
        pass

    @abstractmethod
    def getTwitchChannel(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass
