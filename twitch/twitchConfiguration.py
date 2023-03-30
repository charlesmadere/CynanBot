from typing import Any

from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchContext import TwitchContext
from twitch.twitchMessage import TwitchMessage


class TwitchConfiguration():

    def getChannel(self, channel: Any) -> TwitchChannel:
        pass

    async def getChannelPointsMessage(self, channelPointsMessage: Any) -> TwitchChannelPointsMessage:
        pass

    def getContext(self, context: Any) -> TwitchContext:
        pass

    def getMessage(self, message: Any) -> TwitchMessage:
        pass

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
