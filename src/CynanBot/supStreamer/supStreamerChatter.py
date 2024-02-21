from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class SupStreamerChatter():

    def __init__(
        self,
        mostRecentSup: Optional[SimpleDateTime],
        userId: str
    ):
        assert mostRecentSup is None or isinstance(mostRecentSup, SimpleDateTime), f"malformed {mostRecentSup=}"
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecentSup: Optional[SimpleDateTime] = mostRecentSup
        self.__userId: str = userId

    def __eq__(self, value: Any) -> bool:
        if isinstance(value, SupStreamerChatter):
            return self.__userId == value.__userId
        else:
            return False

    def getMostRecentSup(self) -> Optional[SimpleDateTime]:
        return self.__mostRecentSup

    def getUserId(self) -> str:
        return self.__userId

    def __hash__(self) -> int:
        return hash(self.__userId)

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'mostRecentSup': self.__mostRecentSup,
            'userId': self.__userId
        }
