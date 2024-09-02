from typing import Any

from twitchio import Message

from .exceptions import TwitchIoHasMalformedTagsException, TwitchIoTagsIsMissingRoomIdException
from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoChannel import TwitchIoChannel
from ..twitchAuthor import TwitchAuthor
from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessage import TwitchMessage
from ..twitchMessageReplyData import TwitchMessageReplyData
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

        self.__checkedForReplyData: bool = False
        self.__twitchChannelId: str | None = None
        self.__replyData: TwitchMessageReplyData | None = None

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

    async def getReplyData(self) -> TwitchMessageReplyData | None:
        if self.__checkedForReplyData:
            return self.__replyData

        self.__checkedForReplyData = True
        tags: dict[Any, Any] | Any | None = self.__message.tags

        if not isinstance(tags, dict) or len(tags) == 0:
            return None

        replyParentMsgBody: str | Any | None = tags.get('reply-parent-msg-body', None)
        replyParentMsgId: str | Any | None = tags.get('reply-parent-msg-id', None)
        replyParentUserId: str | Any | None = tags.get('reply-parent-user-id', None)
        replyParentUserLogin: str | Any | None = tags.get('reply-parent-user-login', None)

        if not utils.isValidStr(replyParentMsgBody) \
                or not utils.isValidStr(replyParentMsgId) \
                or not utils.isValidStr(replyParentUserId) \
                or not utils.isValidStr(replyParentUserLogin):
            return None

        replyData = TwitchMessageReplyData(
            msgBody = replyParentMsgBody,
            msgsId = replyParentMsgId,
            userId = replyParentUserId,
            userLogin = replyParentUserLogin
        )

        self.__replyData = replyData
        return replyData

    async def getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is not None:
            return twitchChannelId

        tags: dict[Any, Any] | Any | None = self.__message.tags
        if not isinstance(tags, dict) or len(tags) == 0:
            raise TwitchIoHasMalformedTagsException(f'Encountered malformed \"tags\" value when trying to retrieve twitchChannelId ({twitchChannelId=}) from tags ({tags=}) ({self=})')

        twitchChannelId = tags.get('room-id')
        if not utils.isValidStr(twitchChannelId):
            raise TwitchIoTagsIsMissingRoomIdException(f'Encoutnered malformed twitchChannelId ({twitchChannelId=}) value when trying to retrieve \"room-id\" from tags ({tags=}) ({self=})')

        self.__twitchChannelId = twitchChannelId
        return twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    @property
    def isEcho(self) -> bool:
        return self.__message.echo

    async def isReply(self) -> bool:
        return await self.getReplyData() is not None

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
