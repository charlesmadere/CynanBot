from datetime import datetime

import CynanBot.misc.utils as utils


class TwitchTokensDetails():

    def __init__(
        self,
        expirationTime: datetime,
        accessToken: str,
        refreshToken: str
    ):
        if not isinstance(expirationTime, datetime):
            raise ValueError(f'expirationTime argument is malformed: \"{expirationTime}\"')
        elif not utils.isValidStr(accessToken):
            raise ValueError(f'accessToken argument is malformed: \"{accessToken}\"')
        elif not utils.isValidStr(refreshToken):
            raise ValueError(f'refreshToken argument is malformed: \"{refreshToken}\"')

        self.__expirationTime: datetime = expirationTime
        self.__accessToken: str = accessToken
        self.__refreshToken: str = refreshToken

    def getAccessToken(self) -> str:
        return self.__accessToken

    def getExpirationTime(self) -> datetime:
        return self.__expirationTime

    def getRefreshToken(self) -> str:
        return self.__refreshToken

    def __str__(self) -> str:
        return f'expirationTime={self.__expirationTime}, accessToken=\"{self.__accessToken}\", refreshToken=\"{self.__refreshToken}\"'
