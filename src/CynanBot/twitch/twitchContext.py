from abc import abstractmethod
from typing import Optional

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchMessageable import TwitchMessageable


class TwitchContext(TwitchMessageable):

    @abstractmethod
    def getAuthor(self) -> TwitchAuthor:
        pass

    @abstractmethod
    def getAuthorDisplayName(self) -> str:
        pass

    @abstractmethod
    def getAuthorId(self) -> str:
        pass

    @abstractmethod
    def getAuthorName(self) -> str:
        pass

    @abstractmethod
    def getMessageContent(self) -> Optional[str]:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    def isAuthorMod(self) -> bool:
        pass

    @abstractmethod
    def isAuthorVip(self) -> bool:
        pass

    @abstractmethod
    async def send(self, message: str):
        pass
