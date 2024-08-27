from datetime import datetime
from typing import Any

from .crowdControlButton import CrowdControlButton
from ..misc import utils as utils


class CrowdControlInput:

    def __init__(
        self,
        button: CrowdControlButton,
        dateTime: datetime,
        chatterUserId: str,
        chatterUserName: str,
        inputId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not isinstance(button, CrowdControlButton):
            raise TypeError(f'button argument is malformed: \"{button}\"')
        elif not isinstance(dateTime, datetime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')
        elif not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        elif not utils.isValidStr(chatterUserName):
            raise TypeError(f'chatterUserName argument is malformed: \"{chatterUserName}\"')
        elif not utils.isValidStr(inputId):
            raise TypeError(f'inputId argument is malformed: \"{inputId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__button: CrowdControlButton = button
        self.__dateTime: datetime = dateTime
        self.__chatterUserId: str = chatterUserId
        self.__chatterUserName: str = chatterUserName
        self.__inputId: str = inputId
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId

        self.__handleAttempts: int = 0

    @property
    def button(self) -> CrowdControlButton:
        return self.__button

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
        self.__handleAttempts = self.__handleAttempts + 1

    @property
    def inputId(self) -> str:
        return self.__inputId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'button': self.__button,
            'chatterUserId': self.__chatterUserId,
            'chatterUserName': self.__chatterUserName,
            'dateTime': self.__dateTime,
            'handleAttempts': self.__handleAttempts,
            'inputId': self.__inputId,
            'twitchChannel': self.__twitchChannel,
            'twitchChannelId': self.__twitchChannelId
        }

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
