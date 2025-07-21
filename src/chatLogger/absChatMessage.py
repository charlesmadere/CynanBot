from abc import ABC, abstractmethod
from typing import Final

from .chatEventType import ChatEventType
from ..misc import utils as utils
from ..misc.simpleDateTime import SimpleDateTime


class AbsChatMessage(ABC):

    def __init__(
        self,
        dateTime: SimpleDateTime,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not isinstance(dateTime, SimpleDateTime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__dateTime: Final[SimpleDateTime] = dateTime
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    @abstractmethod
    def chatEventType(self) -> ChatEventType:
        pass

    @property
    def dateTime(self) -> SimpleDateTime:
        return self.__dateTime

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
