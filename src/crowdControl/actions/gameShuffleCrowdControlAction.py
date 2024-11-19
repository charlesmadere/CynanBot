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

    @property
    def startOfGigaShuffleSize(self) -> int | None:
        return self.__startOfGigaShuffleSize
