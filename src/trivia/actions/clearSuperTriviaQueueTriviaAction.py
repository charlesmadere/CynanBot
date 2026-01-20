from typing import Final

from .absTriviaAction import AbsTriviaAction
from .triviaActionType import TriviaActionType
from ...misc import utils as utils


class ClearSuperTriviaQueueTriviaAction(AbsTriviaAction):

    def __init__(
        self,
        actionId: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str,
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(twitchChatMessageId):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')

        self.__twitchChannel: Final[str] = twitchChannel
        self.__twitchChannelId: Final[str] = twitchChannelId
        self.__twitchChatMessageId: Final[str] = twitchChatMessageId

    @property
    def triviaActionType(self) -> TriviaActionType:
        return TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId

    @property
    def twitchChatMessageId(self) -> str:
        return self.__twitchChatMessageId
