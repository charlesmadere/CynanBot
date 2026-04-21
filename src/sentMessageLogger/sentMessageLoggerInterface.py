from abc import ABC, abstractmethod
from typing import Collection

from .messageMethod import MessageMethod
from ..misc.startable import Startable


class SentMessageLoggerInterface(Startable, ABC):

    @abstractmethod
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
        pass
