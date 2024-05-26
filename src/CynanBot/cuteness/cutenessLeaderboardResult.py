from dataclasses import dataclass

from CynanBot.cuteness.cutenessDate import CutenessDate
from CynanBot.cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from CynanBot.cuteness.cutenessResult import CutenessResult


@dataclass(frozen = True)
class CutenessLeaderboardResult():
    cutenessDate: CutenessDate
    specificLookupCutenessResult: CutenessResult | None = None
    entries: list[CutenessLeaderboardEntry] | None = None
