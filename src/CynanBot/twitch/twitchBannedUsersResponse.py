from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchBannedUser import TwitchBannedUser


class TwitchBannedUsersResponse():

    def __init__(
        self,
        users: Optional[List[TwitchBannedUser]],
        broadcasterId: str,
        requestedUserId: Optional[str]
    ):
        if users is not None and not isinstance(users, List):
            raise ValueError(f'users argument is malformed: \"{users}\"')
        elif not utils.isValidStr(broadcasterId):
            raise ValueError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif requestedUserId is not None and not isinstance(requestedUserId, str):
            raise ValueError(f'requestedUserId argument is malformed: \"{requestedUserId}\"')

        self.__users: Optional[List[TwitchBannedUser]] = users
        self.__broadcasterId: str = broadcasterId
        self.__requestedUserId: Optional[str] = requestedUserId

    def getBroadcasterId(self) -> str:
        return self.__broadcasterId

    def getRequestedUserId(self) -> Optional[str]:
        return self.__requestedUserId

    def getUsers(self) -> Optional[List[TwitchBannedUser]]:
        return self.__users

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'broadcasterId': self.__broadcasterId,
            'requestedUserId': self.__requestedUserId,
            'users': self.__users
        }
