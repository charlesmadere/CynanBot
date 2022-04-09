from typing import List

import CynanBotCommon.utils as utils

from cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry


class CutenessChampionsResult():

    def __init__(
        self,
        twitchChannel: str,
        champions: List[CutenessLeaderboardEntry] = None
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel
        self.__champions: List[CutenessLeaderboardEntry] = champions

    def getChampions(self) -> List[CutenessLeaderboardEntry]:
        return self.__champions

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def hasChampions(self) -> bool:
        return utils.hasItems(self.__champions)
