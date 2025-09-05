from abc import ABC, abstractmethod

from ..listener.timeoutEventListener import TimeoutEventListener
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsTimeoutEventHandler(TimeoutEventListener, ABC):

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
