import locale

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.score.triviaScoreResult import TriviaScoreResult
from CynanBot.trivia.specialStatus.specialTriviaStatus import \
    SpecialTriviaStatus


class CorrectAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        cutenessResult: CutenessResult,
        pointsForWinning: int,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        answer: str,
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
        triviaScoreResult: TriviaScoreResult
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not isinstance(cutenessResult, CutenessResult):
            raise TypeError(f'cutenessResult argument is malformed: \"{cutenessResult}\"')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not utils.isValidStr(answer):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(triviaScoreResult, TriviaScoreResult):
            raise TypeError(f'triviaScoreResult argument is malformed: \"{triviaScoreResult}\"')

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__cutenessResult: CutenessResult = cutenessResult
        self.__pointsForWinning: int = pointsForWinning
        self.__specialTriviaStatus: SpecialTriviaStatus | None = specialTriviaStatus
        self.__answer: str = answer
        self.__emote: str = emote
        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
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

    def getSpecialTriviaStatus(self) -> SpecialTriviaStatus | None:
        return self.__specialTriviaStatus

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.CORRECT_ANSWER

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTriviaScoreResult(self) -> TriviaScoreResult:
        return self.__triviaScoreResult

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC
