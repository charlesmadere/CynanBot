import locale

import CynanBotCommon.utils as utils

from cuteness.cutenessEntry import CutenessEntry


class CutenessLeaderboardEntry(CutenessEntry):

    def __init__(
        self,
        cuteness: int,
        rank: int,
        userId: str,
        userName: str
    ):
        super().__init__(
            cuteness = cuteness,
            userId = userId,
            userName = userName
        )

        if not utils.isValidNum(rank):
            raise ValueError(f'rank argument is malformed: \"{rank}\"')

        self.__rank: int = rank

    def getRank(self) -> int:
        return self.__rank

    def getRankStr(self) -> str:
        return locale.format_string("%d", self.__rank, grouping = True)

    def toStr(self) -> str:
        return f'#{self.getRankStr()} {self.getUserName()} ({self.getCutenessStr()})'
