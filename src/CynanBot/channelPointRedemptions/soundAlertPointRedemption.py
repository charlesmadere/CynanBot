from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.soundPlayerManager.channelPoint.channelPointSoundHelperInterface import \
    ChannelPointSoundHelperInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage


class SoundAlertPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        channelPointSoundHelper: ChannelPointSoundHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface
    ):
        if not isinstance(channelPointSoundHelper, ChannelPointSoundHelperInterface):
            raise TypeError(f'channelPointSoundHelper argument is malformed: \"{channelPointSoundHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__channelPointSoundHelper: ChannelPointSoundHelperInterface = channelPointSoundHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager

    async def __determineSoundAlert(
        self,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> SoundAlert | None:
        if not isinstance(twitchChannelPointsMessage, TwitchChannelPointsMessage):
            raise TypeError(f'twitchChannelPointsMessage argument is malformed: \"{twitchChannelPointsMessage}\"')

        user = twitchChannelPointsMessage.getTwitchUser()

        if twitchChannelPointsMessage.getRewardId() == user.getRandomSoundAlertRewardId():
            return await self.__channelPointSoundHelper.chooseRandomSoundAlert()

        soundAlertRedemptions = user.getSoundAlertRedemptions()
        if soundAlertRedemptions is None or len(soundAlertRedemptions) == 0:
            return None

        soundAlertRedemption = soundAlertRedemptions.get(twitchChannelPointsMessage.getRewardId(), None)
        if soundAlertRedemption is None:
            return None

        return soundAlertRedemption.getSoundAlert()

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        user = twitchChannelPointsMessage.getTwitchUser()
        if not user.areSoundAlertsEnabled():
            return False

        soundAlert = await self.__determineSoundAlert(
            twitchChannelPointsMessage = twitchChannelPointsMessage
        )

        if soundAlert is None:
            return False

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = soundAlert,
            twitchChannel = twitchChannel.getTwitchChannelName(),
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            ttsEvent = None
        ))

        return True
