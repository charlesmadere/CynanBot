from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.supStreamer.supStreamerChatter import SupStreamerChatter


class SupStreamerAction():

    def __init__(
        self,
        chatters: dict[str, SupStreamerChatter | None],
        broadcasterUserId: str,
        broadcasterUserName: str
    ):
        if not isinstance(chatters, dict):
            raise TypeError(f'chatters argument is malformed: \"{chatters}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(broadcasterUserName):
            raise TypeError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')

        self.__chatters: dict[str, SupStreamerChatter | None] = chatters
        self.__broadcasterUserId: str = broadcasterUserId
        self.__broadcasterUserName: str = broadcasterUserName

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getBroadcasterUserName(self) -> str:
        return self.__broadcasterUserName

    def getChatters(self) -> dict[str, SupStreamerChatter | None]:
        return self.__chatters

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'chatters': self.__chatters,
            'broadcasterUserId': self.__broadcasterUserId,
            'broadcasterUserName': self.__broadcasterUserName
        }

    def updateChatter(self, chatter: SupStreamerChatter):
        if not isinstance(chatter, SupStreamerChatter):
            raise TypeError(f'chatter argument is malformed: \"{chatter}\"')

        self.__chatters[chatter.getUserId()] = chatter
