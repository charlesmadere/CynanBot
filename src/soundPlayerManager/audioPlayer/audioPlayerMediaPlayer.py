import asyncio
import traceback

from audioplayer import AudioPlayer

from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber

        self.__isPlaying: bool = False
        self.__volume: int = 100
        self.__filePath: str | None = None
        self.__playbackTask: asyncio.Task | None = None

    @property
    def isPlaying(self) -> bool:
        return self.__isPlaying

    async def play(self) -> bool:
        self.__isPlaying = True
        filePath = self.__filePath

        if not utils.isValidStr(filePath):
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath has not been set yet ({filePath=})')
            return False

        try:
            audioPlayer = AudioPlayer(filename = self.__filePath)
        except Exception as e:
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to create new AudioPlayer instance ({filePath=}): {e}', e, traceback.format_exc())
            return False

        audioPlayer.volume = self.__volume

        async def __play():
            audioPlayer.play(
                loop = False,
                block = True
            )

            self.__isPlaying = False
            self.__playbackTask = None

        self.__playbackTask = asyncio.create_task(
            coro = __play(),
            name = f'AudioPlayerMediaPlayer:{filePath}'
        )

        return True

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
        playbackTask = self.__playbackTask

        if playbackTask is None:
            return

        playbackTask.cancel()
        self.__playbackTask = None
        playbackTask = None
        self.__isPlaying = False
