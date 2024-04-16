from abc import ABC, abstractmethod

from CynanBot.twitch.twitchTimeoutRemodData import TwitchTimeoutRemodData


class TwitchTimeoutRemodHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def submitRemodData(self, action: TwitchTimeoutRemodData):
        pass
