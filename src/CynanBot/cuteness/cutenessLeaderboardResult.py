from typing import List, Optional

import misc.utils as utils
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
        if not isinstance(cutenessDate, CutenessDate):
            raise ValueError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__specificLookupCutenessResult: CutenessResult = specificLookupCutenessResult
        self.__entries: List[CutenessLeaderboardEntry] = entries

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getEntries(self) -> Optional[List[CutenessLeaderboardEntry]]:
        return self.__entries

    def getSpecificLookupCutenessResult(self) -> Optional[CutenessResult]:
        return self.__specificLookupCutenessResult

    def hasEntries(self) -> bool:
        return utils.hasItems(self.__entries)

    def hasSpecificLookupCutenessResult(self) -> bool:
        return self.__specificLookupCutenessResult is not None and self.__specificLookupCutenessResult.hasCuteness()
