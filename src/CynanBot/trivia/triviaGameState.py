from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaGameState import AbsTriviaGameState
from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.specialTriviaStatus import SpecialTriviaStatus
from CynanBot.trivia.triviaGameType import TriviaGameType


class TriviaGameState(AbsTriviaGameState):

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
        userId: str,
        userName: str
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
            triviaGameType = TriviaGameType.NORMAL
        )

        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userId: str = userId
        self.__userName: str = userName

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
