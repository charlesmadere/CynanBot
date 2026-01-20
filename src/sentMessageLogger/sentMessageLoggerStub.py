from typing import Collection

from .messageMethod import MessageMethod
from .sentMessageLoggerInterface import SentMessageLoggerInterface


class SentMessageLoggerStub(SentMessageLoggerInterface):

    def log(
        self,
        successfullySent: bool,
        exceptions: Collection[Exception] | None,
        numberOfSendAttempts: int,
        messageMethod: MessageMethod,
        msg: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass
