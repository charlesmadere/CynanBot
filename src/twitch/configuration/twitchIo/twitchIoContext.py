from twitchio.ext.commands import Context

from .twitchIoAuthor import TwitchIoAuthor
from ..twitchAuthor import TwitchAuthor
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchContext import TwitchContext
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
        self.__twitchChannelId: str | None = None
        self.__author: TwitchAuthor = TwitchIoAuthor(context.author)
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    def getAuthor(self) -> TwitchAuthor:
        return self.__author

    def getAuthorDisplayName(self) -> str:
        return self.__author.getDisplayName()

    def getAuthorId(self) -> str:
        return self.__author.getId()

    def getAuthorName(self) -> str:
        return self.__author.getName()

    def getMessageContent(self) -> str | None:
        return self.__context.message.content

    async def getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is None:
            twitchChannelId = await self.__userIdsRepository.requireUserId(
                userName = self.getTwitchChannelName()
            )

            self.__twitchChannelId = twitchChannelId

        return twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__context.channel.name

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    def isAuthorMod(self) -> bool:
        return self.__author.isMod()

    def isAuthorVip(self) -> bool:
        return self.__author.isVip()

    async def send(self, message: str):
        await self.__context.send(message)
