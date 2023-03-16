from typing import Optional

from twitchio.ext.commands import Context

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchContext import TwitchContext
from twitch.twitchIoAuthor import TwitchIoAuthor
from twitch.twitchMessageable import TwitchMessageable


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

    async def send(self, message: str):
        await self.__context.send(message)
