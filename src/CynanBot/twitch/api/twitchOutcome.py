from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from CynanBot.twitch.api.twitchOutcomePredictor import TwitchOutcomePredictor


class TwitchOutcome():

    def __init__(
        self,
        channelPoints: int,
        users: int,
        outcomeId: str,
        title: str,
        color: TwitchOutcomeColor,
        topPredictors: Optional[List[TwitchOutcomePredictor]] = None
    ):
        if not utils.isValidInt(channelPoints):
            raise TypeError(f'channelPoints argument is malformed: \"{channelPoints}\"')
        elif channelPoints < 0 or channelPoints > utils.getLongMaxSafeSize():
            raise ValueError(f'channelPoints argument is out of bounds: {channelPoints}')
        elif not utils.isValidInt(users):
            raise TypeError(f'users argument is malformed: \"{users}\"')
        elif users < 0 or users > utils.getIntMaxSafeSize():
            raise ValueError(f'users argument is out of bounds: {users}')
        elif not utils.isValidStr(outcomeId):
            raise TypeError(f'outcomeId argument is malformed: \"{outcomeId}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(color, TwitchOutcomeColor):
            raise TypeError(f'color argument is malformed: \"{color}\"')
        elif topPredictors is not None and not isinstance(topPredictors, List):
            raise TypeError(f'topPredictors argument is malformed: \"{topPredictors}\"')

        self.__channelPoints: int = channelPoints
        self.__users: int = users
        self.__outcomeId: str = outcomeId
        self.__title: str = title
        self.__color: TwitchOutcomeColor = color
        self.__topPredictors: Optional[List[TwitchOutcomePredictor]] = topPredictors

    def getChannelPoints(self) -> int:
        return self.__channelPoints

    def getColor(self) -> TwitchOutcomeColor:
        return self.__color

    def getOutcomeId(self) -> str:
        return self.__outcomeId

    def getTitle(self) -> str:
        return self.__title

    def getTopPredictors(self) -> Optional[List[TwitchOutcomePredictor]]:
        return self.__topPredictors

    def getUsers(self) -> int:
        return self.__users

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'channelPoints': self.__channelPoints,
            'color': self.__color,
            'outcomeId': self.__outcomeId,
            'title': self.__title,
            'topPredictors': self.__topPredictors,
            'users': self.__users
        }
