from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class SupStreamerChatter():

    def __init__(
        self,
        mostRecentSup: SimpleDateTime | None,
        userId: str
    ):
        if mostRecentSup is not None and not isinstance(mostRecentSup, SimpleDateTime):
            raise TypeError(f'mostRecentSup argument is malformed: \"{mostRecentSup}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecentSup: SimpleDateTime | None = mostRecentSup
        self.__userId: str = userId

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, SupStreamerChatter):
            return self.__userId == value.__userId
        else:
            return False

    def getMostRecentSup(self) -> SimpleDateTime | None:
        return self.__mostRecentSup

    def getUserId(self) -> str:
        return self.__userId

    def __hash__(self) -> int:
        return hash(self.__userId)

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'mostRecentSup': self.__mostRecentSup,
            'userId': self.__userId
        }
