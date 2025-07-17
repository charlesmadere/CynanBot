from abc import ABC, abstractmethod

from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class AbsChannelPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        pass
