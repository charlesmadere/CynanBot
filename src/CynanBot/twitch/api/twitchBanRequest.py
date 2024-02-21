from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.exceptions import TimeoutDurationSecondsTooLongException


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
class TwitchBanRequest():

    def __init__(
        self,
        duration: Optional[int],
        broadcasterUserId: str,
        moderatorUserId: str,
        reason: Optional[str],
        userIdToBan: str
    ):
        if duration is not None and not utils.isValidInt(duration):
            raise TypeError(f'duration argument is malformed: \"{duration}\"')
        if duration is not None and duration < 1:
            raise ValueError(f'duration argument is out of bounds: {duration}')
        if duration is not None and duration > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'duration argument is out of bounds: {duration}')
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        if not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        assert reason is None or isinstance(reason, str), f"malformed {reason=}"
        if not utils.isValidStr(userIdToBan):
            raise TypeError(f'userIdToBan argument is malformed: \"{userIdToBan}\"')

        self.__duration: Optional[int] = duration
        self.__broadcasterUserId: str = broadcasterUserId
        self.__moderatorUserId: str = moderatorUserId
        self.__reason: Optional[str] = reason
        self.__userIdToBan: str = userIdToBan

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getDuration(self) -> Optional[int]:
        return self.__duration

    def getModeratorUserId(self) -> str:
        return self.__moderatorUserId

    def getReason(self) -> Optional[str]:
        return self.__reason

    def getUserIdToBan(self) -> str:
        return self.__userIdToBan

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'duration': self.__duration,
            'broadcasterUserId': self.__broadcasterUserId,
            'moderatorUserId': self.__moderatorUserId,
            'reason': self.__reason,
            'userIdToBan': self.__userIdToBan
        }

    def toJson(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'user_id': self.__userIdToBan
        }

        if utils.isValidInt(self.__duration):
            data['duration'] = self.__duration

        if utils.isValidStr(self.__reason):
            data['reason'] = self.__reason

        return {
            'data': data
        }
