from dataclasses import dataclass

from .cutenessDate import CutenessDate
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessResult import CutenessResult


@dataclass(frozen = True)
class CutenessLeaderboardResult():
    cutenessDate: CutenessDate
    specificLookupCutenessResult: CutenessResult | None = None
    entries: list[CutenessLeaderboardEntry] | None = None
