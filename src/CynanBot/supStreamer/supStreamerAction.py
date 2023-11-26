from typing import Any, Dict, Optional

import misc.utils as utils
from supStreamer.supStreamerChatter import SupStreamerChatter


class SupStreamerAction():

    def __init__(
        self,
        chatters: Dict[str, Optional[SupStreamerChatter]],
        broadcasterUserId: str,
        broadcasterUserName: str
    ):
        if not isinstance(chatters, Dict):
            raise ValueError(f'chatters argument is malformed: \"{chatters}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise ValueError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(broadcasterUserName):
            raise ValueError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')

        self.__chatters: Dict[str, Optional[SupStreamerChatter]] = chatters
        self.__broadcasterUserId: str = broadcasterUserId
        self.__broadcasterUserName: str = broadcasterUserName

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getBroadcasterUserName(self) -> str:
        return self.__broadcasterUserName

    def getChatters(self) -> Dict[str, Optional[SupStreamerChatter]]:
        return self.__chatters

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'chatters': self.__chatters,
            'broadcasterUserId': self.__broadcasterUserId,
            'broadcasterUserName': self.__broadcasterUserName
        }

    def updateChatter(self, chatter: SupStreamerChatter):
        self.__chatters[chatter.getUserId()] = chatter
