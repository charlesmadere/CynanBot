from typing import Any

import CynanBot.misc.utils as utils


class TwitchWebsocketUser():

    def __init__(
        self,
        userId: str,
        userName: str
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__userId: str = userId
        self.__userName: str = userName

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TwitchWebsocketUser):
            return False

        return self.__userId == other.__userId

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __hash__(self) -> int:
        return hash(self.__userId)

    def __repr__(self) -> str:
        return self.getUserName()

    def toDictionary(self) -> dict[str, Any]:
        return {
            'userId': self.__userId,
            'userName': self.__userName
        }
