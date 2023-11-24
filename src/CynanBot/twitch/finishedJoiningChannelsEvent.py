from typing import List, Optional

import CynanBotCommon.utils as utils
from twitch.absChannelJoinEvent import AbsChannelJoinEvent
from twitch.channelJoinEventType import ChannelJoinEventType


class FinishedJoiningChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, allChannels: Optional[List[str]]):
        super().__init__(eventType = ChannelJoinEventType.FINISHED)

        self.__allChannels: Optional[List[str]] = allChannels

    def getAllChannels(self) -> Optional[List[str]]:
        return self.__allChannels

    def hasAllChannels(self) -> bool:
        return utils.hasItems(self.__allChannels)
