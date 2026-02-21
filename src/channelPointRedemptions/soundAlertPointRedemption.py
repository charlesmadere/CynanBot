from typing import Final

from .absChannelPointRedemption2 import AbsChannelPointRedemption2
from ..misc import utils as utils
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ..soundPlayerManager.soundAlert import SoundAlert
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChannelPointsRedemption import TwitchChannelPointsRedemption
from ..users.soundAlert.soundAlertRedemption import SoundAlertRedemption
from ..users.userInterface import UserInterface


class SoundAlertPointRedemption(AbsChannelPointRedemption2):

    def __init__(
        self,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
    ):
        if not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerManagerProvider: Final[SoundPlayerManagerProviderInterface] = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: Final[SoundPlayerRandomizerHelperInterface] = soundPlayerRandomizerHelper
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber

    async def __findSoundAlertRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
        user: UserInterface,
    ) -> SoundAlertRedemption | None:
        if not isinstance(TwitchChannelPointsRedemption, TwitchChannelPointsRedemption):
            raise TypeError(f'channelPointsRedemption argument is malformed: \"{channelPointsRedemption}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        soundAlertRedemptions = user.soundAlertRedemptions
        if soundAlertRedemptions is None or len(soundAlertRedemptions) == 0:
            return None

        return soundAlertRedemptions.get(channelPointsRedemption.rewardId, None)

    async def handlePointRedemption(
        self,
        channelPointsRedemption: TwitchChannelPointsRedemption,
    ) -> bool:
        user = channelPointsRedemption.twitchUser
        if not user.areSoundAlertsEnabled:
            return False

        isImmediate = False
        soundAlert: SoundAlert | None = None
        soundAlertRedemption: SoundAlertRedemption | None = None
        filePath: str | None = None

        if channelPointsRedemption.rewardId == user.randomSoundAlertRewardId:
            soundAlert = await self.__soundPlayerRandomizerHelper.chooseRandomSoundAlert()

        if soundAlert is None:
            soundAlertRedemption = await self.__findSoundAlertRedemption(
                channelPointsRedemption = channelPointsRedemption,
                user = user,
            )

        if soundAlertRedemption is not None:
            isImmediate = soundAlertRedemption.isImmediate

            if soundAlertRedemption.soundAlert is SoundAlert.RANDOM_FROM_DIRECTORY:
                filePath = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
                    directoryPath = soundAlertRedemption.directoryPath,
                )
            else:
                soundAlert = soundAlertRedemption.soundAlert

        if soundAlert is None and filePath is None:
            return False

        if isImmediate:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

            if utils.isValidStr(filePath):
                await soundPlayerManager.playSoundFile(filePath)
            elif soundAlert is not None:
                await soundPlayerManager.playSoundAlert(soundAlert)
        else:
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = soundAlert,
                twitchChannel = channelPointsRedemption.twitchChannel,
                twitchChannelId = channelPointsRedemption.twitchChannelId,
                ttsEvent = None,
            ))

        self.__timber.log('SoundAlertPointRedemption', f'Redeemed ({channelPointsRedemption=}) ({soundAlert=}) ({filePath=}) ({isImmediate=})')
        return True
