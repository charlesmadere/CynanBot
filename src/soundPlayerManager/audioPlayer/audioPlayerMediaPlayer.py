import asyncio
import traceback

import aiofiles.ospath
import librosa
from audioplayer import AudioPlayer

from .audioPlayerPlaybackTask import AudioPlayerPlaybackTask
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        playbackLoopSleepTimeSeconds: float = 0.25
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.125 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__playbackLoopSleepTimeSeconds: float = playbackLoopSleepTimeSeconds

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
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath has not yet been set ({filePath=})')
            return False
        elif not await aiofiles.ospath.exists(filePath):
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath does not point to a file that exists ({filePath=})')
            return False

        try:
            durationSeconds = librosa.get_duration(filename = filePath)
        except Exception as e:
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to determine duration seconds ({filePath=}): {e}', e, traceback.format_exc())
            return False

        # TODO
        task = AudioPlayerPlaybackTask(
            durationSeconds = durationSeconds,
            volume = self.__volume,
            filePath = filePath
        )

        try:
            audioPlayer = AudioPlayer(filename = task.filePath)
        except Exception as e:
            self.__isPlaying = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to create new AudioPlayer instance ({task=}): {e}', e, traceback.format_exc())
            return False

        audioPlayer.volume = task.volume

        async def __play():
            audioPlayer.play(
                loop = False,
                block = True
            )

            self.__isPlaying = False
            self.__playbackTask = None

        self.__playbackTask = asyncio.create_task(
            coro = __play(),
            name = f'AudioPlayerMediaPlayer:{task}'
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
