import locale

import misc.utils as utils
from simpleDateTime import SimpleDateTime
from trivia.absTriviaAction import AbsTriviaAction
from trivia.triviaActionType import TriviaActionType
from trivia.triviaFetchOptions import TriviaFetchOptions


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
        twitchChannel: str,
        triviaFetchOptions: TriviaFetchOptions
    ):
        super().__init__(triviaActionType = TriviaActionType.START_NEW_SUPER_GAME)

        if not utils.isValidBool(isQueueActionConsumed):
            raise ValueError(f'isQueueActionConsumed argument is malformed: \"{isQueueActionConsumed}\"')
        elif not utils.isValidBool(isShinyTriviaEnabled):
            raise ValueError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidBool(isToxicTriviaEnabled):
            raise ValueError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        elif not utils.isValidInt(numberOfGames):
            raise ValueError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')
        elif not utils.isValidInt(perUserAttempts):
            raise ValueError(f'perUserAttempts argument is malformed: \"{perUserAttempts}\"')
        elif perUserAttempts < 1 or perUserAttempts > 5:
            raise ValueError(f'perUserAttempts argument is out of bounds: {perUserAttempts}')
        elif not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(regularTriviaPointsForWinning):
            raise ValueError(f'regularTriviaPointsForWinning argument is malformed: \"{regularTriviaPointsForWinning}\"')
        elif regularTriviaPointsForWinning < 1 or regularTriviaPointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'regularTriviaPointsForWinning argument is out of bounds: {regularTriviaPointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise ValueError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif not utils.isValidInt(shinyMultiplier):
            raise ValueError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        elif shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        elif not utils.isValidInt(toxicMultiplier):
            raise ValueError(f'toxicMultiplier argument is malformed: \"{toxicMultiplier}\"')
        elif toxicMultiplier < 1 or toxicMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicMultiplier argument is out of bounds: {toxicMultiplier}')
        elif not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is malformed: \"{toxicTriviaPunishmentMultiplier}\"')
        elif toxicTriviaPunishmentMultiplier < 0 or toxicTriviaPunishmentMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is out of bounds: {toxicTriviaPunishmentMultiplier}')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

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

    def getToxicTriviaPunishmentMultiplierStr(self) -> int:
        return locale.format_string("%d", self.__toxicTriviaPunishmentMultiplier, grouping = True)

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
