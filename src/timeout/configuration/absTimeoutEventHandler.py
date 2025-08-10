from abc import ABC, abstractmethod

from ..listener.timeoutEventListener import TimeoutEventListener
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsTimeoutEventHandler(TimeoutEventListener, ABC):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
