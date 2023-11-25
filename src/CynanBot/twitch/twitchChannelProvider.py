from abc import ABC, abstractmethod

from twitch.twitchChannel import TwitchChannel


class TwitchChannelProvider(ABC):

    @abstractmethod
    async def getTwitchChannel(twitchChannel: str) -> TwitchChannel:
        pass
