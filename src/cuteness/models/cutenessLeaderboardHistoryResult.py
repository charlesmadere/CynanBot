from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessLeaderboardResult import CutenessLeaderboardResult


@dataclass(frozen = True, slots = True)
class CutenessLeaderboardHistoryResult:
    history: FrozenList[CutenessLeaderboardResult]
    twitchChannelId: str
