from abc import ABC, abstractmethod

from CynanBot.twitch.configuration.channelJoinEventType import \
    ChannelJoinEventType


class AbsChannelJoinEvent(ABC):

    @abstractmethod
    def getEventType(self) -> ChannelJoinEventType:
        pass
