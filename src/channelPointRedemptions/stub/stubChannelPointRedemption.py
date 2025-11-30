from ..absChannelPointRedemption import AbsChannelPointRedemption
from ...twitch.configuration.twitchChannel import TwitchChannel
from ...twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage


class StubPointRedemption(AbsChannelPointRedemption):

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
    ) -> bool:
        # this method is intentionally empty
        return False
