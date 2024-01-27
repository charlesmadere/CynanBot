import traceback
from typing import Optional

import aiofiles.ospath
import vlc

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundPlayerInterface import \
    SoundPlayerInterface
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface
from CynanBot.soundPlayerHelper.soundReferenceStub import SoundReferenceStub
from CynanBot.soundPlayerHelper.vlcSoundPlayer.vlcSoundReference import \
    VlcSoundReference
from CynanBot.timber.timberInterface import TimberInterface


class VlcSoundPlayer(SoundPlayerInterface):

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

    async def load(self, filePath: str) -> SoundReferenceInterface:
        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayer', f'filePath argument is invalid: \"{filePath}\"')

            return SoundReferenceStub(
                filePath = filePath,
                timber = self.__timber
            )
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return SoundReferenceStub(
                filePath = filePath,
                timber = self.__timber
            )
        elif not await aiofiles.ospath.exists(filePath):
            self.__timber.log('VlcSoundPlayer', f'File for filePath does not exist: \"{filePath}\"')

            return SoundReferenceStub(
                filePath = filePath,
                timber = self.__timber
            )
        elif not await aiofiles.ospath.isfile(filePath):
            self.__timber.log('VlcSoundPlayer', f'File for filePath is not a file: \"{filePath}\"')

            return SoundReferenceStub(
                filePath = filePath,
                timber = self.__timber
            )

        exception: Optional[Exception] = None
        mediaPlayer: Optional[vlc.MediaPlayer] = None

        try:
            mediaPlayer = vlc.MediaPlayer(filePath)
        except Exception as e:
            exception = e

        if mediaPlayer is None or exception is not None:
            self.__timber.log('VlcSoundPlayer', f'Failed to load sound with filePath \"{filePath}\": {exception}', exception, traceback.format_exc())

            return SoundReferenceStub(
                filePath = filePath,
                timber = self.__timber
            )
        else:
            return VlcSoundReference(
                filePath = filePath,
                timber = self.__timber,
                mediaPlayer = mediaPlayer
            )
