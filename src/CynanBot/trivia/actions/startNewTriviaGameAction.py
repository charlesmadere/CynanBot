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
        userId: str,
        userName: str,
        triviaFetchOptions: TriviaFetchOptions
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidBool(isShinyTriviaEnabled):
            raise ValueError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        if not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        if pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        if not utils.isValidInt(secondsToLive):
            raise ValueError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        if secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        if not utils.isValidInt(shinyMultiplier):
            raise ValueError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        if shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert isinstance(triviaFetchOptions, TriviaFetchOptions), f"malformed {triviaFetchOptions=}"

        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__pointsForWinning: int = pointsForWinning
        self.__shinyMultiplier: int = shinyMultiplier
        self.__secondsToLive: int = secondsToLive
        self.__twitchChannel: str = twitchChannel
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

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled
