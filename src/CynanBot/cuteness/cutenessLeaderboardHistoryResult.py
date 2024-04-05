import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult


class CutenessLeaderboardHistoryResult():

    def __init__(
        self,
        twitchChannel: str,
        leaderboards: list[CutenessLeaderboardResult] | None = None
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel
        self.__leaderboards: list[CutenessLeaderboardResult] | None = leaderboards

    def getLeaderboards(self) -> list[CutenessLeaderboardResult] | None:
        return self.__leaderboards

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
