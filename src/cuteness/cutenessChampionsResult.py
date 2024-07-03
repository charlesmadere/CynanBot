from dataclasses import dataclass

from .cutenessLeaderboardEntry import CutenessLeaderboardEntry


@dataclass(frozen = True)
class CutenessChampionsResult():
    twitchChannel: str
    twitchChannelId: str
    champions: list[CutenessLeaderboardEntry] | None = None
