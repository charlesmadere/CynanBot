import locale
from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ...misc import utils as utils


class NewSuperTriviaGameEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        pointsForWinning: int,
        secondsToLive: int,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        emote: str,
        eventId: str,
        gameId: str,
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
        elif not utils.isValidInt(secondsToLive):
            raise TypeError(f'secondsToLive argument is malformed: \"{secondsToLive}\"')
        elif secondsToLive < 1 or secondsToLive > utils.getIntMaxSafeSize():
            raise ValueError(f'secondsToLive argument is out of bounds: {secondsToLive}')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise TypeError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__triviaQuestion: Final[AbsTriviaQuestion] = triviaQuestion
        self.__pointsForWinning: Final[int] = pointsForWinning
        self.__secondsToLive: Final[int] = secondsToLive
        self.__specialTriviaStatus: Final[SpecialTriviaStatus | None] = specialTriviaStatus
        self.__emote: Final[str] = emote
        self.__gameId: Final[str] = gameId
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

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
    def secondsToLive(self) -> int:
        return self.__secondsToLive

    @property
    def secondsToLiveStr(self) -> str:
        return locale.format_string("%d", self.__secondsToLive, grouping = True)

    @property
    def specialTriviaStatus(self) -> SpecialTriviaStatus | None:
        return self.__specialTriviaStatus

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.NEW_SUPER_GAME

    @property
    def triviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId
