from datetime import datetime

import CynanBotCommon.utils as utils
from twitch.twitchMessageable import TwitchMessageable


class OutboundMessage():

    def __init__(
        self,
        delayUntilTime: datetime,
        messageable: TwitchMessageable,
        message: str
    ):
        if not isinstance(delayUntilTime, datetime):
            raise ValueError(f'delayUntilTime argument is malformed: \"{delayUntilTime}\"')
        elif not isinstance(messageable, TwitchMessageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        self.__delayUntilTime: datetime = delayUntilTime
        self.__messageable: TwitchMessageable = messageable
        self.__message: str = message

    def getDelayUntilTime(self) -> datetime:
        return self.__delayUntilTime

    def getMessage(self) -> str:
        return self.__message

    def getMessageable(self) -> TwitchMessageable:
        return self.__messageable
