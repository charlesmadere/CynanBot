from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchMessageReplyData:
    msgBody: str
    msgId: str
    userId: str
    userLogin: str
