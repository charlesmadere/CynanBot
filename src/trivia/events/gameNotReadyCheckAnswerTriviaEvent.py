from typing import Any, Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class GameNotReadyCheckAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        answer: str | None,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if answer is not None and not isinstance(answer, str):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__answer: Final[str | None] = answer
        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName

    @property
    def answer(self) -> str | None:
        return self.__answer

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionId': self.actionId,
            'answer': self.__answer,
            'eventId': self.eventId,
            'twitchChannel': self.__twitchChannel,
            'twitchChannelId': self.__twitchChannelId,
            'triviaEventType': self.triviaEventType,
            'userId': self.__userId,
            'userName': self.__userName,
        }

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.GAME_NOT_READY

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
