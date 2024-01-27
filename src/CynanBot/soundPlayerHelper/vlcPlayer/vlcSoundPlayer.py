from CynanBot.soundPlayerHelper.soundPlayerInterface import SoundPlayerInterface
import traceback
from typing import Optional
import CynanBot.misc.utils as utils
import vlc
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.soundPlayerHelper.soundReferenceStub import SoundReferenceStub
from CynanBot.soundPlayerHelper.soundReferenceInterface import SoundReferenceInterface
from CynanBot.soundPlayerHelper.vlcPlayer.vlcSoundReference import VlcSoundReference


class VlcSoundPlayer(SoundPlayerInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def load(self, filePath: str) -> SoundReferenceInterface:
        if not utils.isValidStr(filePath):
            self.__timber.log('VlcHelper', f'filePath argument is invalid: \"{filePath}\"')

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
