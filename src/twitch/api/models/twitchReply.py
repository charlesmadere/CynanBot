from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class TwitchReply:
    parentMessageBody: str | None
    parentMessageId: str
    parentUserId: str
    parentUserLogin: str
    parentUserName: str
    threadMessageId: str
    threadUserId: str
    threadUserLogin: str
    threadUserName: str
