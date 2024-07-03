from abc import abstractmethod

from .twitchConfigurationType import TwitchConfigurationType
from .twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
