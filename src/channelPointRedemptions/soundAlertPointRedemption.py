from typing import Final

from .absChannelPointsRedemption2 import AbsChannelPointRedemption2
from .pointsRedemptionResult import PointsRedemptionResult
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
        pointsRedemption: TwitchChannelPointsRedemption,
        user: UserInterface,
    ) -> SoundAlertRedemption | None:
        soundAlertRedemptions = user.soundAlertRedemptions
        if soundAlertRedemptions is None or len(soundAlertRedemptions) == 0:
            return None

        return soundAlertRedemptions.get(pointsRedemption.rewardId, None)

    async def handlePointsRedemption(
        self,
        pointsRedemption: TwitchChannelPointsRedemption,
    ) -> PointsRedemptionResult:
        user = pointsRedemption.twitchUser
        if not user.areSoundAlertsEnabled:
            return PointsRedemptionResult.IGNORED

        isImmediate = False
        soundAlert: SoundAlert | None = None
        soundAlertRedemption: SoundAlertRedemption | None = None
        filePath: str | None = None

        if pointsRedemption.rewardId == user.randomSoundAlertRewardId:
            soundAlert = await self.__soundPlayerRandomizerHelper.chooseRandomSoundAlert()

        if soundAlert is None:
            soundAlertRedemption = await self.__findSoundAlertRedemption(
                pointsRedemption = pointsRedemption,
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
            return PointsRedemptionResult.IGNORED

        if isImmediate:
            soundPlayerManager = self.__soundPlayerManagerProvider.constructNewInstance()

            if utils.isValidStr(filePath):
                await soundPlayerManager.playSoundFile(filePath)
            elif soundAlert is not None:
                await soundPlayerManager.playSoundAlert(soundAlert)
        else:
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = soundAlert,
                twitchChannel = pointsRedemption.twitchChannel,
                twitchChannelId = pointsRedemption.twitchChannelId,
                ttsEvent = None,
            ))

        self.__timber.log(self.pointsRedemptionName, f'Redeemed ({isImmediate=}) ({filePath=}) ({soundAlert=}) ({pointsRedemption=})')
        return PointsRedemptionResult.CONSUMED

    @property
    def pointsRedemptionName(self) -> str:
        return 'SoundAlertPointRedemption'

    def relevantRewardIds(
        self,
        twitchUser: UserInterface,
    ) -> frozenset[str]:
        rewardIds: set[str] = set()

        randomSoundAlertRewardId = twitchUser.randomSoundAlertRewardId
        if utils.isValidStr(randomSoundAlertRewardId):
            rewardIds.add(randomSoundAlertRewardId)

        soundAlertRedemptions = twitchUser.soundAlertRedemptions
        if soundAlertRedemptions is not None and len(soundAlertRedemptions) >= 1:
            rewardIds.update(soundAlertRedemptions.keys())

        return frozenset(rewardIds)
