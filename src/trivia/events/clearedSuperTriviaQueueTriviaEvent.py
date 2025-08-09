import locale

from .absTriviaEvent import AbsTriviaEvent
from .triviaEventType import TriviaEventType
from ...misc import utils as utils


class ClearedSuperTriviaQueueTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        numberOfGamesRemoved: int,
        previousQueueSize: int,
        actionId: str,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str,
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId,
        )

        if not utils.isValidInt(numberOfGamesRemoved):
            raise TypeError(f'numberOfGamesRemoved argument is malformed: \"{numberOfGamesRemoved}\"')
        elif numberOfGamesRemoved < 0 or numberOfGamesRemoved > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfGamesRemoved argument is out of bounds: {numberOfGamesRemoved}')
        elif not utils.isValidInt(previousQueueSize):
            raise TypeError(f'previousQueueSize argument is malformed: \"{previousQueueSize}\"')
        elif previousQueueSize < 0 or previousQueueSize > utils.getIntMaxSafeSize():
            raise ValueError(f'previousQueueSize argument is malformed: \"{previousQueueSize}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(twitchChatMessageId):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')

        self.__numberOfGamesRemoved: int = numberOfGamesRemoved
        self.__previousQueueSize: int = previousQueueSize
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__twitchChatMessageId: str = twitchChatMessageId

    @property
    def numberOfGamesRemoved(self) -> int:
        return self.__numberOfGamesRemoved

    @property
    def numberOfGamesRemovedStr(self) -> str:
        return locale.format_string("%d", self.__numberOfGamesRemoved, grouping = True)

    @property
    def previousQueueSize(self) -> int:
        return self.__previousQueueSize

    @property
    def previousQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__previousQueueSize, grouping = True)

    @property
    def triviaEventType(self) -> TriviaEventType:
        return TriviaEventType.CLEARED_SUPER_TRIVIA_QUEUE

    @property
    def twitchChannel(self) -> str:
        return self.__twitchChannel

    @property
    def twitchChannelId(self) -> str:
        return self.__twitchChannelId

    @property
    def twitchChatMessageId(self) -> str:
        return self.__twitchChatMessageId
