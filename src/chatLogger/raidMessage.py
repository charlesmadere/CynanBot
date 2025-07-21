import locale
from typing import Final

from .absChatMessage import AbsChatMessage
from .chatEventType import ChatEventType
from ..misc import utils as utils
from ..misc.simpleDateTime import SimpleDateTime


class RaidMessage(AbsChatMessage):

    def __init__(
        self,
        raidSize: int,
        dateTime: SimpleDateTime,
        fromWho: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            dateTime = dateTime,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidInt(raidSize):
            raise TypeError(f'raidSize argument is malformed: \"{raidSize}\"')
        elif raidSize < 0 or raidSize > utils.getIntMaxSafeSize():
            raise ValueError(f'raidSize argument is out of bounds: {raidSize}')
        elif not utils.isValidStr(fromWho):
            raise TypeError(f'fromWho argument is malformed: \"{fromWho}\"')

        self.__raidSize: Final[int] = raidSize
        self.__fromWho: Final[str] = fromWho

    @property
    def chatEventType(self) -> ChatEventType:
        return ChatEventType.RAID

    @property
    def fromWho(self) -> str:
        return self.__fromWho

    @property
    def raidSize(self) -> int:
        return self.__raidSize

    @property
    def raidSizeStr(self) -> str:
        return locale.format_string("%d", self.__raidSize, grouping = True)
