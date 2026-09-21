import time
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Final

import aiofiles.ospath
import pygame.mixer
from pygame.mixer import Channel as PygameChannel
from pygame.mixer import Sound as PygameSound

from .pygameMediaPlaybackTask import PygameMediaPlaybackTask
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class PygameMediaPlayer:

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        playbackLoopSleepTimeSeconds: float = 0.125,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.125 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__timber: Final[TimberInterface] = timber
        self.__playbackLoopSleepTimeSeconds: Final[float] = playbackLoopSleepTimeSeconds

        self.__isPlayingOrLoading: bool = False
        self.__volume: float = float(1)
        self.__playbackTask: PygameMediaPlaybackTask | None = None
        self.__filePath: str | None = None

    @property
    def isPlaying(self) -> bool:
        return self.__isPlayingOrLoading or self.__playbackTask is not None

    async def play(self) -> bool:
        self.__isPlayingOrLoading = True
        filePath = self.__filePath

        if not utils.isValidStr(filePath):
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Attempted to play, but filePath has not yet been set ({filePath=})')
            return False
        elif not await aiofiles.ospath.exists(
            path = filePath,
            loop = self.__eventLoop,
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Attempted to play, but filePath does not point to a file that exists ({filePath=})')
            return False
        elif await aiofiles.ospath.isdir(
            s = filePath,
            loop = self.__eventLoop,
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Attempted to play, but filePath points to a directory instead of a file ({filePath=})')
            return False
        elif not await aiofiles.ospath.isfile(
            path = filePath,
            loop = self.__eventLoop,
        ):
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Attempted to play, but filePath points to something that is not a file ({filePath=})')
            return False

        playbackTask = PygameMediaPlaybackTask(
            volume = self.__volume,
            filePath = filePath,
        )

        playbackThread = Thread(
            target = self.__play,
            args = ( playbackTask, ),
        )

        self.__playbackTask = playbackTask
        playbackThread.start()

        return True

    def __play(self, task: PygameMediaPlaybackTask):
        if not isinstance(task, PygameMediaPlaybackTask):
            raise TypeError(f'task argument is malformed: \"{task}\"')

        pygameChannel: PygameChannel | None = None
        pygameChannelException: Exception | None = None

        try:
            pygameChannel = pygame.mixer.find_channel(force = False)
        except Exception as e:
            pygameChannelException = e

        if pygameChannel is None or pygameChannelException is not None:
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Pygame failed to allocate channel ({pygameChannel=}) ({pygameChannelException=}) ({task=})')
            return

        pygameSound: PygameSound | None = None
        pygameSoundException: Exception | None = None

        try:
            pygameSound = PygameSound(task.filePath)
        except Exception as e:
            pygameSoundException = e

        if pygameSound is None or pygameChannelException is not None:
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            self.__timber.log('PygameMediaPlayer', f'Pygame failed to load sound ({pygameSound=}) ({pygameSoundException=}) ({pygameChannel=}) ({pygameChannelException=}) ({task=})')
            return

        pygameChannel.set_volume(task.volume)

        if task.isCanceled:
            self.__playbackTask = None
            self.__isPlayingOrLoading = False
            return

        pygameChannel.play(pygameSound)

        while pygameChannel.get_busy() and not task.isCanceled:
            time.sleep(self.__playbackLoopSleepTimeSeconds)

        if task.isCanceled:
            pygameChannel.stop()

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
            self.__volume = float(0)
            self.__timber.log('PygameMediaPlayer', f'The given volume parameter was too small and has been coerced to {float(0)} ({volume=})')
        elif volume > 100:
            self.__volume = float(1)
            self.__timber.log('PygameMediaPlayer', f'The given volume parameter was too large and has been coerced to {float(1)} ({volume=})')
        else:
            self.__volume = float(volume) / float(100)

    async def stop(self):
        if not self.isPlaying:
            return

        playbackTask = self.__playbackTask

        if playbackTask is not None:
            playbackTask.cancel()
