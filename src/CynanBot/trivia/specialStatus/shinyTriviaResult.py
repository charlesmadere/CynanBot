import locale
from datetime import datetime
from typing import Optional

import CynanBot.misc.utils as utils


class ShinyTriviaResult():

    def __init__(
        self,
        mostRecent: Optional[datetime],
        newShinyCount: int,
        oldShinyCount: int,
        twitchChannel: str,
        userId: str
    ):
        assert mostRecent is None or isinstance(mostRecent, datetime), f"malformed {mostRecent=}"
        if not utils.isValidInt(newShinyCount):
            raise ValueError(f'newShinyCount argument is malformed: \"{newShinyCount}\"')
        if newShinyCount < 0 or newShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newShinyCount argument is out of bounds: {newShinyCount}')
        if not utils.isValidInt(oldShinyCount):
            raise ValueError(f'oldShinyCount argument is malformed: \"{oldShinyCount}\"')
        if oldShinyCount < 0 or oldShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'oldShinyCount argument is out of bounds: {oldShinyCount}')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecent: Optional[datetime] = mostRecent
        self.__newShinyCount: int = newShinyCount
        self.__oldShinyCount: int = oldShinyCount
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId

    def getMostRecent(self) -> Optional[datetime]:
        return self.__mostRecent

    def getNewShinyCount(self) -> int:
        return self.__newShinyCount

    def getNewShinyCountStr(self) -> str:
        return locale.format_string("%d", self.__newShinyCount, grouping = True)

    def getOldShinyCount(self) -> int:
        return self.__oldShinyCount

    def getOldShinyCountStr(self) -> str:
        return locale.format_string("%d", self.__oldShinyCount, grouping = True)

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def hasMostRecent(self) -> bool:
        return self.__mostRecent is not None
