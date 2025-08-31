from abc import ABC, abstractmethod


class TwitchChatMessengerInterface(ABC):

    @abstractmethod
    def send(
        self,
        text: str,
        twitchChannelId: str,
        delaySeconds: int | None = None,
        replyMessageId: str | None = None,
    ):
        pass

    @abstractmethod
    def start(self):
        pass
