from abc import ABC

import CynanBot.misc.utils as utils
from CynanBot.chatLogger.chatEventType import ChatEventType
from CynanBot.misc.simpleDateTime import SimpleDateTime


class AbsChatMessage(ABC):

    def __init__(
        self,
        chatEventType: ChatEventType,
        twitchChannel: str
    ):
        if not isinstance(chatEventType, ChatEventType):
            raise TypeError(f'chatEventType argument is malformed: \"{chatEventType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__chatEventType: ChatEventType = chatEventType
        self.__twitchChannel: str = twitchChannel
        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getChatEventType(self) -> ChatEventType:
        return self.__chatEventType

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
