from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ...misc import utils as utils


class WrongUserCheckAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        actionId: str,
        answer: str | None,
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise TypeError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
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
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__answer: str | None = answer
        self.__emote: str = emote
        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId
        self.__userName: str = userName

    @property
    def answer(self) -> str | None:
        return self.__answer

    @property
    def emote(self) -> str:
        return self.__emote

    @property
    def gameId(self) -> str:
        return self.__gameId

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.WRONG_USER

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
    def userId(self) -> str:
        return self.__userId

    @property
    def userName(self) -> str:
        return self.__userName
