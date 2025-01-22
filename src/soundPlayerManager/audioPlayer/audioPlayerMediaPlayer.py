import time
import traceback
from datetime import datetime, timedelta
from threading import Thread

import aiofiles.ospath
import librosa
from audioplayer import AudioPlayer

from .audioPlayerPlaybackTask import AudioPlayerPlaybackTask
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        playbackLoopSleepTimeSeconds: float = 0.125
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.125 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__playbackLoopSleepTimeSeconds: float = playbackLoopSleepTimeSeconds

        self.__isPlayingOrLoading: bool = False
        self.__volume: int = 100
        self.__filePath: str | None = None
        self.__playbackTask: AudioPlayerPlaybackTask | None = None

    @property
    def isPlaying(self) -> bool:
        return self.__isPlayingOrLoading or self.__playbackTask is not None

    async def play(self) -> bool:
        self.__isPlayingOrLoading = True
        filePath = self.__filePath

        if not utils.isValidStr(filePath):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath has not yet been set ({filePath=})')
            return False
        elif not await aiofiles.ospath.exists(filePath):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath does not point to a file that exists ({filePath=})')
            return False
        elif await aiofiles.ospath.isdir(filePath):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath points to a directory instead of a file ({filePath=})')
            return False

        try:
            durationSeconds = librosa.get_duration(filename = filePath)
        except Exception as e:
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to determine duration seconds ({filePath=}): {e}', e, traceback.format_exc())
            return False

        playbackTask = AudioPlayerPlaybackTask(
            durationSeconds = durationSeconds,
            volume = self.__volume,
            filePath = filePath
        )

        try:
            audioPlayer = AudioPlayer(filename = playbackTask.filePath)
        except Exception as e:
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to create new AudioPlayer instance ({playbackTask=}): {e}', e, traceback.format_exc())
            return False

        playbackThread = Thread(
            target = self.__play,
            args = ( audioPlayer, playbackTask, )
        )

        self.__playbackTask = playbackTask
        playbackThread.start()

        return True

    def __play(
        self,
        audioPlayer: AudioPlayer,
        task: AudioPlayerPlaybackTask
    ):
        if not isinstance(audioPlayer, AudioPlayer):
            raise TypeError(f'audioPlayer argument is malformed: \"{audioPlayer}\"')
        elif not isinstance(task, AudioPlayerPlaybackTask):
            raise TypeError(f'task argument is malformed: \"{task}\"')

        audioPlayer.volume = task.volume

        audioPlayer.play(
            loop = False,
            block = False
        )

        isStillPlaying = True
        timeZone = self.__timeZoneRepository.getDefault()
        endTime = datetime.now(timeZone) + timedelta(seconds = task.durationSeconds)

        while isStillPlaying and not task.isCanceled:
            if task.isCanceled:
                continue

            now = datetime.now(timeZone)

            if now >= endTime:
                isStillPlaying = False
            else:
                time.sleep(self.__playbackLoopSleepTimeSeconds)

        if task.isCanceled:
            audioPlayer.stop()

        self.__playbackTask = None
        self.__isPlayingOrLoading = False

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
        if not self.isPlaying:
            return

        playbackTask = self.__playbackTask

        if playbackTask is not None:
            playbackTask.cancel()
