from abc import ABC, abstractmethod

from CynanBot.sentMessageLogger.messageMethod import MessageMethod


class SentMessageLoggerInterface(ABC):

    @abstractmethod
    def log(
        self,
        successfullySent: bool,
        numberOfRetries: int,
        exceptions: list[Exception] | None,
        messageMethod: MessageMethod,
        msg: str,
        twitchChannel: str
    ):
        pass

    @abstractmethod
    def start(self):
        pass
