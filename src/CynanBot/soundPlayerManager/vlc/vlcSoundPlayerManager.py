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

    async def __calculateMediaDurationMillis(
        self,
        alert: SoundAlert,
        filePath: str,
        mediaPlayer: vlc.MediaPlayer
    ) -> int:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')
        elif not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif not isinstance(mediaPlayer, vlc.MediaPlayer):
            raise TypeError(f'mediaPlayer argument is malformed: \"{mediaPlayer}\"')

        mediaLengthMillis: Optional[float] = None
        exception: Optional[Exception] = None

        try:
            mediaLengthMillis = mediaPlayer.get_length()
        except Exception as e:
            exception = e

        if not utils.isValidNum(mediaLengthMillis) or mediaLengthMillis <= 0 or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Unable to determine playback duration of alert ({alert=}) ({filePath=}) ({mediaLengthMillis=}) ({exception=})', exception, traceback.format_exc())
            return utils.getIntMinSafeSize()

        return int(round(mediaLengthMillis)) + self.__soundAlertBufferMillis

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
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for sound alert ({alert=}) ({filePath=})')
            return False
        elif not await aiofiles.ospath.exists(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'Sound alert\'s file path does not exist ({alert=}) ({filePath=})')
            return False
        elif not await aiofiles.ospath.isfile(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'Sound alert\'s file path is not a file ({alert=}) ({filePath=})')
            return False

        exception: Optional[Exception] = None
        mediaPlayer: Optional[vlc.MediaPlayer] = None

        try:
            mediaPlayer = vlc.MediaPlayer(filePath)
        except Exception as e:
            exception = e

        if mediaPlayer is None or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to load sound alert from file path: \"{filePath}\" ({alert=}) ({exception=})', exception, traceback.format_exc())
            return False

        playbackResult: Optional[int] = None

        try:
            playbackResult = mediaPlayer.play()
        except Exception as e:
            exception = e

        if playbackResult != 0 or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to play sound alert ({alert=}) ({filePath=}) ({playbackResult=}) ({exception=})', exception, traceback.format_exc())
            return False

        durationMillis = await self.__calculateMediaDurationMillis(
            alert = alert,
            filePath = filePath,
            mediaPlayer = mediaPlayer
        )

        if durationMillis < 1:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to determine sound alert\'s duration, or its duration is 0 ({alert=}) ({filePath=}) ({playbackResult=}) ({durationMillis=})')
            return False

        now = datetime.now(self.__timeZone)
        self.__currentSoundEndTime = now + timedelta(milliseconds = durationMillis)
        self.__timber.log('VlcSoundPlayerManager', f'Started playing sound alert ({alert=}) ({filePath=}) ({playbackResult=}) ({durationMillis=}) ({self.__currentSoundEndTime})')

        return True

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'currentSoundEndTime': self.__currentSoundEndTime
        }
