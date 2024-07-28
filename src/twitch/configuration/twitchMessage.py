from abc import ABC, abstractmethod

from .twitchAuthor import TwitchAuthor
from .twitchChannel import TwitchChannel
from .twitchConfigurationType import TwitchConfigurationType


class TwitchMessage(ABC):

    @abstractmethod
    def getAuthor(self) -> TwitchAuthor:
        pass

    @abstractmethod
    def getAuthorId(self) -> str:
        pass

    @abstractmethod
    def getAuthorName(self) -> str:
        pass

    @abstractmethod
    def getChannel(self) -> TwitchChannel:
        pass

    @abstractmethod
    def getContent(self) -> str | None:
        pass

    @abstractmethod
    async def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @property
    @abstractmethod
    def isEcho(self) -> bool:
        pass

    @abstractmethod
    async def isReply(self) -> bool:
        pass
