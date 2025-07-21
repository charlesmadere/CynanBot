import locale
from typing import Final

from .absChatMessage import AbsChatMessage
from .chatEventType import ChatEventType
from ..misc import utils as utils
from ..misc.simpleDateTime import SimpleDateTime


class CheerMessage(AbsChatMessage):

    def __init__(
        self,
        bits: int,
        dateTime: SimpleDateTime,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        super().__init__(
            dateTime = dateTime,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 0 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__bits: Final[int] = bits
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName

    @property
    def bits(self) -> int:
        return self.__bits

    @property
    def bitsStr(self) -> str:
        return locale.format_string("%d", self.__bits, grouping = True)

    @property
    def chatEventType(self) -> ChatEventType:
        return ChatEventType.CHEER

    @property
    def userId(self) -> str:
        return self.__userId

    @property
    def userName(self) -> str:
        return self.__userName
