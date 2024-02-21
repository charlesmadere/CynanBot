from typing import Optional

from twitchio import Message

from CynanBot.twitch.configuration.twitchAuthor import TwitchAuthor
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchIo.twitchIoAuthor import \
    TwitchIoAuthor
from CynanBot.twitch.configuration.twitchIo.twitchIoChannel import \
    TwitchIoChannel
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchIoMessage(TwitchMessage):

    def __init__(
        self,
        message: Message,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert isinstance(message, Message), f"malformed {message=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__message: Message = message
        self.__author: TwitchAuthor = TwitchIoAuthor(message.author)
        self.__channel: TwitchChannel = TwitchIoChannel(
            channel = message.channel,
            userIdsRepository = userIdsRepository
        )

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

    async def getTwitchChannelId(self) -> str:
        return await self.__channel.getTwitchChannelId()

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    def isEcho(self) -> bool:
        return self.__message.echo
