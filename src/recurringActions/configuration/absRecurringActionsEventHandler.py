from abc import abstractmethod

from ..recurringActionEventListener import RecurringActionEventListener
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider


class AbsRecurringActionsEventHandler(RecurringActionEventListener):

    @abstractmethod
    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        pass
