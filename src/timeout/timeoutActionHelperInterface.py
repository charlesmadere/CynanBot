from abc import ABC, abstractmethod

from .timeoutActionData import TimeoutActionData
from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider


class TimeoutActionHelperInterface(ABC):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitTimeout(self, timeoutData: TimeoutActionData) -> bool:
        pass
