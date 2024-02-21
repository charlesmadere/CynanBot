from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils


class TwitchBannedUserRequest():

    def __init__(
        self,
        broadcasterId: str,
        requestedUserId: Optional[str]
    ):
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        assert requestedUserId is None or isinstance(requestedUserId, str), f"malformed {requestedUserId=}"

        self.__broadcasterId: str = broadcasterId
        self.__requestedUserId: Optional[str] = requestedUserId

    def getBroadcasterId(self) -> str:
        return self.__broadcasterId

    def getRequestedUserId(self) -> Optional[str]:
        return self.__requestedUserId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'broadcasterId': self.__broadcasterId,
            'requestedUserId': self.__requestedUserId
        }
