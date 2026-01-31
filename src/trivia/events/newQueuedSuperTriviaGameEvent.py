from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class NewQueuedSuperTriviaGameEvent(AbsTriviaEvent):

    def __init__(
        self,
        numberOfGames: int,
        pointsForWinning: int,
        secondsToLive: int,
        shinyMultiplier: int,
        actionId: str,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not utils.isValidInt(numberOfGames):
            raise TypeError(f'numberOfGames argument is malformed: \"{numberOfGames}\"')
        elif numberOfGames < 1 or numberOfGames > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGames argument is out of bounds: {numberOfGames}')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or numberOfGames > utils.getIntMaxSafeSize():
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

        self.__numberOfGames: Final[int] = numberOfGames
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__secondsToLive: Final[int] = secondsToLive
        self.__shinyMultiplier: Final[int] = shinyMultiplier
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    def numberOfGames(self) -> int:
        return self.__numberOfGames

    @property
    def pointsForWinning(self) -> int:
        return self.__pointsForWinning

    @property
    def secondsToLive(self) -> int:
        return self.__secondsToLive

    @property
    def shinyMultiplier(self) -> int:
        return self.__shinyMultiplier

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.NEW_QUEUED_SUPER_GAME

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
