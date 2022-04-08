from typing import List

import CynanBotCommon.utils as utils

from cuteness.cutenessHistoryEntry import CutenessHistoryEntry


class CutenessHistoryResult():

    def __init__(
        self,
        userId: str,
        userName: str,
        entries: List[CutenessHistoryEntry] = None
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userId: str = userId
        self.__userName: str = userName
        self.__entries: List[CutenessHistoryEntry] = entries

    def getEntries(self) -> List[CutenessHistoryEntry]:
        return self.__entries

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def hasEntries(self) -> bool:
        return utils.hasItems(self.__entries)
