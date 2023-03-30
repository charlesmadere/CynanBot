from twitchio import Message
from twitchio.channel import Channel
from twitchio.ext.commands import Context
from twitchio.ext.pubsub import PubSubChannelPointsMessage

from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelPointsMessage import TwitchChannelPointsMessage
from twitch.twitchConfiguration import TwitchConfiguration
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchContext import TwitchContext
from twitch.twitchIoChannel import TwitchIoChannel
from twitch.twitchIoChannelPointsMessage import TwitchIoChannelPointsMessage
from twitch.twitchIoContext import TwitchIoContext
from twitch.twitchIoMessage import TwitchIoMessage
from twitch.twitchMessage import TwitchMessage
from users.usersRepository import UsersRepository


class TwitchIoConfiguration(TwitchConfiguration):

    def __init__(
        self,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    def getChannel(self, channel: Channel) -> TwitchChannel:
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        return TwitchIoChannel(channel = channel)

    async def getChannelPointsMessage(self, channelPointsMessage: PubSubChannelPointsMessage) -> TwitchChannelPointsMessage:
        if not isinstance(channelPointsMessage, PubSubChannelPointsMessage):
            raise ValueError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')

        userId = str(channelPointsMessage.channel_id)
        userName = await self.__userIdsRepository.fetchUserName(userId)
        user = await self.__usersRepository.getUserAsync(userName)

        return TwitchIoChannelPointsMessage(
            channelPointsMessage = channelPointsMessage,
            user = user
        )

    def getContext(self, context: Context) -> TwitchContext:
        if not isinstance(context, Context):
            raise ValueError(f'context argument is malformed: \"{context}\"')

        return TwitchIoContext(context = context)

    def getMessage(self, message: Message) -> TwitchMessage:
        if not isinstance(message, Message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        return TwitchIoMessage(message = message)

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
