from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry


class CutenessChampionsResult():

    def __init__(
        self,
        twitchChannel: str,
        champions: Optional[List[CutenessLeaderboardEntry]] = None
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel
        self.__champions: Optional[List[CutenessLeaderboardEntry]] = champions

    def getChampions(self) -> Optional[List[CutenessLeaderboardEntry]]:
        return self.__champions

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def hasChampions(self) -> bool:
        return utils.hasItems(self.__champions)
