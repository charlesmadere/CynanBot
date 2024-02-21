from abc import ABC

from CynanBot.twitch.configuration.channelJoinEventType import \
    ChannelJoinEventType


class AbsChannelJoinEvent(ABC):

    def __init__(self, eventType: ChannelJoinEventType):
        assert isinstance(eventType, ChannelJoinEventType), f"malformed {eventType=}"

        self.__eventType: ChannelJoinEventType = eventType

    def getEventType(self) -> ChannelJoinEventType:
        return self.__eventType
