from abc import ABC, abstractmethod
from typing import Any

from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage


class TwitchConfiguration(ABC):

    @abstractmethod
    def getChannel(self, channel: Any) -> TwitchChannel:
        pass

    @abstractmethod
    def getContext(self, context: Any) -> TwitchContext:
        pass

    @abstractmethod
    def getMessage(self, message: Any) -> TwitchMessage:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
