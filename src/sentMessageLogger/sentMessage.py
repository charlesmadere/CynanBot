from dataclasses import dataclass

from .messageMethod import MessageMethod
from ..misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class SentMessage:
    successfullySent: bool
    numberOfRetries: int
    exceptions: list[Exception] | None
    messageMethod: MessageMethod
    sendTime: SimpleDateTime
    msg: str
    twitchChannel: str
