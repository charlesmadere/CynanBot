from typing import Optional

from twitchio.ext.commands import Context

from twitch.twitchContext import TwitchContext
from twitch.twitchContextType import TwitchContextType
from twitch.twitchMessageable import TwitchMessageable


class TwitchIoContext(TwitchContext, TwitchMessageable):

    def __init__(self, context: Context):
        if not isinstance(context, Context):
            raise ValueError(f'context argument is malformed: \"{context}\"')

        self.__context: Context = context

    def getAuthorId(self) -> str:
        return self.__context.author.id

    def getAuthorName(self) -> str:
        return self.__context.author.name

    def getMessageContent(self) -> Optional[str]:
        return self.__context.message.content

    def getTwitchChannelName(self) -> str:
        return self.__context.channel.name

    def getTwitchContextType(self) -> TwitchContextType:
        return TwitchContextType.TWITCHIO

    async def send(self, message: str):
        await self.__context.send(message)
