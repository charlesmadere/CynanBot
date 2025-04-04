from abc import ABC, abstractmethod
from typing import Collection

from .messageMethod import MessageMethod


class SentMessageLoggerInterface(ABC):

    @abstractmethod
    def log(
        self,
        successfullySent: bool,
        exceptions: Collection[Exception] | None,
        numberOfRetries: int,
        messageMethod: MessageMethod,
        msg: str,
        twitchChannel: str
    ):
        pass

    @abstractmethod
    def start(self):
        pass
