from collections import defaultdict
from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaGameState import AbsTriviaGameState
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.specialTriviaStatus import SpecialTriviaStatus
from CynanBot.trivia.triviaGameType import TriviaGameType


class SuperTriviaGameState(AbsTriviaGameState):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        basePointsForWinning: int,
        perUserAttempts: int,
        pointsForWinning: int,
        regularTriviaPointsForWinning: int,
        secondsToLive: int,
        toxicTriviaPunishmentMultiplier: int,
        specialTriviaStatus: Optional[SpecialTriviaStatus],
        actionId: str,
        emote: str,
        twitchChannel: str
    ):
        super().__init__(
            triviaQuestion = triviaQuestion,
            basePointsForWinning = basePointsForWinning,
            pointsForWinning = pointsForWinning,
            secondsToLive = secondsToLive,
            specialTriviaStatus = specialTriviaStatus,
            actionId = actionId,
            emote = emote,
            twitchChannel = twitchChannel,
            triviaGameType = TriviaGameType.SUPER
        )

        if not utils.isValidInt(perUserAttempts):
            raise ValueError(f'perUserAttempts argument is malformed: \"{perUserAttempts}\"')
        elif perUserAttempts < 1 or perUserAttempts > 3:
            raise ValueError(f'perUserAttempts argument is out of bounds: {perUserAttempts}')
        elif not utils.isValidInt(toxicTriviaPunishmentMultiplier):
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is malformed: \"{toxicTriviaPunishmentMultiplier}\"')
        elif toxicTriviaPunishmentMultiplier < 0 or toxicTriviaPunishmentMultiplier > utils.getIntMaxSafeSize():
            raise ValueError(f'toxicTriviaPunishmentMultiplier argument is out of bounds: {toxicTriviaPunishmentMultiplier}')

        self.__perUserAttempts: int = perUserAttempts
        self.__regularTriviaPointsForWinning: int = regularTriviaPointsForWinning
        self.__toxicTriviaPunishmentMultiplier: int = toxicTriviaPunishmentMultiplier

        self.__answeredUserIds: Dict[str, int] = defaultdict(lambda: 0)

    def getAnsweredUserIds(self) -> Dict[str, int]:
        return dict(self.__answeredUserIds)

    def getPerUserAttempts(self) -> int:
        return self.__perUserAttempts

    def getRegularTriviaPointsForWinning(self) -> int:
        return self.__regularTriviaPointsForWinning

    def getToxicTriviaPunishmentMultiplier(self) -> int:
        return self.__toxicTriviaPunishmentMultiplier

    def incrementAnswerCount(self, userId: str):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        userId = userId.lower()
        self.__answeredUserIds[userId] = self.__answeredUserIds[userId] + 1

    def isEligibleToAnswer(self, userId: str) -> bool:
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        userId = userId.lower()
        return self.__answeredUserIds[userId] < self.__perUserAttempts
