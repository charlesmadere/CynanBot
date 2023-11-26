import random
import string
from abc import ABC
from datetime import datetime, timedelta, timezone
from typing import Optional

import misc.utils as utils
from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.specialTriviaStatus import SpecialTriviaStatus
from trivia.triviaGameType import TriviaGameType


class AbsTriviaGameState(ABC):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        basePointsForWinning: int,
        pointsForWinning: int,
        secondsToLive: int,
        specialTriviaStatus: Optional[SpecialTriviaStatus],
        actionId: str,
        emote: str,
        twitchChannel: str,
        triviaGameType: TriviaGameType
    ):
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(basePointsForWinning):
            raise ValueError(f'basePointsForWinning argument is malformed: \"{basePointsForWinning}\"')
        elif basePointsForWinning < 1 or basePointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'basePointsForWinning argument is out of bounds: {basePointsForWinning}')
        elif not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(secondsToLive):
            raise ValueError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not isinstance(triviaGameType, TriviaGameType):
            raise ValueError(f'triviaGameType argument is malformed: \"{triviaGameType}\"')

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__basePointsForWinning: int = basePointsForWinning
        self.__pointsForWinning: int = pointsForWinning
        self.__secondsToLive: int = secondsToLive
        self.__specialTriviaStatus: Optional[SpecialTriviaStatus] = specialTriviaStatus
        self.__actionId: str = actionId
        self.__emote: str = emote
        self.__twitchChannel: str = twitchChannel
        self.__triviaGameType: TriviaGameType = triviaGameType

        self.__endTime: datetime = datetime.now(timezone.utc) + timedelta(seconds = secondsToLive)
        self.__gameId: str = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))

    def getActionId(self) -> str:
        return self.__actionId

    def getBasePointsForWinning(self) -> int:
        return self.__basePointsForWinning

    def getEmote(self) -> str:
        return self.__emote

    def getEndTime(self) -> datetime:
        return self.__endTime

    def getGameId(self) -> str:
        return self.__gameId

    def getPointsForWinning(self) -> int:
        return self.__pointsForWinning

    def getSecondsToLive(self) -> int:
        return self.__secondsToLive

    def getSpecialTriviaStatus(self) -> Optional[SpecialTriviaStatus]:
        return self.__specialTriviaStatus

    def getTriviaGameType(self) -> TriviaGameType:
        return self.__triviaGameType

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC
