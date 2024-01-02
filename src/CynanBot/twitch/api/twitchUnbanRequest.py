from typing import Any, Dict

import CynanBot.misc.utils as utils


# This class intends to directly correspond to Twitch's "Unban User" API:
# https://dev.twitch.tv/docs/api/reference/#unban-user
class TwitchUnbanRequest():

    def __init__(
        self,
        broadcasterUserId: str,
        moderatorUserId: str,
        userIdToBan: str
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise ValueError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(userIdToBan):
            raise ValueError(f'userIdToBan argument is malformed: \"{userIdToBan}\"')

        self.__broadcasterUserId: str = broadcasterUserId
        self.__moderatorUserId: str = moderatorUserId
        self.__userIdToBan: str = userIdToBan

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getModeratorUserId(self) -> str:
        return self.__moderatorUserId

    def getUserIdToBan(self) -> str:
        return self.__userIdToBan

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'broadcasterUserId': self.__broadcasterUserId,
            'moderatorUserId': self.__moderatorUserId,
            'userIdToBan': self.__userIdToBan
        }
