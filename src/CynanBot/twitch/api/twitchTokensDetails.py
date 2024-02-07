from datetime import datetime
from typing import Any, Dict

import CynanBot.misc.utils as utils


class TwitchTokensDetails():

    def __init__(
        self,
        expirationTime: datetime,
        accessToken: str,
        refreshToken: str
    ):
        if not isinstance(expirationTime, datetime):
            raise TypeError(f'expirationTime argument is malformed: \"{expirationTime}\"')
        elif not utils.isValidStr(accessToken):
            raise TypeError(f'accessToken argument is malformed: \"{accessToken}\"')
        elif not utils.isValidStr(refreshToken):
            raise TypeError(f'refreshToken argument is malformed: \"{refreshToken}\"')

        self.__expirationTime: datetime = expirationTime
        self.__accessToken: str = accessToken
        self.__refreshToken: str = refreshToken

    def getAccessToken(self) -> str:
        return self.__accessToken

    def getExpirationTime(self) -> datetime:
        return self.__expirationTime

    def getRefreshToken(self) -> str:
        return self.__refreshToken

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'accessToken': self.__accessToken,
            'expirationTime': self.__expirationTime,
            'refreshToken': self.__refreshToken
        }
