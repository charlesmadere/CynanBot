import locale

import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions


class StartNewTriviaGameAction(AbsTriviaAction):

    def __init__(
        self,
        isShinyTriviaEnabled: bool,
        pointsForWinning: int,
        secondsToLive: int,
        shinyMultiplier: int,
        actionId: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
        triviaFetchOptions: TriviaFetchOptions
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise TypeError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif not utils.isValidInt(shinyMultiplier):
            raise TypeError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        elif shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__pointsForWinning: int = pointsForWinning
        self.__shinyMultiplier: int = shinyMultiplier
        self.__secondsToLive: int = secondsToLive
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId
        self.__userName: str = userName
        self.__triviaFetchOptions: TriviaFetchOptions = triviaFetchOptions

    def getPointsForWinning(self) -> int:
        return self.__pointsForWinning

    def getPointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__pointsForWinning, grouping = True)

    def getSecondsToLive(self) -> int:
        return self.__secondsToLive

    def getSecondsToLiveStr(self) -> str:
        return locale.format_string("%d", self.__secondsToLive, grouping = True)

    def getShinyMultiplier(self) -> int:
        return self.__shinyMultiplier

    def getShinyMultiplierStr(self) -> str:
        return locale.format_string("%d", self.__shinyMultiplier, grouping = True)

    def getTriviaActionType(self) -> TriviaActionType:
        return TriviaActionType.START_NEW_GAME

    def getTriviaFetchOptions(self) -> TriviaFetchOptions:
        return self.__triviaFetchOptions

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled
