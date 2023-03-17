from twitchio import Message
from twitchio.abcs import Messageable
from twitchio.channel import Channel
from twitchio.ext.commands import Context

import CynanBotCommon.utils as utils
from twitch.twitchChannel import TwitchChannel
from twitch.twitchConfiguration import TwitchConfiguration
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchContext import TwitchContext
from twitch.twitchIoChannel import TwitchIoChannel
from twitch.twitchIoContext import TwitchIoContext
from twitch.twitchIoMessage import TwitchIoMessage
from twitch.twitchIoMessageable import TwitchIoMessageable
from twitch.twitchMessage import TwitchMessage
from twitch.twitchMessageable import TwitchMessageable


class TwitchIoConfiguration(TwitchConfiguration):

    def __init__(self):
        pass

    def getChannel(self, channel: Channel) -> TwitchChannel:
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')

        return TwitchIoChannel(channel = channel)

    def getContext(self, context: Context) -> TwitchContext:
        if not isinstance(context, Context):
            raise ValueError(f'context argument is malformed: \"{context}\"')

        return TwitchIoContext(context = context)

    def getMessage(self, message: Message) -> TwitchMessage:
        if not isinstance(message, Message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        return TwitchIoMessage(message = message)

    def getMessageable(
        self,
        messageable: Messageable,
        twitchChannelName: str
    ) -> TwitchMessageable:
        if not isinstance(messageable, Messageable):
            raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
        elif not utils.isValidStr(twitchChannelName):
            raise ValueError(f'twitchChannelName argument is malformed: \"{twitchChannelName}\"')

        return TwitchIoMessageable(
            messageable = messageable,
            twitchChannelName = twitchChannelName
        )

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
