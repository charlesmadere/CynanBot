from twitch.channelJoinEventType import ChannelJoinEventType


class AbsChannelJoinEvent():

    def __init__(self, eventType: ChannelJoinEventType):
        if not isinstance(eventType, ChannelJoinEventType):
            raise ValueError(f'eventType argument is malformed: \"{eventType}\"')

        self.__eventType: ChannelJoinEventType = eventType

    def getEventType(self) -> ChannelJoinEventType:
        return self.__eventType
