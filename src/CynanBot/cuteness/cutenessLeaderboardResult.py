from typing import Any

from CynanBot.cuteness.cutenessDate import CutenessDate
from CynanBot.cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from CynanBot.cuteness.cutenessResult import CutenessResult


class CutenessLeaderboardResult():

    def __init__(
        self,
        cutenessDate: CutenessDate,
        specificLookupCutenessResult: CutenessResult | None = None,
        entries: list[CutenessLeaderboardEntry] | None = None
    ):
        if not isinstance(cutenessDate, CutenessDate):
            raise TypeError(f'cutenessDate argument is malformed: \"{cutenessDate}\"')
        elif specificLookupCutenessResult is not None and not isinstance(specificLookupCutenessResult, CutenessResult):
            raise TypeError(f'specificLookupCutenessResult argument is malformed: \"{specificLookupCutenessResult}\"')
        elif entries is not None and not isinstance(entries, list):
            raise TypeError(f'entries argument is malformed: \"{entries}\"')

        self.__cutenessDate: CutenessDate = cutenessDate
        self.__specificLookupCutenessResult: CutenessResult | None = specificLookupCutenessResult
        self.__entries: list[CutenessLeaderboardEntry] | None = entries

    def getCutenessDate(self) -> CutenessDate:
        return self.__cutenessDate

    def getEntries(self) -> list[CutenessLeaderboardEntry] | None:
        return self.__entries

    def getSpecificLookupCutenessResult(self) -> CutenessResult | None:
        return self.__specificLookupCutenessResult

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'cutenessDate': self.__cutenessDate,
            'entries': self.__entries,
            'specificLookupCutenessResult': self.__specificLookupCutenessResult
        }
