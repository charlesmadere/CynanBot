import locale

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions


class StartNewSuperTriviaGameAction(AbsTriviaAction):

    def __init__(
        self,
        isQueueActionConsumed: bool,
        isShinyTriviaEnabled: bool,
        isToxicTriviaEnabled: bool,
        numberOfGames: int,
        perUserAttempts: int,
        pointsForWinning: int,
        regularTriviaPointsForWinning: int,
        secondsToLive: int,
        shinyMultiplier: int,
        toxicMultiplier: int,
        toxicTriviaPunishmentMultiplier: int,
        actionId: str,
        twitchChannel: str,
        triviaFetchOptions: TriviaFetchOptions
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidBool(isQueueActionConsumed):
            raise TypeError(f'isQueueActionConsumed argument is malformed: \"{isQueueActionConsumed}\"')
        if not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        if not utils.isValidBool(isToxicTriviaEnabled):
            raise TypeError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        if not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        if numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')
        if not utils.isValidInt(perUserAttempts):
            raise TypeError(f'perUserAttempts argument is malformed: \"{perUserAttempts}\"')
        if perUserAttempts < 1 or perUserAttempts > 5:
            raise ValueError(f'perUserAttempts argument is out of bounds: {perUserAttempts}')
        if not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        if pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        if not utils.isValidInt(regularTriviaPointsForWinning):
            raise TypeError(f'regularTriviaPointsForWinning argument is malformed: \"{regularTriviaPointsForWinning}\"')
        if regularTriviaPointsForWinning < 1 or regularTriviaPointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'regularTriviaPointsForWinning argument is out of bounds: {regularTriviaPointsForWinning}')
        if not utils.isValidInt(secondsToLive):
            raise TypeError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        if secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        if not utils.isValidInt(shinyMultiplier):
            raise TypeError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        if shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        if not utils.isValidInt(toxicMultiplier):
            raise TypeError(f'toxicMultiplier argument is malformed: \"{toxicMultiplier}\"')
        if toxicMultiplier < 1 or toxicMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicMultiplier argument is out of bounds: {toxicMultiplier}')
        if not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            raise TypeError(f'toxicTriviaPunishmentMultiplier argument is malformed: \"{toxicTriviaPunishmentMultiplier}\"')
        if toxicTriviaPunishmentMultiplier < 0 or toxicTriviaPunishmentMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is out of bounds: {toxicTriviaPunishmentMultiplier}')
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        assert isinstance(triviaFetchOptions, TriviaFetchOptions), f"malformed {triviaFetchOptions=}"

        self.__isQueueActionConsumed: bool = isQueueActionConsumed
        self.__isShinyTriviaEnabled: bool = isShinyTriviaEnabled
        self.__isToxicTriviaEnabled: bool = isToxicTriviaEnabled
        self.__numberOfGames: int = numberOfGames
        self.__perUserAttempts: int = perUserAttempts
        self.__pointsForWinning: int = pointsForWinning
        self.__regularTriviaPointsForWinning: int = regularTriviaPointsForWinning
        self.__secondsToLive: int = secondsToLive
        self.__shinyMultiplier: int = shinyMultiplier
        self.__toxicMultiplier: int = toxicMultiplier
        self.__toxicTriviaPunishmentMultiplier: int = toxicTriviaPunishmentMultiplier
        self.__twitchChannel: str = twitchChannel
        self.__triviaFetchOptions: TriviaFetchOptions = triviaFetchOptions

        self.__creationTime = SimpleDateTime()

    def consumeQueueAction(self):
        self.__isQueueActionConsumed = True

    def getCreationTime(self) -> SimpleDateTime:
        return self.__creationTime

    def getNumberOfGames(self) -> int:
        return self.__numberOfGames

    def getNumberOfGamesStr(self) -> str:
        return locale.format_string("%d", self.__numberOfGames, grouping = True)

    def getPerUserAttempts(self) -> int:
        return self.__perUserAttempts

    def getPointsForWinning(self) -> int:
        return self.__pointsForWinning

    def getPointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__pointsForWinning, grouping = True)

    def getRegularTriviaPointsForWinning(self) -> int:
        return self.__regularTriviaPointsForWinning

    def getRegularTriviaPointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__regularTriviaPointsForWinning, grouping = True)

    def getSecondsToLive(self) -> int:
        return self.__secondsToLive

    def getSecondsToLiveStr(self) -> str:
        return locale.format_string("%d", self.__secondsToLive, grouping = True)

    def getShinyMultiplier(self) -> int:
        return self.__shinyMultiplier

    def getShinyMultiplierStr(self) -> str:
        return locale.format_string("%d", self.__shinyMultiplier, grouping = True)

    def getToxicMultiplier(self) -> int:
        return self.__toxicMultiplier

    def getToxicMultiplierStr(self) -> str:
        return locale.format_string("%d", self.__toxicMultiplier, grouping = True)

    def getToxicTriviaPunishmentMultiplier(self) -> int:
        return self.__toxicTriviaPunishmentMultiplier

    def getToxicTriviaPunishmentMultiplierStr(self) -> str:
        return locale.format_string("%d", self.__toxicTriviaPunishmentMultiplier, grouping = True)

    def getTriviaActionType(self) -> TriviaActionType:
        return TriviaActionType.START_NEW_SUPER_GAME

    def getTriviaFetchOptions(self) -> TriviaFetchOptions:
        return self.__triviaFetchOptions

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def isQueueActionConsumed(self) -> bool:
        return self.__isQueueActionConsumed

    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled

    def isToxicTriviaEnabled(self) -> bool:
        return self.__isToxicTriviaEnabled
