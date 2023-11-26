from abc import ABC, abstractmethod
from typing import List, Optional


class SentMessageLoggerInterface(ABC):

    @abstractmethod
    def log(
        self,
        successfullySent: bool,
        numberOfRetries: int,
        exceptions: Optional[List[Exception]],
        msg: str,
        twitchChannel: str
    ):
        pass
