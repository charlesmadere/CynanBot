import locale
from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ..specialStatus.toxicTriviaPunishmentResult import ToxicTriviaPunishmentResult
from ...misc import utils as utils


class OutOfTimeSuperTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        pointsForWinning: int,
        remainingQueueSize: int,
        specialTriviaStatus: SpecialTriviaStatus | None,
        toxicTriviaPunishmentResult: ToxicTriviaPunishmentResult | None,
        actionId: str,
        emote: str,
        eventId: str,
        gameId: str,
        outOfTimeEmote: str | None,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidInt(pointsForWinning):
            raise TypeError(f'pointsForWinning argument is malformed: \"{pointsForWinning}\"')
        elif pointsForWinning < 1 or pointsForWinning > utils.getIntMaxSafeSize():
            raise ValueError(f'pointsForWinning argument is out of bounds: {pointsForWinning}')
        elif not utils.isValidInt(remainingQueueSize):
            raise TypeError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')
        elif remainingQueueSize < 0 or remainingQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'remainingQueueSize argument is out of bounds: {remainingQueueSize}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif toxicTriviaPunishmentResult is not None and not isinstance(toxicTriviaPunishmentResult, ToxicTriviaPunishmentResult):
            raise TypeError(f'toxicTriviaPunishmentResult argument is malformed: \"{toxicTriviaPunishmentResult}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif outOfTimeEmote is not None and not isinstance(outOfTimeEmote, str):
            raise TypeError(f'outOfTimeEmote argument is malformed: \"{outOfTimeEmote}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__triviaQuestion: Final[AbsTriviaQuestion] = triviaQuestion
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__remainingQueueSize: Final[int] = remainingQueueSize
        self.__specialTriviaStatus: Final[SpecialTriviaStatus | None] = specialTriviaStatus
        self.__toxicTriviaPunishmentResult: Final[ToxicTriviaPunishmentResult | None] = toxicTriviaPunishmentResult
        self.__emote: Final[str] = emote
        self.__gameId: Final[str] = gameId
        self.__outOfTimeEmote: Final[str | None] = outOfTimeEmote
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    def emote(self) -> str:
        return self.__emote

    @property
    def gameId(self) -> str:
        return self.__gameId

    @property
    def pointsForWinning(self) -> int:
        return self.__pointsForWinning

    @property
    def pointsForWinningStr(self) -> str:
        return locale.format_string("%d", self.__pointsForWinning, grouping = True)

    @property
    def outOfTimeEmote(self) -> str | None:
        return self.__outOfTimeEmote

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
        return TriviaEventType.SUPER_GAME_OUT_OF_TIME

    @property
    def triviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
