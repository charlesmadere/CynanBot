import random

import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.channelPoint.channelPointSoundHelperInterface import \
    ChannelPointSoundHelperInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface


class ChannelPointSoundHelper(ChannelPointSoundHelperInterface):

    def __init__(
        self,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        pointRedemptionSoundAlerts: set[SoundAlert] | None = {
            SoundAlert.POINT_REDEMPTION_01,
            SoundAlert.POINT_REDEMPTION_02,
            SoundAlert.POINT_REDEMPTION_03,
            SoundAlert.POINT_REDEMPTION_04,
            SoundAlert.POINT_REDEMPTION_05,
            SoundAlert.POINT_REDEMPTION_06,
            SoundAlert.POINT_REDEMPTION_07,
            SoundAlert.POINT_REDEMPTION_08,
            SoundAlert.POINT_REDEMPTION_09,
            SoundAlert.POINT_REDEMPTION_10,
            SoundAlert.POINT_REDEMPTION_11,
            SoundAlert.POINT_REDEMPTION_12,
            SoundAlert.POINT_REDEMPTION_13,
            SoundAlert.POINT_REDEMPTION_14,
            SoundAlert.POINT_REDEMPTION_15,
            SoundAlert.POINT_REDEMPTION_16
        }
    ):
        if not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif pointRedemptionSoundAlerts is not None and not isinstance(pointRedemptionSoundAlerts, set):
            raise TypeError(f'pointRedemptionSoundAlerts argument is malformed: \"{pointRedemptionSoundAlerts}\"')

        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__pointRedemptionSoundAlerts: set[SoundAlert] | None = pointRedemptionSoundAlerts

        self.__cache: dict[SoundAlert, str | None] | None = None

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('ChannelPointSoundHelper', 'Caches cleared')

    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        cache = self.__cache

        if cache is None:
            cache = await self.__loadSoundAlertsCache()
            self.__cache = cache

        availableSoundAlerts: list[SoundAlert] = list()

        for soundAlert, filePath in cache.items():
            if not utils.isValidStr(filePath):
                continue
            elif not await aiofiles.ospath.exists(filePath):
                continue

            availableSoundAlerts.append(soundAlert)

        if len(availableSoundAlerts) == 0:
            return None

        return random.choice(availableSoundAlerts)

    async def __loadSoundAlertsCache(self) -> dict[SoundAlert, str | None]:
        cache: dict[SoundAlert, str | None] = dict()

        if self.__pointRedemptionSoundAlerts is not None and len(self.__pointRedemptionSoundAlerts) >= 1:
            for soundAlert in self.__pointRedemptionSoundAlerts:
                filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(soundAlert)
                cache[soundAlert] = filePath

        self.__timber.log('ChannelPointSoundHelper', f'Finished loading in ({len(cache)}) sound alert(s)')
        return cache
