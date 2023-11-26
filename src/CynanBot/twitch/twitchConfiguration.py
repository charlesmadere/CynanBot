from abc import ABC, abstractmethod
from typing import Any

from CynanBot.twitch.twitchChannel import TwitchChannel
from CynanBot.twitch.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchConfigurationType import TwitchConfigurationType
from CynanBot.twitch.twitchContext import TwitchContext
from CynanBot.twitch.twitchMessage import TwitchMessage


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
