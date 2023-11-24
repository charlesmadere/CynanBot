from abc import ABC, abstractmethod
from typing import Any

from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchContext import TwitchContext
from twitch.twitchMessage import TwitchMessage


class TwitchConfiguration(ABC):

    @abstractmethod
    def getChannel(self, channel: Any) -> TwitchChannel:
        pass

    @abstractmethod
    async def getChannelPointsMessage(self, channelPointsMessage: Any) -> TwitchChannelPointsMessage:
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
