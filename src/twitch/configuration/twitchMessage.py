from abc import ABC, abstractmethod

from .twitchAuthor import TwitchAuthor
from .twitchChannel import TwitchChannel
from .twitchConfigurationType import TwitchConfigurationType
from .twitchMessageTags import TwitchMessageTags


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
    async def getMessageId(self) -> str:
        pass

    @abstractmethod
    async def getTags(self) -> TwitchMessageTags:
        pass

    @abstractmethod
    async def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @property
    @abstractmethod
    def isEcho(self) -> bool:
        pass

    @abstractmethod
    async def isMessageFromExternalSharedChat(self) -> bool:
        pass

    @abstractmethod
    async def isReply(self) -> bool:
        pass

    @property
    @abstractmethod
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        pass
