from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class WebsocketOutcomePredictor():

    def __init__(
        self,
        channelPointsUsed: int,
        channelPointsWon: Optional[int],
        userId: str,
        userLogin: str,
        userName: str
    ):
        if not utils.isValidInt(channelPointsUsed):
            raise ValueError(f'channelPointsUsed argument is malformed: \"{channelPointsUsed}\"')
        elif channelPointsUsed < 0 or channelPointsUsed > utils.getLongMaxSafeSize():
            raise ValueError(f'channelPointsUsed argument is out of bounds: {channelPointsUsed}')
        elif channelPointsWon is not None and not utils.isValidInt(channelPointsWon):
            raise ValueError(f'channelPointsWon argument is malformed: \"{channelPointsWon}\"')
        elif channelPointsWon is not None and (channelPointsWon < 0 or channelPointsWon > utils.getLongMaxSafeSize()):
            raise ValueError(f'channelPointsWon argument is out of bounds: {channelPointsWon}')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__channelPointsUsed: int = channelPointsUsed
        self.__channelPointsWon: Optional[int] = channelPointsWon
        self.__userId: str = userId
        self.__userLogin: str = userLogin
        self.__userName: str = userName

    def getChannelPointsUsed(self) -> int:
        return self.__channelPointsUsed

    def getChannelPointsWon(self) -> Optional[int]:
        return self.__channelPointsWon

    def getUserId(self) -> str:
        return self.__userId

    def getUserLogin(self) -> str:
        return self.__userLogin

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'channelPointsUsed': self.__channelPointsUsed,
            'channelPointsWon': self.__channelPointsWon,
            'userId': self.__userId,
            'userLogin': self.__userLogin,
            'userName': self.__userName
        }
