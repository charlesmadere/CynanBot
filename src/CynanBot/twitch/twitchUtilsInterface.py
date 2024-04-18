from abc import abstractmethod

from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable
from CynanBot.twitch.twitchConstantsInterface import TwitchConstantsInterface


class TwitchUtilsInterface(TwitchConstantsInterface):

    @abstractmethod
    async def safeSend(
        self,
        messageable: TwitchMessageable,
        message: str | None,
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
