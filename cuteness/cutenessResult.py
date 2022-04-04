import locale
from typing import List, Optional

import CynanBotCommon.utils as utils

from cuteness.cutenessDate import CutenessDate
from cuteness.cutenessEntry import CutenessEntry


class CutenessResult():

    def __init__(
        self,
        cutenessDate: CutenessDate,
        cuteness: Optional[int],
        localLeaderboard: Optional[List[CutenessEntry]],
        userId: str,
        userName: str
    ):
        if cutenessDate is None:
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__cuteness: int = cuteness
        self.__localLeaderboard: List[CutenessEntry] = localLeaderboard
        self.__userId: str = userId
        self.__userName: str = userName

    def getCuteness(self) -> int:
        return self.__cuteness

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getCutenessStr(self) -> str:
        return locale.format_string("%d", self.__cuteness, grouping = True)

    def getLocalLeaderboard(self) -> List[CutenessEntry]:
        return self.__localLeaderboard

    def getLocalLeaderboardStr(self, delimiter: str = ', ') -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasLocalLeaderboard():
            return ''

        strings: List[str] = list()

        for entry in self.__localLeaderboard:
            strings.append(entry.toStr())

        return delimiter.join(strings)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def hasCuteness(self) -> bool:
        return utils.isValidNum(self.__cuteness)

    def hasLocalLeaderboard(self) -> bool:
        return utils.hasItems(self.__localLeaderboard)

    def toStr(self, delimiter: str = ', ') -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if self.hasCuteness() and self.__cuteness >= 1:
            if self.hasLocalLeaderboard():
                return f'{self.getUserName()}\'s {self.__cutenessDate.toStr()} cuteness is {self.getCutenessStr()}, and their local leaderboard is: {self.getLocalLeaderboardStr(delimiter)} ✨'
            else:
                return f'{self.getUserName()}\'s {self.__cutenessDate.toStr()} cuteness is {self.getCutenessStr()} ✨'
        else:
            return f'{self.getUserName()} has no cuteness in {self.__cutenessDate.toStr()} 😿'
