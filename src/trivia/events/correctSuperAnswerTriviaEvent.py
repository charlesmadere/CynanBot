import locale
from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..score.triviaScoreResult import TriviaScoreResult
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ..specialStatus.toxicTriviaPunishmentResult import ToxicTriviaPunishmentResult
from ...cuteness.incrementedCutenessResult import IncrementedCutenessResult
from ...misc import utils as utils


class CorrectSuperAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        cutenessResult: IncrementedCutenessResult,
        pointsForWinning: int,
        remainingQueueSize: int,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        answer: str,
        celebratoryTwitchEmote: str | None,
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str,
        userId: str,
        userName: str,
        triviaScoreResult: TriviaScoreResult,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not isinstance(cutenessResult, IncrementedCutenessResult):
            raise TypeError(f'cutenessResult argument is malformed: \"{cutenessResult}\"')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(remainingQueueSize):
            raise TypeError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')
        elif remainingQueueSize < 0 or remainingQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'remainingQueueSize argument is out of bounds: {remainingQueueSize}')
        elif toxicTriviaPunishmentResult is not None and not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise TypeError(f'toxicTriviaPunishmentResult argument is out of bounds: {toxicTriviaPunishmentResult}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not utils.isValidStr(answer):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')
        elif celebratoryTwitchEmote is not None and not isinstance(celebratoryTwitchEmote, str):
            raise TypeError(f'celebratoryTwitchEmote argument is malformed: \"{celebratoryTwitchEmote}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(twitchChatMessageId):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(triviaScoreResult, TriviaScoreResult):
            raise TypeError(f'triviaScoreResult argument is malformed: \"{triviaScoreResult}\"')

        self.__triviaQuestion: Final[AbsTriviaQuestion] = triviaQuestion
        self.__cutenessResult: Final[IncrementedCutenessResult] = cutenessResult
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__remainingQueueSize: Final[int] = remainingQueueSize
        self.__toxicTriviaPunishmentResult: Final[ToxicTriviaPunishmentResult | None] = toxicTriviaPunishmentResult
        self.__specialTriviaStatus: Final[SpecialTriviaStatus | None] = specialTriviaStatus
        self.__answer: Final[str] = answer
        self.__celebratoryTwitchEmote: Final[str | None] = celebratoryTwitchEmote
        self.__emote: Final[str] = emote
        self.__gameId: Final[str] = gameId
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__twitchChatMessageId: Final[str] = twitchChatMessageId
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName
        self.__triviaScoreResult: Final[TriviaScoreResult] = triviaScoreResult

    @property
    def answer(self) -> str:
        return self.__answer

    @property
    def celebratoryTwitchEmote(self) -> str | None:
        return self.__celebratoryTwitchEmote

    @property
    def cutenessResult(self) -> IncrementedCutenessResult:
        return self.__cutenessResult

    @property
    def emote(self) -> str:
        return self.__emote

    @property
    def gameId(self) -> str:
        return self.__gameId

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC

    @property
    def pointsForWinning(self) -> int:
        return self.__pointsForWinning

    @property
    def pointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__pointsForWinning, grouping = True)

    @property
    def remainingQueueSize(self) -> int:
        return self.__remainingQueueSize

    @property
    def remainingQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__remainingQueueSize, grouping = True)

    @property
    def specialTriviaStatus(self) -> SpecialTriviaStatus | None:
        return self.__specialTriviaStatus

    @property
    def toxicTriviaPunishmentResult(self) -> ToxicTriviaPunishmentResult | None:
        return self.__toxicTriviaPunishmentResult

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_CORRECT_ANSWER

    @property
    def triviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    @property
    def triviaScoreResult(self) -> TriviaScoreResult:
        return self.__triviaScoreResult

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId

    @property
    def twitchChatMessageId(self) -> str:
        return self.__twitchChatMessageId

    @property
    def userId(self) -> str:
        return self.__userId

    @property
    def userName(self) -> str:
        return self.__userName
