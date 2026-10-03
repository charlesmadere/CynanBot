from dataclasses import dataclass

from frozenlist import FrozenList

from .preparedCutenessLeaderboardResult import PreparedCutenessLeaderboardResult


@dataclass(frozen = True, slots = True)
class PreparedCutenessLeaderboardHistoryResult:
    history: FrozenList[PreparedCutenessLeaderboardResult]
    twitchChannelId: str
