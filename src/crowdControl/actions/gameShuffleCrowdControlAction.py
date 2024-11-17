from datetime import datetime

from .crowdControlAction import CrowdControlAction
from .crowdControlActionType import CrowdControlActionType


class GameShuffleCrowdControlAction(CrowdControlAction):

    def __init__(
        self,
        isOriginOfGigaShuffle: bool,
        dateTime: datetime,
        actionId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__isOriginOfGigaShuffle: bool = isOriginOfGigaShuffle

    @property
    def actionType(self) -> CrowdControlActionType:
        return CrowdControlActionType.GAME_SHUFFLE

    @property
    def isOriginOfGigaShuffle(self) -> bool:
        return self.__isOriginOfGigaShuffle
