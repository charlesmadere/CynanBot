from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable


class TwitchUtilsInterface(ABC):

    @abstractmethod
    def getMaxMessageSize(self) -> int:
        pass

    @abstractmethod
    async def safeSend(
        self,
        messageable: TwitchMessageable,
        message: Optional[str],
        maxMessages: int = 3,
        perMessageMaxSize: int = 494
    ):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def waitThenSend(
        self,
        messageable: TwitchMessageable,
        delaySeconds: int,
        message: str
    ):
        pass
