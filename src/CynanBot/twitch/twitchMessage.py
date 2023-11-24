from abc import ABC, abstractmethod
from typing import Optional

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchChannel import TwitchChannel
from twitch.twitchConfigurationType import TwitchConfigurationType


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
    def getContent(self) -> Optional[str]:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    def isEcho(self) -> bool:
        pass
