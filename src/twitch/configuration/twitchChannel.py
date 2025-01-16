from abc import abstractmethod

from .twitchConfigurationType import TwitchConfigurationType
from .twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    @property
    @abstractmethod
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        pass
