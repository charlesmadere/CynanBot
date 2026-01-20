from typing import Final

from .absTriviaAction import AbsTriviaAction
from .triviaActionType import TriviaActionType
from ..triviaFetchOptions import TriviaFetchOptions
from ...misc import utils as utils
from ...misc.simpleDateTime import SimpleDateTime


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
        twitchChannelId: str,
        triviaFetchOptions: TriviaFetchOptions,
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidBool(isQueueActionConsumed):
            raise TypeError(f'isQueueActionConsumed argument is malformed: \"{isQueueActionConsumed}\"')
        elif not utils.isValidBool(isShinyTriviaEnabled):
            raise TypeError(f'isShinyTriviaEnabled argument is malformed: \"{isShinyTriviaEnabled}\"')
        elif not utils.isValidBool(isToxicTriviaEnabled):
            raise TypeError(f'isToxicTriviaEnabled argument is malformed: \"{isToxicTriviaEnabled}\"')
        elif not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')
        elif not utils.isValidInt(perUserAttempts):
            raise TypeError(f'perUserAttempts argument is malformed: \"{perUserAttempts}\"')
        elif perUserAttempts < 1 or perUserAttempts > 5:
            raise ValueError(f'perUserAttempts argument is out of bounds: {perUserAttempts}')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(regularTriviaPointsForWinning):
            raise TypeError(f'regularTriviaPointsForWinning argument is malformed: \"{regularTriviaPointsForWinning}\"')
        elif regularTriviaPointsForWinning < 1 or regularTriviaPointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'regularTriviaPointsForWinning argument is out of bounds: {regularTriviaPointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise TypeError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif not utils.isValidInt(shinyMultiplier):
            raise TypeError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        elif shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        elif not utils.isValidInt(toxicMultiplier):
            raise TypeError(f'toxicMultiplier argument is malformed: \"{toxicMultiplier}\"')
        elif toxicMultiplier < 1 or toxicMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicMultiplier argument is out of bounds: {toxicMultiplier}')
        elif not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            raise TypeError(f'toxicTriviaPunishmentMultiplier argument is malformed: \"{toxicTriviaPunishmentMultiplier}\"')
        elif toxicTriviaPunishmentMultiplier < 0 or toxicTriviaPunishmentMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is out of bounds: {toxicTriviaPunishmentMultiplier}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        self.__isQueueActionConsumed: bool = isQueueActionConsumed
        self.__isShinyTriviaEnabled: Final[bool] = isShinyTriviaEnabled
        self.__isToxicTriviaEnabled: Final[bool] = isToxicTriviaEnabled
        self.__numberOfGames: Final[int] = numberOfGames
        self.__perUserAttempts: Final[int] = perUserAttempts
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__regularTriviaPointsForWinning: Final[int] = regularTriviaPointsForWinning
        self.__secondsToLive: Final[int] = secondsToLive
        self.__shinyMultiplier: Final[int] = shinyMultiplier
        self.__toxicMultiplier: Final[int] = toxicMultiplier
        self.__toxicTriviaPunishmentMultiplier: Final[int] = toxicTriviaPunishmentMultiplier
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__triviaFetchOptions: Final[TriviaFetchOptions] = triviaFetchOptions

        self.__creationTime: Final[SimpleDateTime] = SimpleDateTime()

    def consumeQueueAction(self):
        self.__isQueueActionConsumed = True

    @property
    def creationTime(self) -> SimpleDateTime:
        return self.__creationTime

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    @property
    def isQueueActionConsumed(self) -> bool:
        return self.__isQueueActionConsumed

    @property
    def isShinyTriviaEnabled(self) -> bool:
        return self.__isShinyTriviaEnabled

    @property
    def isToxicTriviaEnabled(self) -> bool:
        return self.__isToxicTriviaEnabled

    @property
    def numberOfGames(self) -> int:
        return self.__numberOfGames

    @property
    def perUserAttempts(self) -> int:
        return self.__perUserAttempts

    @property
    def pointsForWinning(self) -> int:
        return self.__pointsForWinning

    @property
    def regularTriviaPointsForWinning(self) -> int:
        return self.__regularTriviaPointsForWinning

    @property
    def secondsToLive(self) -> int:
        return self.__secondsToLive

    @property
    def shinyMultiplier(self) -> int:
        return self.__shinyMultiplier

    @property
    def toxicMultiplier(self) -> int:
        return self.__toxicMultiplier

    @property
    def toxicTriviaPunishmentMultiplier(self) -> int:
        return self.__toxicTriviaPunishmentMultiplier

    @property
    def triviaActionType(self) -> TriviaActionType:
        return TriviaActionType.START_NEW_SUPER_GAME

    @property
    def triviaFetchOptions(self) -> TriviaFetchOptions:
        return self.__triviaFetchOptions
