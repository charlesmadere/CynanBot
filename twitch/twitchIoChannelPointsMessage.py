from twitchio.ext.pubsub import PubSubChannelPointsMessage

from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchConfigurationType import TwitchConfigurationType
from users.user import User


class TwitchIoChannelPointsMessage(TwitchChannelPointsMessage):

    def __init__(
        self,
        pubSubChannelPointsMessage: PubSubChannelPointsMessage,
        user: User
    ):
        if not isinstance(pubSubChannelPointsMessage, PubSubChannelPointsMessage):
            raise ValueError(f'pubSubChannelPointsMessage argument is malformed: \"{pubSubChannelPointsMessage}\"')
        elif not isinstance(user, User):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        self.__pubSubChannelPointsMessage: PubSubChannelPointsMessage = pubSubChannelPointsMessage

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
