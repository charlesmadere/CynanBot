from abc import ABC, abstractmethod

from .twitchChannel import TwitchChannel


class TwitchChannelProvider(ABC):

    @abstractmethod
    async def getTwitchChannel(self, twitchChannel: str) -> TwitchChannel:
        pass
