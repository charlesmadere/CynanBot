import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry


class CutenessChampionsResult():

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        champions: list[CutenessLeaderboardEntry] | None = None
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif champions is not None and not isinstance(champions, list):
            raise TypeError(f'champions argument is malformed: \"{champions}\"')

        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__champions: list[CutenessLeaderboardEntry] | None = champions

    def getChampions(self) -> list[CutenessLeaderboardEntry] | None:
        return self.__champions

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId
