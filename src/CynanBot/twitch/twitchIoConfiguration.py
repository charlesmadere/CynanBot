from twitchio import Message
from twitchio.channel import Channel
from twitchio.ext.commands import Context
from twitchio.ext.pubsub import PubSubChannelPointsMessage

from CynanBot.twitch.twitchChannel import TwitchChannel
from CynanBot.twitch.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchConfiguration import TwitchConfiguration
from CynanBot.twitch.twitchConfigurationType import TwitchConfigurationType
from CynanBot.twitch.twitchContext import TwitchContext
from CynanBot.twitch.twitchIoChannel import TwitchIoChannel
from CynanBot.twitch.twitchIoChannelPointsMessage import \
    TwitchIoChannelPointsMessage
from CynanBot.twitch.twitchIoContext import TwitchIoContext
from CynanBot.twitch.twitchIoMessage import TwitchIoMessage
from CynanBot.twitch.twitchMessage import TwitchMessage
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.usersRepository import UsersRepository


class TwitchIoConfiguration(TwitchConfiguration):

    def __init__(
        self,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepository
    ):
        if not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    def getChannel(self, channel: Channel) -> TwitchChannel:
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        return TwitchIoChannel(channel = channel)

    async def getChannelPointsMessage(self, channelPointsMessage: PubSubChannelPointsMessage) -> TwitchChannelPointsMessage:
        if not isinstance(channelPointsMessage, PubSubChannelPointsMessage):
            raise ValueError(f'channelPointsMessage argument is malformed: \"{channelPointsMessage}\"')

        userId = str(channelPointsMessage.channel_id)
        userName = await self.__userIdsRepository.requireUserName(userId = userId)
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
