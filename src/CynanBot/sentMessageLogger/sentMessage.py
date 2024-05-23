from dataclasses import dataclass

from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.sentMessageLogger.messageMethod import MessageMethod


@dataclass(frozen = True)
class SentMessage():
    successfullySent: bool
    numberOfRetries: int
    exceptions: list[Exception] | None
    messageMethod: MessageMethod
    sendTime: SimpleDateTime
    msg: str
    twitchChannel: str
