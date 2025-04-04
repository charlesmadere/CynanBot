from dataclasses import dataclass
from typing import Collection

from .messageMethod import MessageMethod
from ..misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class SentMessage:
    successfullySent: bool
    exceptions: Collection[Exception] | None
    numberOfRetries: int
    messageMethod: MessageMethod
    sendTime: SimpleDateTime
    msg: str
    twitchChannel: str
