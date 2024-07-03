from abc import ABC, abstractmethod
from typing import Any

from .twitchChannel import TwitchChannel
from .twitchConfigurationType import TwitchConfigurationType
from .twitchContext import TwitchContext
from .twitchMessage import TwitchMessage


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
