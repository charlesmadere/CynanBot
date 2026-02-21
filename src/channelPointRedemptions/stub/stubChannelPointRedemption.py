from ..absChannelPointRedemption import AbsChannelPointRedemption
from ...twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption


class StubChannelPointRedemption(AbsChannelPointRedemption):

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        # this method is intentionally empty
        return False
