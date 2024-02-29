from datetime import datetime
from typing import Any, Dict

import CynanBot.misc.utils as utils


class GoogleAccessToken():

    def __init__(
        self,
        expireTime: datetime,
        accessToken: str
    ):
        if not isinstance(expireTime, datetime):
            raise TypeError(f'expireTime argument is malformed: \"{expireTime}\"')
        elif utils.isValidStr(accessToken):
            raise TypeError(f'accessToken argument is malformed: \"{accessToken}\"')

        self.__expireTime: datetime = expireTime
        self.__accessToken: str = accessToken

    def getAccessToken(self) -> str:
        return self.__accessToken

    def getExpireTime(self) -> datetime:
        return self.__expireTime

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'accessToken': self.__accessToken,
            'expireTime': self.__expireTime
        }
