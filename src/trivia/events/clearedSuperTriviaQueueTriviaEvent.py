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
        twitchChannelId: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
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

        self.__numberOfGamesRemoved: int = numberOfGamesRemoved
        self.__previousQueueSize: int = previousQueueSize
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId

    def getNumberOfGamesRemoved(self) -> int:
        return self.__numberOfGamesRemoved

    def getNumberOfGamesRemovedStr(self) -> str:
        return locale.format_string("%d", self.__numberOfGamesRemoved, grouping = True)

    def getPreviousQueueSize(self) -> int:
        return self.__previousQueueSize

    def getPreviousQueueSizeStr(self) -> str:
        return locale.format_string("%d", self.__previousQueueSize, grouping = True)

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.CLEARED_SUPER_TRIVIA_QUEUE

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId
