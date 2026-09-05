from abc import ABC, abstractmethod
from typing import Collection

from ..misc.startable import Startable


class SentMessageLoggerInterface(Startable, ABC):

    @abstractmethod
    def log(
        self,
        successfullySent: bool,
        exceptions: Collection[Exception] | None,
        numberOfSendAttempts: int,
        msg: str,
        twitchChannel: str,
        twitchChannelId: str,
    ):
        pass
