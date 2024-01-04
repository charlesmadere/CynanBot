from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult


class CutenessLeaderboardHistoryResult():

    def __init__(
        self,
        twitchChannel: str,
        leaderboards: Optional[List[CutenessLeaderboardResult]] = None
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel
        self.__leaderboards: Optional[List[CutenessLeaderboardResult]] = leaderboards

    def getLeaderboards(self) -> Optional[List[CutenessLeaderboardResult]]:
        return self.__leaderboards

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def hasLeaderboards(self) -> bool:
        return utils.hasItems(self.__leaderboards)
