from abc import ABC, abstractmethod

from ..triviaEventListener import TriviaEventListener
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsTriviaEventHandler(TriviaEventListener, ABC):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
