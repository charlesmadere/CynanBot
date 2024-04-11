import locale

import CynanBot.misc.utils as utils
from CynanBot.chatLogger.absChatMessage import AbsChatMessage
from CynanBot.chatLogger.chatEventType import ChatEventType


class RaidMessage(AbsChatMessage):

    def __init__(
        self,
        raidSize: int,
        fromWho: str,
        twitchChannel: str
    ):
        super().__init__(
            chatEventType = ChatEventType.RAID,
            twitchChannel = twitchChannel
        )

        if not utils.isValidInt(raidSize):
            raise TypeError(f'raidSize argument is malformed: \"{raidSize}\"')
        elif raidSize < 0 or raidSize > utils.getIntMaxSafeSize():
            raise ValueError(f'raidSize argument is out of bounds: {raidSize}')
        elif not utils.isValidStr(fromWho):
            raise TypeError(f'fromWho argument is malformed: \"{fromWho}\"')

        self.__raidSize: int = raidSize
        self.__fromWho: str = fromWho

    def getFromWho(self) -> str:
        return self.__fromWho

    def getRaidSize(self) -> int:
        return self.__raidSize

    def getRaidSizeStr(self) -> str:
        return locale.format_string("%d", self.__raidSize, grouping = True)
