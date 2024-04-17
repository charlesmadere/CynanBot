from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.twitch.exceptions import TimeoutDurationSecondsTooLongException


# This class intends to directly correspond to Twitch's "Ban User" API:
# https://dev.twitch.tv/docs/api/reference/#ban-user
class TwitchBanRequest():

    def __init__(
        self,
        duration: int | None,
        broadcasterUserId: str,
        moderatorUserId: str,
        reason: str | None,
        userIdToBan: str
    ):
        if duration is not None and not utils.isValidInt(duration):
            raise TypeError(f'duration argument is malformed: \"{duration}\"')
        elif duration is not None and duration < 1:
            raise ValueError(f'duration argument is out of bounds: {duration}')
        elif duration is not None and duration > 1209600:
            raise TimeoutDurationSecondsTooLongException(f'duration argument is out of bounds: {duration}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif reason is not None and not isinstance(reason, str):
            raise TypeError(f'reason argument is malformed: \"{reason}\"')
        elif not utils.isValidStr(userIdToBan):
            raise TypeError(f'userIdToBan argument is malformed: \"{userIdToBan}\"')

        self.__duration: int | None = duration
        self.__broadcasterUserId: str = broadcasterUserId
        self.__moderatorUserId: str = moderatorUserId
        self.__reason: str | None = reason
        self.__userIdToBan: str = userIdToBan

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getDuration(self) -> int | None:
        return self.__duration

    def getModeratorUserId(self) -> str:
        return self.__moderatorUserId

    def getReason(self) -> str | None:
        return self.__reason

    def getUserIdToBan(self) -> str:
        return self.__userIdToBan

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'duration': self.__duration,
            'broadcasterUserId': self.__broadcasterUserId,
            'moderatorUserId': self.__moderatorUserId,
            'reason': self.__reason,
            'userIdToBan': self.__userIdToBan
        }

    def toJson(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            'user_id': self.__userIdToBan
        }

        if utils.isValidInt(self.__duration):
            data['duration'] = self.__duration

        if utils.isValidStr(self.__reason):
            data['reason'] = self.__reason

        return {
            'data': data
        }
