import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.triviaEventType import TriviaEventType


class NewQueuedSuperTriviaGameEvent(AbsTriviaEvent):

    def __init__(
        self,
        numberOfGames: int,
        pointsForWinning: int,
        secondsToLive: int,
        shinyMultiplier: int,
        actionId: str,
        eventId: str,
        twitchChannel: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not utils.isValidInt(numberOfGames):
            raise ValueError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')
        elif not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise ValueError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif not utils.isValidInt(shinyMultiplier):
            raise ValueError(f'shinyMultiplier argument is malformed: \"{shinyMultiplier}\"')
        elif shinyMultiplier < 1 or shinyMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'shinyMultiplier argument is out of bounds: {shinyMultiplier}')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__numberOfGames: int = numberOfGames
        self.__pointsForWinning: int = pointsForWinning
        self.__secondsToLive: int = secondsToLive
        self.__shinyMultiplier: int = shinyMultiplier
        self.__twitchChannel: str = twitchChannel

    def getNumberOfGames(self) -> int:
        return self.__numberOfGames

    def getPointsForWinning(self) -> int:
        return self.__pointsForWinning

    def getSecondsToLive(self) -> int:
        return self.__secondsToLive

    def getShinyMultiplier(self) -> int:
        return self.__shinyMultiplier

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.NEW_QUEUED_SUPER_GAME

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
