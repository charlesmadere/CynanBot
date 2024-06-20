import random
import re
from typing import Pattern

import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.soundPlayerManager.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface


class SoundPlayerRandomizerHelper(SoundPlayerRandomizerHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
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
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif pointRedemptionSoundAlerts is not None and not isinstance(pointRedemptionSoundAlerts, set):
            raise TypeError(f'pointRedemptionSoundAlerts argument is malformed: \"{pointRedemptionSoundAlerts}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__pointRedemptionSoundAlerts: set[SoundAlert] | None = pointRedemptionSoundAlerts

        self.__cache: dict[SoundAlert, str | None] | None = None
        self.__soundFileRegEx: Pattern = re.compile(r'^[^.].+\.(mp3|ogg|wav)$', re.IGNORECASE)

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('SoundPlayerRandomizerHelper', 'Caches cleared')

    async def chooseRandomFromDirectorySoundAlert(
        self,
        directoryPath: str | None
    ) -> str | None:
        if not utils.isValidStr(directoryPath):
            return None

        directoryPath = utils.cleanPath(directoryPath)

        if not await aiofiles.ospath.exists(
            path = directoryPath,
            loop = self.__backgroundTaskHelper.getEventLoop()
        ):
            self.__timber.log('SoundPlayerRandomizerHelper', f'The given directory path does not exist: \"{directoryPath}\"')
            return None
        elif not await aiofiles.ospath.isdir(
            s = directoryPath,
            loop = self.__backgroundTaskHelper.getEventLoop()
        ):
            self.__timber.log('SoundPlayerRandomizerHelper', f'The given directory path is not a directry: \"{directoryPath}\"')
            return None

        directoryContents = await aiofiles.os.scandir(
            path = directoryPath,
            loop = self.__backgroundTaskHelper.getEventLoop()
        )

        if directoryContents is None:
            self.__timber.log('SoundPlayerRandomizerHelper', f'Failed to scan the given directory path: \"{directoryPath}\"')
            return None

        soundFiles: list[str] = list()

        for entry in directoryContents:
            if not entry.is_file():
                continue
            elif self.__soundFileRegEx.fullmatch(entry.name) is None:
                continue

            cleanedPath = utils.cleanPath(entry.name)
            soundFiles.append(cleanedPath)

        directoryContents.close()

        if len(soundFiles) == 0:
            self.__timber.log('SoundPlayerRandomizerHelper', f'Scanned the given directory path but found no sound files: \"{directoryPath}\"')
            return None

        return random.choice(soundFiles)

    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        cache = self.__cache

        if cache is None:
            cache = await self.__loadSoundAlertsCache()
            self.__cache = cache

        availableSoundAlerts: list[SoundAlert] = list()

        for soundAlert, filePath in cache.items():
            if not utils.isValidStr(filePath):
                continue
            elif not await aiofiles.ospath.exists(
                path = filePath,
                loop = self.__backgroundTaskHelper.getEventLoop()
            ):
                continue
            elif not await aiofiles.ospath.isfile(
                path = filePath,
                loop = self.__backgroundTaskHelper.getEventLoop()
            ):
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

        self.__timber.log('SoundPlayerRandomizerHelper', f'Finished loading in ({len(cache)}) sound alert(s)')
        return cache
