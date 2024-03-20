from abc import ABC, abstractmethod


class SentMessageLoggerInterface(ABC):

    @abstractmethod
    def log(
        self,
        successfullySent: bool,
        usedTwitchApi: bool,
        numberOfRetries: int,
        exceptions: list[Exception] | None,
        msg: str,
        twitchChannel: str
    ):
        pass

    @abstractmethod
    def start(self):
        pass
