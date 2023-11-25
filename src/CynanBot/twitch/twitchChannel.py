from abc import abstractmethod

from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
