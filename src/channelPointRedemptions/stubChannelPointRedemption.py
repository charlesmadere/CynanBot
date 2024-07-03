from .absChannelPointRedemption import AbsChannelPointRedemption
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage


class StubPointRedemption(AbsChannelPointRedemption):

    def __init__(self):
        pass

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        return False
