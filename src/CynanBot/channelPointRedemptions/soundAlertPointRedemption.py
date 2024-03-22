from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface


class SoundAlertPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        return False
