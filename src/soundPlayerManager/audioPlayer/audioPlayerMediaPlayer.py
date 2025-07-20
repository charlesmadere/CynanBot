import time
import traceback
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta
from threading import Thread
from typing import Any, Final

import aiofiles.ospath
import librosa
from audioplayer import AudioPlayer

from .audioPlayerPlaybackTask import AudioPlayerPlaybackTask
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class AudioPlayerMediaPlayer:

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        playbackLoopSleepTimeSeconds: float = 0.125,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.125 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__playbackLoopSleepTimeSeconds: Final[float] = playbackLoopSleepTimeSeconds

        self.__playbackTask: AudioPlayerPlaybackTask | None = None
        self.__isPlayingOrLoading: bool = False
        self.__volume: int = 100
        self.__filePath: str | None = None

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
        elif not await aiofiles.ospath.exists(
            path = filePath,
            loop = self.__eventLoop
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath does not point to a file that exists ({filePath=})')
            return False
        elif await aiofiles.ospath.isdir(
            s = filePath,
            loop = self.__eventLoop
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath points to a directory instead of a file ({filePath=})')
            return False
        elif not await aiofiles.ospath.isfile(
            path = filePath,
            loop = self.__eventLoop
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but filePath points to something that is not a file ({filePath=})')
            return False

        playbackTask = AudioPlayerPlaybackTask(
            volume = self.__volume,
            filePath = filePath
        )

        playbackThread = Thread(
            target = self.__play,
            args = ( playbackTask, )
        )

        self.__playbackTask = playbackTask
        playbackThread.start()

        return True

    def __play(self, task: AudioPlayerPlaybackTask):
        if not isinstance(task, AudioPlayerPlaybackTask):
            raise TypeError(f'task argument is malformed: \"{task}\"')

        try:
            audioPlayer = AudioPlayer(filename = task.filePath)
        except Exception as e:
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Encountered exception when trying to create new AudioPlayer instance ({task=}): {e}', e, traceback.format_exc())
            return

        audioPlayer.volume = task.volume
        durationSeconds: float | Any | None = None

        try:
            durationSeconds = librosa.get_duration(path = task.filePath)
        except Exception as e:
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attemped to play, but encountered exception when trying to determine duration seconds ({task=}) ({audioPlayer=}) ({durationSeconds=}): {e}', e, traceback.format_exc())
            return

        if not utils.isValidNum(durationSeconds) or durationSeconds < 0 or durationSeconds > utils.getIntMaxSafeSize():
            # This is an extremely gratuitous check, but I want to be absolutely sure that I fully
            # understand the durationSeconds value being provided by librosa. For the purpose of
            # determining a sound file's length, I picked the librosa library rather quickly, and
            # so, I want to be very sure and mindful of its output.
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            self.__timber.log('AudioPlayerMediaPlayer', f'Attempted to play, but encountered bizarre durationSeconds value ({task=}) ({audioPlayer=}) ({durationSeconds=})')
            return

        if task.isCanceled:
            # It is technically possible that playback could have been canceled before we
            # even begin playing this file. So let's do one final cancelation check super
            # quick before we start the actual file playback.
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            return

        audioPlayer.play(
            loop = False,
            block = False
        )

        isStillPlaying = True
        timeZone = self.__timeZoneRepository.getDefault()
        endTime = datetime.now(timeZone) + timedelta(seconds = durationSeconds)

        while isStillPlaying and not task.isCanceled:
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
