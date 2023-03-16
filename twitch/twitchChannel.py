from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
