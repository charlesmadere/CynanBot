from asyncio import AbstractEventLoop
from typing import Final

import aiofiles.ospath

from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class PygameMediaPlayer:

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__timber: Final[TimberInterface] = timber

        self.__isPlayingOrLoading: bool = False
        self.__volume: float = float(1)
        self.__filePath: str | None = None

    @property
    def isPlaying(self) -> bool:
        return self.__isPlayingOrLoading

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

        # TODO
        pass

        return True

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

        # TODO
        pass
