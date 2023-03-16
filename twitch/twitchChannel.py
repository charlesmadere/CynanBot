from twitch.twitchChannelType import TwitchChannelType
from twitch.twitchMessageable import TwitchMessageable


class TwitchChannel(TwitchMessageable):

    def getTwitchChannelType(self) -> TwitchChannelType:
        pass
