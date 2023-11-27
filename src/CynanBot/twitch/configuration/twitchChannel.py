from abc import abstractmethod

from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
