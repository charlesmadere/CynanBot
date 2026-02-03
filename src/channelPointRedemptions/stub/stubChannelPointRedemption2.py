from ..absChannelPointRedemption2 import AbsChannelPointRedemption2
from ...twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class StubChannelPointRedemption2(AbsChannelPointRedemption2):

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        # this method is intentionally empty
        return False
