from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchMessageable import TwitchMessageable


class TwitchIoMessageable(TwitchMessageable):

    def __init__(self, messageable: Messageable, twitchChannelName: str):
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(twitchChannelName):
            raise ValueError(f'twitchChannelName argument is malformed: \"{twitchChannelName}\"')

        self.__messageable: Messageable = messageable
        self.__twitchChannelName: str = twitchChannelName

    def getTwitchChannelName(self) -> str:
        return self.__twitchChannelName

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    async def send(self, message: str):
        await self.__messageable.send(message)
