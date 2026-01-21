from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessLeaderboardResult import CutenessLeaderboardResult


@dataclass(frozen = True, slots = True)
class CutenessLeaderboardHistoryResult:
    twitchChannel: str
    twitchChannelId: str
    leaderboards: FrozenList[CutenessLeaderboardResult] | None = None
