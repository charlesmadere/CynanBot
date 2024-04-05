import locale

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessHistoryEntry import CutenessHistoryEntry


class CutenessHistoryResult():

    def __init__(
        self,
        userId: str,
        userName: str,
        bestCuteness: CutenessHistoryEntry | None = None,
        totalCuteness: int | None = None,
        entries: list[CutenessHistoryEntry] | None = None
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif bestCuteness is not None and not isinstance(bestCuteness, CutenessHistoryEntry):
            raise ValueError(f'bestCuteness argument is malformed: \"{bestCuteness}\"')
        elif totalCuteness is not None and not utils.isValidInt(totalCuteness):
            raise ValueError(f'totalCuteness argument is malformed: \"{totalCuteness}\"')
        elif totalCuteness is not None and (totalCuteness < 0 or totalCuteness > utils.getLongMaxSafeSize()):
            raise ValueError(f'totalCuteness argument is out of bounds: {totalCuteness}')
        elif entries is not None and not isinstance(entries, list):
            raise ValueError(f'entries argument is malformed: \"{entries}\"')

        self.__userId: str = userId
        self.__userName: str = userName
        self.__bestCuteness: CutenessHistoryEntry | None = bestCuteness
        self.__totalCuteness: int | None = totalCuteness
        self.__entries: list[CutenessHistoryEntry] | None = entries

    def getBestCuteness(self) -> CutenessHistoryEntry | None:
        return self.__bestCuteness

    def getEntries(self) -> list[CutenessHistoryEntry] | None:
        return self.__entries

    def getTotalCuteness(self) -> int | None:
        return self.__totalCuteness

    def getTotalCutenessStr(self) -> str:
        totalCuteness = self.requireTotalCuteness()
        return locale.format_string("%d", totalCuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def requireTotalCuteness(self) -> int:
        totalCuteness = self.__totalCuteness

        if not utils.isValidInt(totalCuteness):
            raise RuntimeError(f'No totalCuteness value is available: {totalCuteness}')

        return totalCuteness
