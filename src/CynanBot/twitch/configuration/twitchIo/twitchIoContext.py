from typing import Optional

from twitchio.ext.commands import Context

from CynanBot.twitch.configuration.twitchAuthor import TwitchAuthor
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.configuration.twitchIo.twitchIoAuthor import \
    TwitchIoAuthor
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchIoContext(TwitchContext, TwitchMessageable):

    def __init__(
        self,
        context: Context,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        assert isinstance(context, Context), f"malformed {context=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"

        self.__context: Context = context
        self.__twitchChannelId: Optional[str] = None
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

    def getMessageContent(self) -> Optional[str]:
        return self.__context.message.content

    async def getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is None:
            twitchChannelId = await self.__userIdsRepository.requireUserId(
                userName = self.getTwitchChannelName()
            )

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
