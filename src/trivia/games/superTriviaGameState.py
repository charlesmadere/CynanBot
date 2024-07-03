from collections import defaultdict
from datetime import datetime

from .absTriviaGameState import AbsTriviaGameState
from .triviaGameType import TriviaGameType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ...misc import utils as utils


class SuperTriviaGameState(AbsTriviaGameState):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        endTime: datetime,
        basePointsForWinning: int,
        perUserAttempts: int,
        pointsForWinning: int,
        regularTriviaPointsForWinning: int,
        secondsToLive: int,
        toxicTriviaPunishmentMultiplier: int,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        emote: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            triviaQuestion = triviaQuestion,
            endTime = endTime,
            basePointsForWinning = basePointsForWinning,
            pointsForWinning = pointsForWinning,
            secondsToLive = secondsToLive,
            specialTriviaStatus = specialTriviaStatus,
            actionId = actionId,
            emote = emote,
            gameId = gameId,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidInt(perUserAttempts):
            raise TypeError(f'perUserAttempts argument is malformed: \"{perUserAttempts}\"')
        elif perUserAttempts < 1 or perUserAttempts > 5:
            raise ValueError(f'perUserAttempts argument is out of bounds: {perUserAttempts}')
        elif not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            raise TypeError(f'toxicTriviaPunishmentMultiplier argument is malformed: \"{toxicTriviaPunishmentMultiplier}\"')
        elif toxicTriviaPunishmentMultiplier < 0 or toxicTriviaPunishmentMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is out of bounds: {toxicTriviaPunishmentMultiplier}')

        self.__perUserAttempts: int = perUserAttempts
        self.__regularTriviaPointsForWinning: int = regularTriviaPointsForWinning
        self.__toxicTriviaPunishmentMultiplier: int = toxicTriviaPunishmentMultiplier

        self.__answeredUserIds: dict[str, int] = defaultdict(lambda: 0)

    def getAnsweredUserIds(self) -> dict[str, int]:
        return dict(self.__answeredUserIds)

    def getPerUserAttempts(self) -> int:
        return self.__perUserAttempts

    def getRegularTriviaPointsForWinning(self) -> int:
        return self.__regularTriviaPointsForWinning

    def getToxicTriviaPunishmentMultiplier(self) -> int:
        return self.__toxicTriviaPunishmentMultiplier

    def getTriviaGameType(self) -> TriviaGameType:
        return TriviaGameType.SUPER

    def incrementAnswerCount(self, userId: str):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__answeredUserIds[userId] = self.__answeredUserIds[userId] + 1

    def isEligibleToAnswer(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        return self.__answeredUserIds[userId] < self.__perUserAttempts
