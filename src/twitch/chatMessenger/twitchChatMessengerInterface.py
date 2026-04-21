from abc import ABC, abstractmethod

from ...misc.startable import Startable


class TwitchChatMessengerInterface(Startable, ABC):

    @abstractmethod
    def send(
        self,
        text: str,
        twitchChannelId: str,
        delaySeconds: int | None = None,
        replyMessageId: str | None = None,
    ):
        pass
