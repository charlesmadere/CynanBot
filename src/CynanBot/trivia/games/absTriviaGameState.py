import random
import string
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.games.triviaGameType import TriviaGameType
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.specialStatus.specialTriviaStatus import SpecialTriviaStatus


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
        twitchChannel: str
    ):
        assert isinstance(triviaQuestion, AbsTriviaQuestion), f"malformed {triviaQuestion=}"
        if not utils.isValidInt(basePointsForWinning):
            raise ValueError(f'basePointsForWinning argument is malformed: \"{basePointsForWinning}\"')
        if basePointsForWinning < 1 or basePointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'basePointsForWinning argument is out of bounds: {basePointsForWinning}')
        if not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        if pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        if not utils.isValidInt(secondsToLive):
            raise ValueError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        if secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        assert specialTriviaStatus is None or isinstance(specialTriviaStatus, SpecialTriviaStatus), f"malformed {specialTriviaStatus=}"
        if not utils.isValidStr(actionId):
            raise ValueError(f'actionId argument is malformed: \"{actionId}\"')
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__basePointsForWinning: int = basePointsForWinning
        self.__pointsForWinning: int = pointsForWinning
        self.__secondsToLive: int = secondsToLive
        self.__specialTriviaStatus: Optional[SpecialTriviaStatus] = specialTriviaStatus
        self.__actionId: str = actionId
        self.__emote: str = emote
        self.__twitchChannel: str = twitchChannel

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

    @abstractmethod
    def getTriviaGameType(self) -> TriviaGameType:
        pass

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC
