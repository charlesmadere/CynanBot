from dataclasses import dataclass
from typing import Any

from frozendict import frozendict


@dataclass(frozen = True, slots = True)
class TwitchIrcTags:
    rawTags: frozendict[Any, Any]
    isSubscribed: bool
    displayName: str
    messageId: str
    replyParentMsgBody: str | None
    replyParentMsgId: str | None
    replyParentUserId: str | None
    replyParentUserLogin: str | None
    sourceMessageId: str | None
    sourceTwitchChannelId: str | None
    twitchChannelId: str
    userId: str
