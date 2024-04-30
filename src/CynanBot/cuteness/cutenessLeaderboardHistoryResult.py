from dataclasses import dataclass

from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult


@dataclass(frozen = True)
class CutenessLeaderboardHistoryResult():
    twitchChannel: str
    twitchChannelId: str
    leaderboards: list[CutenessLeaderboardResult] | None = None
