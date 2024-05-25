from abc import ABC, abstractmethod

from CynanBot.twitch.timeout.twitchTimeoutRemodData import \
    TwitchTimeoutRemodData


class TwitchTimeoutRemodHelperInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def submitRemodData(self, data: TwitchTimeoutRemodData):
        pass
