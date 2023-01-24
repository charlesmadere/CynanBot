from typing import List

import CynanBotCommon.utils as utils
from twitch.absChannelJoinEvent import AbsChannelJoinEvent
from twitch.channelJoinEventType import ChannelJoinEventType


class JoinChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, channels: List[str]):
        super().__init__(eventType = ChannelJoinEventType.JOIN)

        if not utils.areValidStrs(channels):
            raise ValueError(f'channels argument is malformed: \"{channels}\"')

        self.__channels: List[str] = channels

    def getChannels(self) -> List[str]:
        return self.__channels
