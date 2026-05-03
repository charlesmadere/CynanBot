from dataclasses import dataclass

from frozenlist import FrozenList

from .preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry


@dataclass(frozen = True, slots = True)
class PreparedCutenessChampionsResult:
    champions: FrozenList[PreparedCutenessLeaderboardEntry]
    twitchChannelId: str
