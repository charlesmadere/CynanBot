import locale
from datetime import datetime
from typing import Optional

import misc.utils as utils


class ShinyTriviaResult():

    def __init__(
        self,
        mostRecent: Optional[datetime],
        newShinyCount: int,
        oldShinyCount: int,
        twitchChannel: str,
        userId: str
    ):
        if mostRecent is not None and not isinstance(mostRecent, datetime):
            raise ValueError(f'mostRecent argument is malformed: \"{mostRecent}\"')
        elif not utils.isValidInt(newShinyCount):
            raise ValueError(f'newShinyCount argument is malformed: \"{newShinyCount}\"')
        elif newShinyCount < 0 or newShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newShinyCount argument is out of bounds: {newShinyCount}')
        elif not utils.isValidInt(oldShinyCount):
            raise ValueError(f'oldShinyCount argument is malformed: \"{oldShinyCount}\"')
        elif oldShinyCount < 0 or oldShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'oldShinyCount argument is out of bounds: {oldShinyCount}')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
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
