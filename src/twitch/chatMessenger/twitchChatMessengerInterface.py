from abc import ABC, abstractmethod


class TwitchChatMessengerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submit(
        self,
        text: str,
        twitchChannelId: str,
        delaySeconds: int | None = None,
        replyMessageId: str | None = None,
    ):
        pass
