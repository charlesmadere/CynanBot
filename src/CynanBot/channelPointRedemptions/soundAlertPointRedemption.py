import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.soundPlayerManager.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.immediateStreamAlertsManagerInterface import \
    ImmediateStreamAlertsManagerInterface
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.users.soundAlertRedemption import SoundAlertRedemption
from CynanBot.users.userInterface import UserInterface



class SoundAlertPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        immediateStreamAlertsManager: ImmediateStreamAlertsManagerInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface
    ):
        if not isinstance(immediateStreamAlertsManager, ImmediateStreamAlertsManagerInterface):
            raise TypeError(f'immediateStreamAlertsManager argument is malformed: \"{immediateStreamAlertsManager}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__immediateStreamAlertsManager: ImmediateStreamAlertsManagerInterface = immediateStreamAlertsManager
        self.__soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface = soundPlayerRandomizerHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager

    async def __findSoundAlertRedemption(
        self,
        twitchChannelPointsMessage: TwitchChannelPointsMessage,
        user: UserInterface
    ) -> SoundAlertRedemption | None:
        if not isinstance(twitchChannelPointsMessage, TwitchChannelPointsMessage):
            raise TypeError(f'twitchChannelPointsMessage argument is malformed: \"{twitchChannelPointsMessage}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        soundAlertRedemptions = user.getSoundAlertRedemptions()

        if soundAlertRedemptions is None or len(soundAlertRedemptions) == 0:
            return None

        return soundAlertRedemptions.get(twitchChannelPointsMessage.getRewardId(), None)

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        user = twitchChannelPointsMessage.getTwitchUser()

        if not user.areSoundAlertsEnabled():
            return False

        isImmediate = False
        soundAlert: SoundAlert | None = None
        soundAlertRedemption: SoundAlertRedemption | None = None
        filePath: str | None = None

        if twitchChannelPointsMessage.getRewardId() == user.getRandomSoundAlertRewardId():
            soundAlert = await self.__soundPlayerRandomizerHelper.chooseRandomSoundAlert()

        if soundAlert is None:
            soundAlertRedemption = await self.__findSoundAlertRedemption(
                twitchChannelPointsMessage = twitchChannelPointsMessage,
                user = user
            )

        if soundAlertRedemption is not None:
            isImmediate = soundAlertRedemption.isImmediate

            if soundAlertRedemption.soundAlert is SoundAlert.RANDOM_FROM_DIRECTORY:
                filePath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
                    directoryPath = soundAlertRedemption.directoryPath
                )
            else:
                soundAlert = soundAlertRedemption.soundAlert

        if soundAlert is None and filePath is None:
            return False

        if isImmediate:
            if utils.isValidStr(filePath):
                await self.__immediateStreamAlertsManager.playSoundFile(filePath)
            elif soundAlert is not None:
                await self.__immediateStreamAlertsManager.playSoundAlert(soundAlert)
        else:
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = soundAlert,
                twitchChannel = twitchChannel.getTwitchChannelName(),
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                ttsEvent = None
            ))

        return True
