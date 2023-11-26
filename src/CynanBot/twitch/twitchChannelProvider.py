from abc import ABC, abstractmethod

from CynanBot.twitch.twitchChannel import TwitchChannel


class TwitchChannelProvider(ABC):

    @abstractmethod
    async def getTwitchChannel(twitchChannel: str) -> TwitchChannel:
        pass
