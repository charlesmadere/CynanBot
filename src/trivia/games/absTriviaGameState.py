from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Final

from .triviaGameType import TriviaGameType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ...misc import utils as utils


class AbsTriviaGameState(ABC):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        endTime: datetime,
        basePointsForWinning: int,
        pointsForWinning: int,
        secondsToLive: int,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        emote: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not isinstance(endTime, datetime):
            raise TypeError(f'endTime argument is malformed: \"{endTime}\"')
        elif not utils.isValidInt(basePointsForWinning):
            raise TypeError(f'basePointsForWinning argument is malformed: \"{basePointsForWinning}\"')
        elif basePointsForWinning < 1 or basePointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'basePointsForWinning argument is out of bounds: {basePointsForWinning}')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise TypeError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not utils.isValidStr(actionId):
            raise TypeError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__triviaQuestion: Final[AbsTriviaQuestion] = triviaQuestion
        self.__endTime: Final[datetime] = endTime
        self.__basePointsForWinning: Final[int] = basePointsForWinning
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__secondsToLive: Final[int] = secondsToLive
        self.__specialTriviaStatus: Final[SpecialTriviaStatus | None] = specialTriviaStatus
        self.__actionId: Final[str] = actionId
        self.__emote: Final[str] = emote
        self.__gameId: Final[str] = gameId
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    def actionId(self) -> str:
        return self.__actionId

    @property
    def basePointsForWinning(self) -> int:
        return self.__basePointsForWinning

    @property
    def endTime(self) -> datetime:
        return self.__endTime

    @property
    def emote(self) -> str:
        return self.__emote

    @property
    def gameId(self) -> str:
        return self.__gameId

    def getSpecialTriviaStatus(self) -> SpecialTriviaStatus | None:
        return self.__specialTriviaStatus

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC

    @property
    def pointsForWinning(self) -> int:
        return self.__pointsForWinning

    @property
    def secondsToLive(self) -> int:
        return self.__secondsToLive

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.__actionId,
            'basePointsForWinning': self.__basePointsForWinning,
            'emote': self.__emote,
            'gameId': self.__gameId,
            'pointsForWinning': self.__pointsForWinning,
            'secondsToLive': self.__secondsToLive,
            'specialTriviaStatus': self.__specialTriviaStatus,
            'triviaGameType': self.triviaGameType,
            'triviaQuestion': self.__triviaQuestion,
            'twitchChannel': self.__twitchChannel,
            'twitchChannelId': self.__twitchChannelId,
        }

    @property
    @abstractmethod
    def triviaGameType(self) -> TriviaGameType:
        pass
