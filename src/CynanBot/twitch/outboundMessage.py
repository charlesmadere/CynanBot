from datetime import datetime

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchMessageable import TwitchMessageable


class OutboundMessage():

    def __init__(
        self,
        delayUntilTime: datetime,
        message: str,
        messageable: TwitchMessageable
    ):
        if not isinstance(delayUntilTime, datetime):
            raise ValueError(f'delayUntilTime argument is malformed: \"{delayUntilTime}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(messageable, TwitchMessageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')

        self.__delayUntilTime: datetime = delayUntilTime
        self.__message: str = message
        self.__messageable: TwitchMessageable = messageable

    def getDelayUntilTime(self) -> datetime:
        return self.__delayUntilTime

    def getMessage(self) -> str:
        return self.__message

    def getMessageable(self) -> TwitchMessageable:
        return self.__messageable
