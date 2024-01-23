import aiofiles.ospath
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.vlcHelper.vlcHelperInterface import VlcHelperInterface


class SoundPlayerHelper(SoundPlayerHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        vlcHelper: Optional[VlcHelperInterface]
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif vlcHelper is not None and not isinstance(vlcHelper, VlcHelperInterface):
            raise TypeError(f'vlcHelper argument is malformed: \"{vlcHelper}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__vlcHelper: Optional[VlcHelperInterface] = vlcHelper

    async def play(self, soundAlert: SoundAlert):
        if not isinstance(soundAlert, SoundAlert):
            raise ValueError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        if self.__vlcHelper is None:
            return

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(soundAlert)

        if not utils.isValidStr(filePath):
            return

        if not await aiofiles.ospath.exists(filePath):
            self.__timber.log('SoundPlayerHelper', f'File for sound alert {soundAlert} does not exist ({filePath=})')
            return
        elif not await aiofiles.ospath.isfile(filePath):
            self.__timber.log('SoundPlayerHelper', f'File for sound alert {soundAlert} is not a file ({filePath=})')
            return

        self.__timber.log('SoundPlayerHelper', f'Playing sound alert {soundAlert} ({filePath=})...')
        await self.__vlcHelper.play(filePath)
