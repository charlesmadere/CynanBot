import traceback
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any, Dict, Optional

import aiofiles.ospath
import vlc

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerManagerInterface import \
    SoundPlayerManagerInterface
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface


class VlcSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        soundAlertBufferMillis: int = 100,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(soundAlertBufferMillis):
            raise TypeError(f'soundAlertBufferMillis argument is malformed: \"{soundAlertBufferMillis}\"')
        elif soundAlertBufferMillis < 0 or soundAlertBufferMillis > 3000:
            raise ValueError(f'soundAlertBufferMillis argument is out of bounds: {soundAlertBufferMillis}')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__soundAlertBufferMillis: int = soundAlertBufferMillis
        self.__timeZone: tzinfo = timeZone

        self.__currentSoundEndTime: Optional[datetime] = None

    async def isPlaying(self) -> bool:
        currentSoundEndTime = self.__currentSoundEndTime

        if currentSoundEndTime is None:
            return False

        now = datetime.now(self.__timeZone)
        return currentSoundEndTime <= now

    async def playSoundAlert(self, alert: SoundAlert) -> bool:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound alert!')
            return False

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(alert)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for sound alert \"{alert}\" ({filePath=})')
            return False
        elif not await aiofiles.ospath.exists(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'Sound alert\'s (\"{alert}\") file path does not exist ({filePath=})')
            return False
        elif not await aiofiles.ospath.isfile(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'Sound alert\'s (\"{alert}\") file path is not a file ({filePath=})')
            return False

        exception: Optional[Exception] = None
        mediaPlayer: Optional[vlc.MediaPlayer] = None

        try:
            mediaPlayer = vlc.MediaPlayer(filePath)
        except Exception as e:
            exception = e

        if mediaPlayer is None or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to load sound alert (\"{alert}\") with file path \"{filePath}\": {exception}', exception, traceback.format_exc())
            return False

        now = datetime.now(self.__timeZone)
        durationMillis = mediaPlayer.get_length() + self.__soundAlertBufferMillis
        self.__currentSoundEndTime = now + timedelta(milliseconds = durationMillis)

        try:
            mediaPlayer.play()
        except Exception as e:
            exception = e

        if exception is None:
            self.__timber.log('VlcSoundPlayerManager', f'Started playing sound alert (\"{alert}\") ({filePath=}) ({durationMillis=})')
            return True
        else:
            self.__timber.log('VlcSoundPlayerManager', f'Attempted to play sound alert (\"{alert}\") ({filePath=}) ({durationMillis=}) but encountered an exception: {exception}', exception, traceback.format_exc())
            return False

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'currentSoundEndTime': self.__currentSoundEndTime
        }
