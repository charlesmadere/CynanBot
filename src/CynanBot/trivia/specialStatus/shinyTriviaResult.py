import locale
from datetime import datetime

import CynanBot.misc.utils as utils


class ShinyTriviaResult():

    def __init__(
        self,
        mostRecent: datetime | None,
        newShinyCount: int,
        oldShinyCount: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ):
        if mostRecent is not None and not isinstance(mostRecent, datetime):
            raise TypeError(f'mostRecent argument is malformed: \"{mostRecent}\"')
        elif not utils.isValidInt(newShinyCount):
            raise TypeError(f'newShinyCount argument is malformed: \"{newShinyCount}\"')
        elif newShinyCount < 0 or newShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'newShinyCount argument is out of bounds: {newShinyCount}')
        elif not utils.isValidInt(oldShinyCount):
            raise TypeError(f'oldShinyCount argument is malformed: \"{oldShinyCount}\"')
        elif oldShinyCount < 0 or oldShinyCount > utils.getIntMaxSafeSize():
            raise ValueError(f'oldShinyCount argument is out of bounds: {oldShinyCount}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecent: datetime | None = mostRecent
        self.__newShinyCount: int = newShinyCount
        self.__oldShinyCount: int = oldShinyCount
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId

    def getMostRecent(self) -> datetime | None:
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

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId
