from abc import ABC, abstractmethod

from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class AbsChannelPointRedemption(ABC):

    @abstractmethod
    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        pass
