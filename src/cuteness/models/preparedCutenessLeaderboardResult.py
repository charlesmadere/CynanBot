from dataclasses import dataclass
from datetime import datetime

from frozenlist import FrozenList

from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from .preparedCutenessResult import PreparedCutenessResult


@dataclass(frozen = True, slots = True)
class PreparedCutenessLeaderboardResult:
    cutenessLeaderboardResult: CutenessLeaderboardResult
    entries: FrozenList[PreparedCutenessLeaderboardEntry]
    specificLookupCutenessResult: PreparedCutenessResult | None

    @property
    def cutenessDate(self) -> datetime:
        return self.cutenessLeaderboardResult.cutenessDate

    @property
    def twitchChannelId(self) -> str:
        return self.cutenessLeaderboardResult.twitchChannelId
