from audioplayer import AudioPlayer

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

    @property
    def isPlaying(self) -> bool:
        return self.__isPlaying

    async def play(self):
        # TODO
        pass

    async def setMedia(self, filePath: str):
        # TODO
        pass

    async def setVolume(self, volume: int):
        self.__volume = volume

    async def stop(self):
        # TODO
        pass
