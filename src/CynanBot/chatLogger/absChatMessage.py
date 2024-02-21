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
        assert isinstance(chatEventType, ChatEventType), f"malformed {chatEventType=}"
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__chatEventType: ChatEventType = chatEventType
        self.__twitchChannel: str = twitchChannel
        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getChatEventType(self) -> ChatEventType:
        return self.__chatEventType

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
