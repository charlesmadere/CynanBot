from typing import Any

from frozendict import frozendict
from twitchio import Message

from .exceptions import TwitchIoHasMalformedTagsException, TwitchIoTagsIsMissingMessageIdException, \
    TwitchIoTagsIsMissingRoomIdException
from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoChannel import TwitchIoChannel
from ..twitchAuthor import TwitchAuthor
from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessage import TwitchMessage
from ..twitchMessageTags import TwitchMessageTags
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

        self.__tags: TwitchMessageTags | None = None

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

    async def getTags(self) -> TwitchMessageTags:
        tags = self.__tags

        if tags is not None:
            return tags

        rawTagsDictionary: dict[Any, Any] | Any | None = self.__message.tags
        if not isinstance(rawTagsDictionary, dict) or len(rawTagsDictionary) == 0:
            raise TwitchIoHasMalformedTagsException(f'Encountered malformed TwitchIO tags ({rawTagsDictionary=}) ({self=}) ({self.__message})')

        messageId: str | Any | None = rawTagsDictionary.get('id', None)
        if not utils.isValidStr(messageId):
            raise TwitchIoTagsIsMissingMessageIdException(f'Twitch message tags are missing \"id\" value ({messageId=}) ({tags=})')

        roomId: str | Any | None = rawTagsDictionary.get('room-id', None)
        if not utils.isValidStr(roomId):
            raise TwitchIoTagsIsMissingRoomIdException(f'Twitch message tags are missing \"room-id\" value ({roomId=}) ({tags=})')

        replyParentMsgBody: str | Any | None = rawTagsDictionary.get('reply-parent-msg-body', None)
        replyParentMsgId: str | Any | None = rawTagsDictionary.get('reply-parent-msg-id', None)
        replyParentUserId: str | Any | None = rawTagsDictionary.get('reply-parent-user-id', None)
        replyParentUserLogin: str | Any | None = rawTagsDictionary.get('reply-parent-user-login', None)
        sourceMessageId: str | Any | None = rawTagsDictionary.get('source-id', None)
        sourceTwitchChannelId: str | Any | None = rawTagsDictionary.get('source-room-id', None)

        tags = TwitchMessageTags(
            rawTags = frozendict(rawTagsDictionary),
            messageId = messageId,
            replyParentMsgBody = replyParentMsgBody,
            replyParentMsgId = replyParentMsgId,
            replyParentUserId = replyParentUserId,
            replyParentUserLogin = replyParentUserLogin,
            sourceMessageId = sourceMessageId,
            sourceTwitchChannelId = sourceTwitchChannelId,
            twitchChannelId = roomId
        )

        self.__tags = tags
        return tags

    async def getTwitchChannelId(self) -> str:
        tags = await self.getTags()
        return tags.twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

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

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
