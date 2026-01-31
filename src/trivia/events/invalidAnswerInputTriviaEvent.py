from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..specialStatus.specialTriviaStatus import SpecialTriviaStatus
from ...misc import utils as utils


class InvalidAnswerInputTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        specialTriviaStatus: SpecialTriviaStatus | None,
        actionId: str,
        answer: str | None,
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str,
        userId: str,
        userName: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise TypeError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif answer is not None and not isinstance(answer, str):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')
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

        self.__triviaQuestion: Final[AbsTriviaQuestion] = triviaQuestion
        self.__specialTriviaStatus: Final[SpecialTriviaStatus | None] = specialTriviaStatus
        self.__answer: Final[str | None] = answer
        self.__emote: Final[str] = emote
        self.__gameId: Final[str] = gameId
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__twitchChatMessageId: Final[str] = twitchChatMessageId
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName

    @property
    def answer(self) -> str | None:
        return self.__answer

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
    def specialTriviaStatus(self) -> SpecialTriviaStatus | None:
        return self.__specialTriviaStatus

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.INVALID_ANSWER_INPUT

    @property
    def triviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

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
