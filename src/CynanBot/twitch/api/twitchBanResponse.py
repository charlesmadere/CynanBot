from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
class TwitchBanResponse():

    def __init__(
        self,
        createdAt: SimpleDateTime,
        endTime: Optional[SimpleDateTime],
        broadcasterUserId: str,
        moderatorUserId: str,
        userId: str
    ):
        assert isinstance(createdAt, SimpleDateTime), f"malformed {createdAt=}"
        assert endTime is None or isinstance(endTime, SimpleDateTime), f"malformed {endTime=}"
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        if not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__createdAt: SimpleDateTime = createdAt
        self.__endTime: Optional[SimpleDateTime] = endTime
        self.__broadcasterUserId: str = broadcasterUserId
        self.__moderatorUserId: str = moderatorUserId
        self.__userId: str = userId

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getCreatedAt(self) -> SimpleDateTime:
        return self.__createdAt

    def getEndTime(self) -> Optional[SimpleDateTime]:
        return self.__endTime

    def getModeratorUserId(self) -> str:
        return self.__moderatorUserId

    def getUserId(self) -> str:
        return self.__userId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'broadcasterUserId': self.__broadcasterUserId,
            'createdAt': self.__createdAt,
            'endTime': self.__endTime,
            'moderatorUserId': self.__moderatorUserId,
            'userId': self.__userId
        }
