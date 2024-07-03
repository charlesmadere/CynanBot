from .absChannelJoinEvent import AbsChannelJoinEvent
from .channelJoinEventType import ChannelJoinEventType


class FinishedJoiningChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, allChannels: list[str]):
        if not isinstance(allChannels, list):
            raise TypeError(f'allChannels argument is malformed: \"{allChannels}\"')

        self.__allChannels: list[str] = allChannels

    def getAllChannels(self) -> list[str]:
        return self.__allChannels

    def getEventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.FINISHED
