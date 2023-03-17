from typing import Optional

from twitchio import Message

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchChannel import TwitchChannel
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchIoAuthor import TwitchIoAuthor
from twitch.twitchIoChannel import TwitchIoChannel
from twitch.twitchMessage import TwitchMessage


class TwitchIoMessage(TwitchMessage):

    def __init__(self, message: Message):
        if not isinstance(message, Message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        self.__message: Message = message
        self.__author: TwitchAuthor = TwitchIoAuthor(message.author)
        self.__channel: TwitchChannel = TwitchIoChannel(message.channel)

    def getAuthor(self) -> TwitchAuthor:
        return self.__author

    def getAuthorId(self) -> str:
        return self.__author.getId()

    def getAuthorName(self) -> str:
        return self.__author.getName()

    def getChannel(self) -> TwitchChannel:
        return self.__channel

    def getContent(self) -> Optional[str]:
        return self.__message.content

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
