from typing import List, Optional

import CynanBotCommon.utils as utils

from cuteness.cutenessDate import CutenessDate
from cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from cuteness.cutenessResult import CutenessResult


class CutenessLeaderboardResult():

    def __init__(
        self,
        cutenessDate: CutenessDate,
        specificLookupCutenessResult: Optional[CutenessResult] = None,
        entries: Optional[List[CutenessLeaderboardEntry]] = None
    ):
        if cutenessDate is None:
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__specificLookupCutenessResult: CutenessResult = specificLookupCutenessResult
        self.__entries: List[CutenessLeaderboardEntry] = entries

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getEntries(self) -> List[CutenessLeaderboardEntry]:
        return self.__entries

    def hasEntries(self) -> bool:
        return utils.hasItems(self.__entries)

    def hasSpecificLookupCutenessResult(self) -> bool:
        return self.__specificLookupCutenessResult is not None and self.__specificLookupCutenessResult.hasCuteness()

    def toStr(self, delimiter: str = ', ') -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not self.hasEntries():
            return f'Unfortunately the {self.__cutenessDate.toStr()} cuteness leaderboard is empty 😿'

        specificLookupText = ''
        if self.hasSpecificLookupCutenessResult():
            userName = self.__specificLookupCutenessResult.getUserName()
            cutenessStr = self.__specificLookupCutenessResult.getCutenessStr()
            specificLookupText = f'{userName} your cuteness is {cutenessStr}'

        entryStrings: List[str] = list()
        for entry in self.__entries:
            entryStrings.append(entry.toStr())

        if utils.isValidStr(specificLookupText):
            return f'{specificLookupText}, and the {self.__cutenessDate.toStr()} leaderboard is: {delimiter.join(entryStrings)} ✨'
        else:
            return f'The {self.__cutenessDate.toStr()} leaderboard is {delimiter.join(entryStrings)} ✨'
