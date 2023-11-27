from abc import abstractmethod
from typing import Optional

from CynanBot.twitch.configuration.twitchAuthor import TwitchAuthor
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable


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
