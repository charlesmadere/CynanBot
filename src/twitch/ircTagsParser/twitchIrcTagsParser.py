from typing import Any

from frozendict import frozendict

from .exceptions import TwitchIrcTagsAreMissingDisplayNameException, \
    TwitchIrcTagsAreMalformedException, \
    TwitchIrcTagsAreMissingMessageIdException, \
    TwitchIrcTagsAreMissingRoomIdException, \
    TwitchIrcTagsAreMissingUserIdException
from .twitchIrcTags import TwitchIrcTags
from .twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface
from ...misc import utils as utils


class TwitchIrcTagsParser(TwitchIrcTagsParserInterface):

    async def __parseSubscriberStringToBool(
        self,
        subscriberString: str | Any | None,
    ) -> bool:
        if not utils.isValidStr(subscriberString):
            return False

        try:
            subscriberInt = int(subscriberString)
            return subscriberInt == 1
        except:
            pass

        try:
            return utils.strictStrToBool(subscriberString)
        except:
            pass

        return False

    async def parseTwitchIrcTags(
        self,
        rawIrcTags: dict[Any, Any] | Any | None,
    ) -> TwitchIrcTags:
        if not isinstance(rawIrcTags, dict) or len(rawIrcTags) == 0:
            raise TwitchIrcTagsAreMalformedException(f'rawIrcTags argument is malformed: \"{rawIrcTags}\"')

        displayName: str | Any | None = rawIrcTags.get('display-name', None)
        if not utils.isValidStr(displayName):
            raise TwitchIrcTagsAreMissingDisplayNameException(f'Twitch message tags are missing \"display-name\" value ({displayName=}) ({rawIrcTags=})')

        messageId: str | Any | None = rawIrcTags.get('id', None)
        if not utils.isValidStr(messageId):
            raise TwitchIrcTagsAreMissingMessageIdException(f'Twitch message tags are missing \"id\" value ({messageId=}) ({rawIrcTags=})')

        roomId: str | Any | None = rawIrcTags.get('room-id', None)
        if not utils.isValidStr(roomId):
            raise TwitchIrcTagsAreMissingRoomIdException(f'Twitch message tags are missing \"room-id\" value ({roomId=}) ({rawIrcTags=})')

        userId: str | Any | None = rawIrcTags.get('user-id', None)
        if not utils.isValidStr(userId):
            raise TwitchIrcTagsAreMissingUserIdException(f'Twitch message tags are missing \"user-id\" value ({userId=}) ({rawIrcTags=})')

        isSubscribed = await self.__parseSubscriberStringToBool(rawIrcTags.get('subscriber', None))
        replyParentMsgBody: str | Any | None = rawIrcTags.get('reply-parent-msg-body', None)
        replyParentMsgId: str | Any | None = rawIrcTags.get('reply-parent-msg-id', None)
        replyParentUserId: str | Any | None = rawIrcTags.get('reply-parent-user-id', None)
        replyParentUserLogin: str | Any | None = rawIrcTags.get('reply-parent-user-login', None)
        sourceMessageId: str | Any | None = rawIrcTags.get('source-id', None)
        sourceTwitchChannelId: str | Any | None = rawIrcTags.get('source-room-id', None)

        return TwitchIrcTags(
            rawTags = frozendict(rawIrcTags),
            isSubscribed = isSubscribed,
            displayName = displayName,
            messageId = messageId,
            replyParentMsgBody = replyParentMsgBody,
            replyParentMsgId = replyParentMsgId,
            replyParentUserId = replyParentUserId,
            replyParentUserLogin = replyParentUserLogin,
            sourceMessageId = sourceMessageId,
            sourceTwitchChannelId = sourceTwitchChannelId,
            twitchChannelId = roomId,
            userId = userId,
        )
