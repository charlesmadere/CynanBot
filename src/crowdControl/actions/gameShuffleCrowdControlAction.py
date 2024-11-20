import locale
from datetime import datetime

from .crowdControlAction import CrowdControlAction
from .crowdControlActionType import CrowdControlActionType
from ...misc import utils as utils


class GameShuffleCrowdControlAction(CrowdControlAction):

    def __init__(
        self,
        dateTime: datetime,
        startOfGigaShuffleSize: int | None,
        actionId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None
    ):
        super().__init__(
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId
        )

        if startOfGigaShuffleSize is not None and not utils.isValidInt(startOfGigaShuffleSize):
            raise TypeError(f'startOfGigaShuffleSize argument is malformed: \"{startOfGigaShuffleSize}\"')

        self.__startOfGigaShuffleSize: int | None = startOfGigaShuffleSize

    @property
    def actionType(self) -> CrowdControlActionType:
        return CrowdControlActionType.GAME_SHUFFLE

    def requireStartOfGigaShuffleSize(self) -> int:
        startOfGigaShuffleSize = self.__startOfGigaShuffleSize

        if not utils.isValidInt(startOfGigaShuffleSize):
            raise RuntimeError(f'No startOfGigaShuffleSize value is available: {self}')

        return startOfGigaShuffleSize

    @property
    def startOfGigaShuffleSize(self) -> int | None:
        return self.__startOfGigaShuffleSize

    @property
    def startOfGigaShuffleSizeStr(self) -> str:
        startOfGigaShuffleSize = self.requireStartOfGigaShuffleSize()
        return locale.format_string("%d", startOfGigaShuffleSize, grouping = True)
