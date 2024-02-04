import traceback
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
        timber: TimberInterface
    ):
        if not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber

        self.__mediaPlayer: Optional[vlc.MediaPlayer] = None

    async def isPlaying(self) -> bool:
        mediaPlayer = self.__mediaPlayer
        return mediaPlayer is not None and mediaPlayer.is_playing()

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

        media: Optional[vlc.Media] = None
        exception: Optional[Exception] = None

        try:
            media = vlc.Media(filePath)
        except Exception as e:
            exception = e

        if media is None or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to load sound alert from file path: \"{filePath}\" ({alert=}) ({media=}) ({exception=})', exception, traceback.format_exc())
            return False

        mediaPlayer = await self.__retrieveMediaPlayer()
        playbackResult: Optional[int] = None

        try:
            playbackResult = mediaPlayer.play()
        except Exception as e:
            exception = e

        if playbackResult != 0 or exception is not None:
            self.__timber.log('VlcSoundPlayerManager', f'Failed to play sound alert ({alert=}) ({filePath=}) ({playbackResult=}) ({exception=})', exception, traceback.format_exc())
            return False

        self.__timber.log('VlcSoundPlayerManager', f'Started playing sound alert ({alert=}) ({filePath=}) ({media=}) ({playbackResult=})')
        return True

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    async def __retrieveMediaPlayer(self) -> vlc.MediaPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = vlc.MediaPlayer()
            self.__mediaPlayer = mediaPlayer
            self.__timber.log('VlcSoundPlayerManager', f'Created new vlc.MediaPlayer instance: \"{mediaPlayer}\"')

        if not isinstance(mediaPlayer, vlc.MediaPlayer):
            exception = RuntimeError(f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\"')
            self.__timber.log('VlcSoundPlayerManager', f'Failed to instantiate vlc.MediaPlayer: \"{mediaPlayer}\" ({exception=})', exception, traceback.format_exc())
            raise exception

        return mediaPlayer

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'mediaPlayer': self.__mediaPlayer
        }
