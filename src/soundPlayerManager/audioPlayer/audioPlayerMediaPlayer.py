from audioplayer import AudioPlayer

from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__audioPlayer: AudioPlayer | None = None
        self.__isPlaying: bool = False
        self.__volume: int = 100
        self.__filePath: str | None = None

    @property
    def isPlaying(self) -> bool:
        audioPlayer = self.__audioPlayer
        return audioPlayer is not None and self.__isPlaying

    async def play(self):
        self.__isPlaying = True
        filePath = self.__filePath

        if not utils.isValidStr(filePath):
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath has not been set yet ({filePath=})')
            return

        try:
            audioPlayer = AudioPlayer(
                filename = self.__filePath
            )
        except Exception as e:
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to create new AudioPlayer instance ({filePath=}): {e}', e)
            return

        self.__audioPlayer = audioPlayer
        audioPlayer.volume = self.__volume

        audioPlayer.play(
            loop = False,
            block = True
        )

        self.__isPlaying = False

    async def setMedia(self, filePath: str):
        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__filePath = filePath

    async def setVolume(self, volume: int):
        if not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if volume < 0:
            self.__timber.log('AudioPlayerMediaPlayer', f'The given volume parameter was too small and has been coerced to 0 ({volume=})')
            volume = 0
        elif volume > 100:
            self.__timber.log('AudioPlayerMediaPlayer', f'The given volume parameter was too large and has been coerced to 100 ({volume=})')
            volume = 100

        self.__volume = volume

    async def stop(self):
        audioPlayer = self.__audioPlayer

        if audioPlayer is not None:
            audioPlayer.stop()
            self.__isPlaying = False
