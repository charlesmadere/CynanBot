from .absChannelJoinEvent import AbsChannelJoinEvent
from .channelJoinEventType import ChannelJoinEventType


class FinishedJoiningChannelsEvent(AbsChannelJoinEvent):

    def __init__(self, allChannels: list[str]):
        if not isinstance(allChannels, list):
            raise TypeError(f'allChannels argument is malformed: \"{allChannels}\"')

        self.__allChannels: list[str] = allChannels

    @property
    def eventType(self) -> ChannelJoinEventType:
        return ChannelJoinEventType.FINISHED

    def getAllChannels(self) -> list[str]:
        return self.__allChannels
