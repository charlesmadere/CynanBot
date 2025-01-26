import re
import traceback
from typing import Any, Pattern

from frozendict import frozendict

from .exceptions import TwitchIrcTagsAreMissingDisplayNameException, \
    TwitchIrcTagsAreMalformedException, \
    TwitchIrcTagsAreMissingMessageIdException, \
    TwitchIrcTagsAreMissingRoomIdException, \
    TwitchIrcTagsAreMissingUserIdException
from .twitchIrcTags import TwitchIrcTags
from .twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TwitchIrcTagsParser(TwitchIrcTagsParserInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__badgesStringSubscriberRegEx: Pattern = re.compile(r'subscriber\/(\d{2})', re.IGNORECASE)

    async def parseSubscriberTier(
        self,
        badgesString: str | Any | None
    ) -> TwitchIrcTags.SubscriberTier:
        if not utils.isValidStr(badgesString):
            return TwitchIrcTags.SubscriberTier.NONE

        subscriberStringMatch = self.__badgesStringSubscriberRegEx.search(badgesString)
        if subscriberStringMatch is None:
            return TwitchIrcTags.SubscriberTier.NONE

        subscriberTierString = subscriberStringMatch.group(1)
        if not utils.isValidStr(subscriberTierString):
            return TwitchIrcTags.SubscriberTier.NONE

        match subscriberTierString:
            case '10': return TwitchIrcTags.SubscriberTier.TIER_1
            case '20': return TwitchIrcTags.SubscriberTier.TIER_2
            case '30': return TwitchIrcTags.SubscriberTier.TIER_3
            case _: return TwitchIrcTags.SubscriberTier.NONE

    async def parseTwitchIrcTags(
        self,
        rawIrcTags: dict[Any, Any] | Any | None
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

        replyParentMsgBody: str | Any | None = rawIrcTags.get('reply-parent-msg-body', None)
        replyParentMsgId: str | Any | None = rawIrcTags.get('reply-parent-msg-id', None)
        replyParentUserId: str | Any | None = rawIrcTags.get('reply-parent-user-id', None)
        replyParentUserLogin: str | Any | None = rawIrcTags.get('reply-parent-user-login', None)
        sourceMessageId: str | Any | None = rawIrcTags.get('source-id', None)
        sourceTwitchChannelId: str | Any | None = rawIrcTags.get('source-room-id', None)

        badgesString: str | Any | None = rawIrcTags.get('badges', None)
        subscriberTier = await self.parseSubscriberTier(badgesString)

        return TwitchIrcTags(
            rawTags = frozendict(rawIrcTags),
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
            subscriberTier = subscriberTier
        )
