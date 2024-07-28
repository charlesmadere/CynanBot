from typing import Any

from twitchio import Message

from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoChannel import TwitchIoChannel
from ..twitchAuthor import TwitchAuthor
from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessage import TwitchMessage
from ....misc import utils as utils
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchIoMessage(TwitchMessage):

    def __init__(
        self,
        message: Message,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(message, Message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__message: Message = message
        self.__author: TwitchAuthor = TwitchIoAuthor(message.author)
        self.__channel: TwitchChannel = TwitchIoChannel(
            channel = message.channel,
            userIdsRepository = userIdsRepository
        )

        self.__isReply: bool | None = None
        self.__twitchChannelId: str | None = None

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

    async def getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is not None:
            return twitchChannelId

        tags: dict[Any, Any] = self.__message.tags
        twitchChannelId = tags['room-id']

        if not utils.isValidStr(twitchChannelId):
            raise RuntimeError(f'Error trying to retrieve twitchChannelId ({twitchChannelId=}) from tags ({tags=}) ({self=})')

        parentTwitchChannelId = await self.__channel.getTwitchChannelId()

        if twitchChannelId != parentTwitchChannelId:
            raise RuntimeError(f'Tags twitchChannelId ({twitchChannelId=}) is different than parentTwitchChannelId ({parentTwitchChannelId=}) ({tags=}) ({self=})')

        self.__twitchChannelId = twitchChannelId
        return twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    @property
    def isEcho(self) -> bool:
        return self.__message.echo

    async def isReply(self) -> bool:
        isReply = self.__isReply

        if isReply is not None:
            return isReply

        isReply = False
        tags: dict[Any, Any] | Any | None = self.__message.tags

        if isinstance(tags, dict) and len(tags) >= 1:
            replyParentMsgBody: str | Any | None = tags.get('reply-parent-msg-body')
            replyParentMsgId: str | Any | None = tags.get('reply-parent-msg-id')
            replyParentUserId: str | Any | None = tags.get('reply-parent-user-id')
            replyParentUserLogin: str | Any | None = tags.get('reply-parent-user-login')

            isReply = utils.isValidStr(replyParentMsgBody) and \
                utils.isValidStr(replyParentMsgId) and \
                utils.isValidStr(replyParentUserId) and \
                utils.isValidStr(replyParentUserLogin)

        self.__isReply = isReply
        return isReply
