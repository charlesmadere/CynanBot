from typing import Any
from typing import Final

from twitchio import Message

from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoChannel import TwitchIoChannel
from ..twitchAuthor import TwitchAuthor
from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessage import TwitchMessage
from ...ircTagsParser.twitchIrcTags import TwitchIrcTags
from ...ircTagsParser.twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface
from ....misc import utils as utils
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchIoMessage(TwitchMessage):

    def __init__(
        self,
        message: Message,
        twitchIrcTagsParser: TwitchIrcTagsParserInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(message, Message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(twitchIrcTagsParser, TwitchIrcTagsParserInterface):
            raise TypeError(f'twitchIrcTagsParser argument is malformed: \"{twitchIrcTagsParser}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__message: Final[Message] = message
        self.__twitchIrcTagsParser: Final[TwitchIrcTagsParserInterface] = twitchIrcTagsParser

        self.__author: Final[TwitchAuthor] = TwitchIoAuthor(
            author = message.author,
        )

        self.__channel: Final[TwitchChannel] = TwitchIoChannel(
            channel = message.channel,
            userIdsRepository = userIdsRepository,
        )

        self.__tags: TwitchIrcTags | None = None

    def getAuthor(self) -> TwitchAuthor:
        return self.__author

    def getAuthorId(self) -> str:
        return self.__author.getId()

    def getAuthorName(self) -> str:
        return self.__author.getName()

    def getChannel(self) -> TwitchChannel:
        return self.__channel

    def getContent(self) -> str | None:
        return self.__message.content

    async def getMessageId(self) -> str:
        tags = await self.getTags()
        return tags.messageId

    async def getTags(self) -> TwitchIrcTags:
        tags = self.__tags

        if tags is not None:
            return tags

        rawIrcTags: dict[Any, Any] | Any | None = self.__message.tags

        tags = await self.__twitchIrcTagsParser.parseTwitchIrcTags(
            rawIrcTags = rawIrcTags
        )

        self.__tags = tags
        return tags

    async def getTwitchChannelId(self) -> str:
        tags = await self.getTags()
        return tags.twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    @property
    def isAuthorMod(self) -> bool:
        return self.__author.isMod

    @property
    def isAuthorVip(self) -> bool:
        return self.__author.isVip

    @property
    def isEcho(self) -> bool:
        return self.__message.echo

    async def isMessageFromExternalSharedChat(self) -> bool:
        tags = await self.getTags()

        if not utils.isValidStr(tags.sourceTwitchChannelId):
            return False

        twitchChannelId = await self.getTwitchChannelId()
        return twitchChannelId != tags.sourceTwitchChannelId

    async def isReply(self) -> bool:
        tags = await self.getTags()
        return utils.isValidStr(tags.replyParentMsgId)

    async def isTwitchSubscriber(self) -> bool:
        tags = await self.getTags()
        return tags.isSubscribed

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
