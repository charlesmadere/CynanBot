import locale
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.specialStatus.specialTriviaStatus import SpecialTriviaStatus
from CynanBot.trivia.specialStatus.toxicTriviaPunishmentResult import \
    ToxicTriviaPunishmentResult
from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult


class CorrectSuperAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        cutenessResult: CutenessResult,
        pointsForWinning: int,
        remainingQueueSize: int,
        toxicTriviaPunishmentResult: Optional[ToxicTriviaPunishmentResult],
        specialTriviaStatus: Optional[SpecialTriviaStatus],
        actionId: str,
        answer: str,
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        userId: str,
        userName: str,
        triviaScoreResult: TriviaScoreResult
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        assert isinstance(triviaQuestion, AbsTriviaQuestion), f"malformed {triviaQuestion=}"
        assert isinstance(cutenessResult, CutenessResult), f"malformed {cutenessResult=}"
        if not utils.isValidInt(pointsForWinning):
            raise ValueError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        if pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        if not utils.isValidInt(remainingQueueSize):
            raise ValueError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')
        if remainingQueueSize < 0 or remainingQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'remainingQueueSize argument is out of bounds: {remainingQueueSize}')
        if toxicTriviaPunishmentResult is not None and not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise ValueError(f'toxicTriviaPunishmentResult argument is out of bounds: {toxicTriviaPunishmentResult}')
        assert specialTriviaStatus is None or isinstance(specialTriviaStatus, SpecialTriviaStatus), f"malformed {specialTriviaStatus=}"
        if not utils.isValidStr(answer):
            raise ValueError(f'answer argument is malformed: \"{answer}\"')
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        if not utils.isValidStr(gameId):
            raise ValueError(f'gameId argument is malformed: \"{gameId}\"')
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert isinstance(triviaScoreResult, TriviaScoreResult), f"malformed {triviaScoreResult=}"

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__cutenessResult: CutenessResult = cutenessResult
        self.__pointsForWinning: int = pointsForWinning
        self.__remainingQueueSize: int = remainingQueueSize
        self.__toxicTriviaPunishmentResult: Optional[ToxicTriviaPunishmentResult] = toxicTriviaPunishmentResult
        self.__specialTriviaStatus: Optional[SpecialTriviaStatus] = specialTriviaStatus
        self.__answer: str = answer
        self.__emote: str = emote
        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName
        self.__triviaScoreResult: TriviaScoreResult = triviaScoreResult

    def getAnswer(self) -> str:
        return self.__answer

    def getCutenessResult(self) -> CutenessResult:
        return self.__cutenessResult

    def getEmote(self) -> str:
        return self.__emote

    def getGameId(self) -> str:
        return self.__gameId

    def getPointsForWinning(self) -> int:
        return self.__pointsForWinning

    def getPointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__pointsForWinning, grouping = True)

    def getRemainingQueueSize(self) -> int:
        return self.__remainingQueueSize

    def getRemainingQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__remainingQueueSize, grouping = True)

    def getSpecialTriviaStatus(self) -> Optional[SpecialTriviaStatus]:
        return self.__specialTriviaStatus

    def getToxicTriviaPunishmentResult(self) -> Optional[ToxicTriviaPunishmentResult]:
        return self.__toxicTriviaPunishmentResult

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_CORRECT_ANSWER

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTriviaScoreResult(self) -> TriviaScoreResult:
        return self.__triviaScoreResult

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def hasToxicTriviaPunishmentResult(self) -> bool:
        return self.__toxicTriviaPunishmentResult is not None

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC
