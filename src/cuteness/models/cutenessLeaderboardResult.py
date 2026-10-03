from dataclasses import dataclass
from datetime import datetime

from frozenlist import FrozenList

from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessResult import CutenessResult


@dataclass(frozen = True, slots = True)
class CutenessLeaderboardResult:
    specificLookupCutenessResult: CutenessResult | None
    cutenessDate: datetime
    entries: FrozenList[CutenessLeaderboardEntry]
    twitchChannelId: str
