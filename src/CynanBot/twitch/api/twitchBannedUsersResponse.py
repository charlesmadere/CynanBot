from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchBannedUser import TwitchBannedUser


class TwitchBannedUsersResponse():

    def __init__(
        self,
        users: Optional[List[TwitchBannedUser]],
        broadcasterId: str,
        requestedUserId: Optional[str]
    ):
        assert users is None or isinstance(users, List), f"malformed {users=}"
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        assert requestedUserId is None or isinstance(requestedUserId, str), f"malformed {requestedUserId=}"

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
