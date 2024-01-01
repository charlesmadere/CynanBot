from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.configuration.absChannelJoinEvent import \
    AbsChannelJoinEvent
from CynanBot.twitch.configuration.channelJoinEventType import \
    ChannelJoinEventType


class FinishedJoiningChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, allChannels: Optional[List[str]]):
        super().__init__(eventType = ChannelJoinEventType.FINISHED)

        self.__allChannels: Optional[List[str]] = allChannels

    def getAllChannels(self) -> Optional[List[str]]:
        return self.__allChannels

    def hasAllChannels(self) -> bool:
        return utils.hasItems(self.__allChannels)
