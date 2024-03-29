from typing import Any

import CynanBot.misc.utils as utils


class TriviaGameController():

    def __init__(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'twitchChannel': self.__twitchChannel,
            'userId': self.__userId,
            'userName': self.__userName
        }
