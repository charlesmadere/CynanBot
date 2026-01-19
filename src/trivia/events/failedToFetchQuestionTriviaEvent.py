from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class FailedToFetchQuestionTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
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

        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__userId: Final[str] = userId
        self.__userName: Final[str] = userName

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION

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
