from twitchio.ext.pubsub import PubSubChannelPointsMessage

from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchConfigurationType import TwitchConfigurationType
from users.user import User


class TwitchIoChannelPointsMessage(TwitchChannelPointsMessage):

    def __init__(
        self,
        channelPointsMessage: PubSubChannelPointsMessage,
        user: User
    ):
        if not isinstance(channelPointsMessage, PubSubChannelPointsMessage):
            raise ValueError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')
        elif not isinstance(user, User):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        self.__channelPointsMessage: PubSubChannelPointsMessage = channelPointsMessage
        self.__user: User = user

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
