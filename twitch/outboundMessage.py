from datetime import datetime

from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils


class OutboundMessage():

    def __init__(
        self,
        delayUntilTime: datetime,
        messageable: Messageable,
        message: str,
        twitchChannel: str
    ):
        if not isinstance(delayUntilTime, datetime):
            raise ValueError(f'delayUntilTime argument is malformed: \"{delayUntilTime}\"')
        elif not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__delayUntilTime: datetime = delayUntilTime
        self.__messageable: Messageable = messageable
        self.__message: str = message
        self.__twitchChannel: str = twitchChannel

    def getDelayUntilTime(self) -> datetime:
        return self.__delayUntilTime

    def getMessage(self) -> str:
        return self.__message

    def getMessageable(self) -> Messageable:
        return self.__messageable

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
