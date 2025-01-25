from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from frozendict import frozendict


@dataclass(frozen = True)
class TwitchIrcTags:

    class SubscriberTier(Enum):
        NONE = auto()
        TIER_1 = auto()
        TIER_2 = auto()
        TIER_3 = auto()

    rawTags: frozendict[Any, Any]
    messageId: str
    replyParentMsgBody: str | None
    replyParentMsgId: str | None
    replyParentUserId: str | None
    replyParentUserLogin: str | None
    sourceMessageId: str | None
    sourceTwitchChannelId: str | None
    twitchChannelId: str
    tier: SubscriberTier
