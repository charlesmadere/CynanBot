from abc import abstractmethod

from CynanBot.twitch.twitchConfigurationType import TwitchConfigurationType
from CynanBot.twitch.twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
