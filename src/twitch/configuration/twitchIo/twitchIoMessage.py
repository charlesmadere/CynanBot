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
        return await self.__channel.getTwitchChannelId()

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    def isEcho(self) -> bool:
        return self.__message.echo

    def isReply(self) -> bool:
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
