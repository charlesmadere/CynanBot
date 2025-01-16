from twitchio.ext.commands import Context

from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoMessage import TwitchIoMessage
from ..twitchAuthor import TwitchAuthor
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchContext import TwitchContext
from ..twitchMessage import TwitchMessage
from ..twitchMessageTags import TwitchMessageTags
from ..twitchMessageable import TwitchMessageable
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchIoContext(TwitchContext, TwitchMessageable):

    def __init__(
        self,
        context: Context,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(context, Context):
            raise TypeError(f'context argument is malformed: \"{context}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__context: Context = context

        self.__author: TwitchAuthor = TwitchIoAuthor(
            author = context.author
        )

        self.__message: TwitchMessage = TwitchIoMessage(
            message = context.message,
            userIdsRepository = userIdsRepository
        )

    def getAuthor(self) -> TwitchAuthor:
        return self.__author

    def getAuthorDisplayName(self) -> str:
        return self.__author.getDisplayName()

    def getAuthorId(self) -> str:
        return self.__author.getId()

    def getAuthorName(self) -> str:
        return self.__author.getName()

    def getMessageContent(self) -> str | None:
        return self.__message.getContent()

    async def getMessageId(self) -> str:
        return await self.__message.getMessageId()

    async def getMessageTags(self) -> TwitchMessageTags:
        return await self.__message.getTags()

    async def getTwitchChannelId(self) -> str:
        return await self.__message.getTwitchChannelId()

    def getTwitchChannelName(self) -> str:
        return self.__context.channel.name

    def isAuthorMod(self) -> bool:
        return self.__author.isMod()

    def isAuthorVip(self) -> bool:
        return self.__author.isVip()

    async def isMessageFromExternalSharedChat(self) -> bool:
        return await self.__message.isMessageFromExternalSharedChat()

    async def isMessageReply(self) -> bool:
        return await self.__message.isReply()

    async def send(self, message: str):
        await self.__context.send(message)

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
