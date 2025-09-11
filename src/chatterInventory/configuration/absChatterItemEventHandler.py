from abc import ABC, abstractmethod

from ..listeners.chatterItemEventListener import ChatterItemEventListener
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsChatterItemEventHandler(ChatterItemEventListener, ABC):

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
