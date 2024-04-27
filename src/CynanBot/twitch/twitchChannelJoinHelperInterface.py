from abc import ABC, abstractmethod

from CynanBot.twitch.configuration.channelJoinListener import \
    ChannelJoinListener


class TwitchChannelJoinHelperInterface(ABC):

    @abstractmethod
    def joinChannels(self):
        pass

    @abstractmethod
    def setChannelJoinListener(self, listener: ChannelJoinListener | None):
        pass
