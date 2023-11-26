import locale
from datetime import datetime
from typing import Optional

import misc.utils as utils


class ToxicTriviaResult():

    def __init__(
        self,
        mostRecent: Optional[datetime],
        newToxicCount: int,
        oldToxicCount: int,
        twitchChannel: str,
        userId: str
    ):
        if mostRecent is not None and not isinstance(mostRecent, datetime):
            raise ValueError(f'mostRecent argument is malformed: \"{mostRecent}\"')
        elif not utils.isValidInt(newToxicCount):
            raise ValueError(f'newToxicCount argument is malformed: \"{newToxicCount}\"')
        elif newToxicCount < 0 or newToxicCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newToxicCount argument is out of bounds: {newToxicCount}')
        elif not utils.isValidInt(oldToxicCount):
            raise ValueError(f'oldToxicCount argument is malformed: \"{oldToxicCount}\"')
        elif oldToxicCount < 0 or oldToxicCount > utils.getIntMaxSafeSize():
            raise ValueError(f'oldToxicCount argument is out of bounds: {oldToxicCount}')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecent: Optional[datetime] = mostRecent
        self.__newToxicCount: int = newToxicCount
        self.__oldToxicCount: int = oldToxicCount
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId

    def getMostRecent(self) -> Optional[datetime]:
        return self.__mostRecent

    def getNewToxicCount(self) -> int:
        return self.__newToxicCount

    def getNewToxicCountStr(self) -> str:
        return locale.format_string("%d", self.__newToxicCount, grouping = True)

    def getOldToxicCount(self) -> int:
        return self.__oldToxicCount

    def getOldToxicCountStr(self) -> str:
        return locale.format_string("%d", self.__oldToxicCount, grouping = True)

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def hasMostRecent(self) -> bool:
        return self.__mostRecent is not None
