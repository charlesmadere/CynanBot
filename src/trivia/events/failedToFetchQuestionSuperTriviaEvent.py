from typing import Final

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class FailedToFetchQuestionSuperTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION
