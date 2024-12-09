from enum import Enum, auto

import vlc

from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class VlcMediaPlayer:

    class PlaybackState(Enum):

        ERROR = auto()
        PLAYING = auto()
        STOPPED = auto()

        @classmethod
        def fromVlcState(cls, state: vlc.State):
            if not isinstance(state, vlc.State):
                return VlcMediaPlayer.PlaybackState.ERROR

            # VLC State documentation:
            # 0 is "NothingSpecial"
            # 1 is "Opening"
            # 2 is "Buffering"
            # 3 is "Playing"
            # 4 is "Paused"
            # 5 is "Stopped"
            # 6 is "Ended"
            # 7 is "Error"

            match state:
                case 0: return VlcMediaPlayer.PlaybackState.STOPPED
                case 1: return VlcMediaPlayer.PlaybackState.PLAYING
                case 2: return VlcMediaPlayer.PlaybackState.PLAYING
                case 3: return VlcMediaPlayer.PlaybackState.PLAYING
                case 4: return VlcMediaPlayer.PlaybackState.STOPPED
                case 5: return VlcMediaPlayer.PlaybackState.STOPPED
                case 6: return VlcMediaPlayer.PlaybackState.STOPPED
                case 7: return VlcMediaPlayer.PlaybackState.ERROR
                case _: raise ValueError(f'Encountered unexpected vlc.State value: \"{state}\"')

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__mediaPlayer: vlc.MediaPlayer = vlc.MediaPlayer()

    @property
    def isPlaying(self) -> bool:
        return self.__mediaPlayer.is_playing() == 1

    async def play(self) -> bool:
        result = self.__mediaPlayer.play()

        if result == 0:
            return True
        else:
            self.__timber.log('VlcMediaPlayer', f'Attempted to play, but received an unexpected result code: {result}')
            return False

    @property
    def playbackState(self) -> PlaybackState:
        vlcState = self.__mediaPlayer.get_state()
        return VlcMediaPlayer.PlaybackState.fromVlcState(vlcState)

    async def setMedia(self, filePath: str):
        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__mediaPlayer.set_media(vlc.Media(filePath))

    async def setVolume(self, volume: int) -> bool:
        if not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100

        result = self.__mediaPlayer.audio_set_volume(volume)

        if result == 0:
            return True
        else:
            self.__timber.log('VlcMediaPlayer', f'Attempted to set volume to {volume}, but received an unexpected result code: {result}')
            return False

    async def stop(self):
        self.__mediaPlayer.stop()

    @property
    def volume(self) -> int:
        return self.__mediaPlayer.audio_get_volume()
