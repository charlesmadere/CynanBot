from typing import Optional

from twitchio.ext.commands import Context

from CynanBot.twitch.twitchAuthor import TwitchAuthor
from CynanBot.twitch.twitchConfigurationType import TwitchConfigurationType
from CynanBot.twitch.twitchContext import TwitchContext
from CynanBot.twitch.twitchIoAuthor import TwitchIoAuthor
from CynanBot.twitch.twitchMessageable import TwitchMessageable


class TwitchIoContext(TwitchContext, TwitchMessageable):

    def __init__(self, context: Context):
        if not isinstance(context, Context):
            raise ValueError(f'context argument is malformed: \"{context}\"')

        self.__context: Context = context
        self.__author: TwitchAuthor = TwitchIoAuthor(context.author)

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
