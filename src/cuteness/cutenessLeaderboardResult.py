from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessDate import CutenessDate
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessResult import CutenessResult


@dataclass(frozen = True, slots = True)
class CutenessLeaderboardResult:
    cutenessDate: CutenessDate
    specificLookupCutenessResult: CutenessResult | None = None
    entries: FrozenList[CutenessLeaderboardEntry] | None = None
