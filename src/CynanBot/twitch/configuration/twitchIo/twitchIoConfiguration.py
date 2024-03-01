from twitchio import Message
from twitchio.channel import Channel
from twitchio.ext.commands import Context

from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfiguration import \
    TwitchConfiguration
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.configuration.twitchIo.twitchIoChannel import \
    TwitchIoChannel
from CynanBot.twitch.configuration.twitchIo.twitchIoContext import \
    TwitchIoContext
from CynanBot.twitch.configuration.twitchIo.twitchIoMessage import \
    TwitchIoMessage
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchIoConfiguration(TwitchConfiguration):

    def __init__(self, userIdsRepository: UserIdsRepositoryInterface):
        if not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    def getChannel(self, channel: Channel) -> TwitchChannel:
        if not isinstance(channel, Channel):
            raise TypeError(f'channel argument is malformed: \"{channel}\"')

        return TwitchIoChannel(
            channel = channel,
            userIdsRepository = self.__userIdsRepository,
        )

    def getContext(self, context: Context) -> TwitchContext:
        if not isinstance(context, Context):
            raise TypeError(f'context argument is malformed: \"{context}\"')

        return TwitchIoContext(
            context = context,
            userIdsRepository = self.__userIdsRepository
        )

    def getMessage(self, message: Message) -> TwitchMessage:
        if not isinstance(message, Message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        return TwitchIoMessage(
            message = message,
            userIdsRepository = self.__userIdsRepository
        )

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
