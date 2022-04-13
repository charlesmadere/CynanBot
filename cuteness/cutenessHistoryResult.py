import locale
from typing import List

import CynanBotCommon.utils as utils

from cuteness.cutenessHistoryEntry import CutenessHistoryEntry


class CutenessHistoryResult():

    def __init__(
        self,
        userId: str,
        userName: str,
        bestCuteness: CutenessHistoryEntry = None,
        totalCuteness: int = None,
        entries: List[CutenessHistoryEntry] = None
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif totalCuteness is not None and not utils.isValidNum(totalCuteness):
            raise ValueError(f'totalCuteness argument is malformed: \"{totalCuteness}\"')

        self.__userId: str = userId
        self.__userName: str = userName
        self.__bestCuteness: CutenessHistoryEntry = bestCuteness
        self.__totalCuteness: int = totalCuteness
        self.__entries: List[CutenessHistoryEntry] = entries

    def getBestCuteness(self) -> CutenessHistoryEntry:
        return self.__bestCuteness

    def getEntries(self) -> List[CutenessHistoryEntry]:
        return self.__entries

    def getTotalCuteness(self) -> int:
        return self.__totalCuteness

    def getTotalCutenessStr(self) -> str:
        return locale.format_string("%d", self.__totalCuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def hasBestCuteness(self) -> bool:
        return self.__bestCuteness is not None

    def hasEntries(self) -> bool:
        return utils.hasItems(self.__entries)

    def hasTotalCuteness(self) -> bool:
        return utils.isValidNum(self.__totalCuteness) and self.__totalCuteness >= 1
