from abc import ABC, abstractmethod

from ..triviaEventListener import TriviaEventListener
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsTriviaEventHandler(TriviaEventListener, ABC):

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
