from dataclasses import dataclass
from typing import Any

from frozendict import frozendict


@dataclass(frozen = True)
class TwitchMessageTags:
    rawTags: frozendict[Any, Any]
    messageId: str
    replyParentMsgBody: str | None
    replyParentMsgId: str | None
    replyParentUserId: str | None
    replyParentUserLogin: str | None
    twitchChannelId: str
