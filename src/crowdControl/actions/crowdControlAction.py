from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Final

from .crowdControlActionType import CrowdControlActionType
from ...misc import utils as utils


class CrowdControlAction(ABC):

    def __init__(
        self,
        dateTime: datetime,
        actionId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
    ):
        if not isinstance(dateTime, datetime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')
        elif not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')

        self.__dateTime: Final[datetime] = dateTime
        self.__actionId: Final[str] = actionId
        self.__chatterUserId: Final[str] = chatterUserId
        self.__chatterUserName: Final[str] = chatterUserName
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__twitchChatMessageId: Final[str | None] = twitchChatMessageId

        self.__handleAttempts: int = 0

    @property
    def actionId(self) -> str:
        return self.__actionId

    @property
    @abstractmethod
    def actionType(self) -> CrowdControlActionType:
        pass

    @property
    def chatterUserId(self) -> str:
        return self.__chatterUserId

    @property
    def chatterUserName(self) -> str:
        return self.__chatterUserName

    @property
    def dateTime(self) -> datetime:
        return self.__dateTime

    @property
    def handleAttempts(self) -> int:
        return self.__handleAttempts

    def incrementHandleAttempts(self):
        self.__handleAttempts += 1

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'actionType': self.actionType,
            'chatterUserId': self.__chatterUserId,
            'chatterUserName': self.__chatterUserName,
            'dateTime': self.__dateTime,
            'handleAttempts': self.__handleAttempts,
            'twitchChannel': self.__twitchChannel,
            'twitchChannelId': self.__twitchChannelId,
            'twitchChatMessageId': self.__twitchChatMessageId,
        }

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChatMessageId(self) -> str | None:
        return self.__twitchChatMessageId
