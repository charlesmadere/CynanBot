import traceback
from typing import Optional

import vlc

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundReferenceInterface import \
    SoundReferenceInterface
from CynanBot.timber.timberInterface import TimberInterface


class VlcSoundReference(SoundReferenceInterface):

    def __init__(
        self,
        filePath: str,
        timber: TimberInterface,
        mediaPlayer: vlc.MediaPlayer
    ):
        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif mediaPlayer is None:
            raise TypeError(f'mediaPlayer argument is malformed: \"{mediaPlayer}\"')

        self.__filePath: str = filePath
        self.__timber: TimberInterface = timber
        self.__mediaPlayer: vlc.MediaPlayer = mediaPlayer

        self.__durationMillis: Optional[int] = None

    async def getDurationMillis(self) -> int:
        durationMillis = self.__durationMillis

        if not utils.isValidInt(durationMillis):
            try:
                durationMillis = int(round(self.__mediaPlayer.get_length()))
            except Exception as e:
                self.__timber.log('VlcSoundReference', f'Attempted to determine media duration millis using VLC ({self.__filePath=}) but encountered an exception: {e}', e, traceback.format_exc())

            if utils.isValidInt(durationMillis):
                durationMillis = max(0, durationMillis)
            else:
                durationMillis = 0

            self.__durationMillis = durationMillis

        return durationMillis

    async def play(self):
        exception: Optional[Exception] = None

        try:
            self.__mediaPlayer.play()
        except Exception as e:
            exception = e

        if exception is None:
            self.__timber.log('VlcSoundReference', f'Played media using VLC ({self.__filePath=})')
        else:
            self.__timber.log('VlcSoundReference', f'Attempted to play media using VLC ({self.__filePath=}) but encountered an exception: {exception}', exception, traceback.format_exc())
