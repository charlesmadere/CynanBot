import locale
from datetime import datetime

import CynanBot.misc.utils as utils


class ToxicTriviaResult():

    def __init__(
        self,
        mostRecent: datetime | None,
        newToxicCount: int,
        oldToxicCount: int,
        twitchChannel: str,
        userId: str
    ):
        if mostRecent is not None and not isinstance(mostRecent, datetime):
            raise TypeError(f'mostRecent argument is malformed: \"{mostRecent}\"')
        elif not utils.isValidInt(newToxicCount):
            raise TypeError(f'newToxicCount argument is malformed: \"{newToxicCount}\"')
        elif newToxicCount < 0 or newToxicCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newToxicCount argument is out of bounds: {newToxicCount}')
        elif not utils.isValidInt(oldToxicCount):
            raise TypeError(f'oldToxicCount argument is malformed: \"{oldToxicCount}\"')
        elif oldToxicCount < 0 or oldToxicCount > utils.getIntMaxSafeSize():
            raise ValueError(f'oldToxicCount argument is out of bounds: {oldToxicCount}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecent: datetime | None = mostRecent
        self.__newToxicCount: int = newToxicCount
        self.__oldToxicCount: int = oldToxicCount
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId

    def getMostRecent(self) -> datetime | None:
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
